"""HTML report generation — Allure-style test report with vis.js graph."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

from flowscout.analysis.graph import ExplorationResult, Flow

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_VENDOR_DIR = Path(__file__).parent / "vendor"
_ENV = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=True,
)


class HTMLReporter:
    """Generates a standalone HTML report."""

    def generate(self, result: ExplorationResult, output_path: str) -> None:
        """Generate the HTML report file."""
        from flowscout import __version__

        report_dir = Path(output_path).parent
        graph_data = _build_graph_data(result)
        error_results = [
            r
            for r in result.results
            if r.outcome.value
            in (
                "validation_error",
                "network_error",
                "console_error",
                "timeout",
                "exception",
            )
        ]

        # Build action label lookup
        action_labels = {aid: a.label for aid, a in result.actions.items()}

        # Group flows by category (= test suites)
        flow_groups: dict[str, list] = defaultdict(list)
        for flow in result.flows:
            flow_groups[flow.category or "Other"].append(flow)

        # Compute per-group summaries
        group_summaries: dict[str, dict[str, int]] = {}
        for cat, group_flows in flow_groups.items():
            group_summaries[cat] = {
                "pass": sum(
                    1
                    for f in group_flows
                    if f.verdict and f.verdict.verdict.value == "pass"
                ),
                "fail": sum(
                    1
                    for f in group_flows
                    if f.verdict and f.verdict.verdict.value == "fail"
                ),
                "warn": sum(
                    1
                    for f in group_flows
                    if f.verdict and f.verdict.verdict.value == "warn"
                ),
            }

        # Overall verdict counts
        flow_counts = {
            "pass": sum(
                1
                for f in result.flows
                if f.verdict and f.verdict.verdict.value == "pass"
            ),
            "fail": sum(
                1
                for f in result.flows
                if f.verdict and f.verdict.verdict.value == "fail"
            ),
            "warn": sum(
                1
                for f in result.flows
                if f.verdict and f.verdict.verdict.value == "warn"
            ),
        }

        # New: coverage, defects, step summaries
        coverage = _compute_coverage(result)
        page_coverage_map = _build_page_coverage_map(result)
        defects = _build_defects(result)
        step_verdicts_summary = _compute_step_verdicts(result)
        total_test_steps = sum(
            len(f.narrative.steps) if f.narrative and f.narrative.steps else f.depth
            for f in result.flows
        )
        group_pass_rates = _compute_group_pass_rates(flow_groups)

        vis_js = (_VENDOR_DIR / "vis-network.min.js").read_text()

        template = _ENV.get_template("report.html.j2")
        html = template.render(
            start_url=result.config.get("start_url", "unknown"),
            started_at=result.started_at,
            duration=result.duration_seconds,
            config_strategy=result.config.get("strategy", "priority"),
            flows=result.flows,
            flow_groups=dict(flow_groups),
            group_summaries=group_summaries,
            flow_counts=flow_counts,
            states=list(result.states.values()),
            states_by_id=result.states,
            results=result.results,
            actions=action_labels,
            result_screenshot_links=[
                _to_report_asset_href(r.screenshot_path, report_dir=report_dir)
                for r in result.results
            ],
            error_results=error_results,
            graph_json=Markup(json.dumps(graph_data)),
            vis_network_js=Markup(vis_js),
            version=__version__,
            coverage=coverage,
            page_coverage_map=page_coverage_map,
            defects=defects,
            total_test_steps=total_test_steps,
            step_verdicts_summary=step_verdicts_summary,
            group_pass_rates=group_pass_rates,
        )

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)


def _to_report_asset_href(path: str | None, *, report_dir: Path) -> str | None:
    """Build a report-friendly href for local screenshot assets."""
    if not path:
        return None
    asset_path = Path(path)
    if asset_path.is_absolute():
        try:
            return str(asset_path.relative_to(report_dir))
        except ValueError:
            return asset_path.as_uri()
    return str(asset_path)


def _build_graph_data(result: ExplorationResult) -> dict:
    """Build vis.js-compatible graph data."""
    nodes = []
    for sid, state in result.states.items():
        nodes.append(
            {
                "id": sid,
                "label": state.title or state.url,
                "url": state.url,
                "depth": state.depth,
                "signals": state.signals,
            }
        )

    edges = []
    for r in result.results:
        action = result.actions.get(r.action_id)
        edges.append(
            {
                "source": r.source_state_id,
                "target": r.target_state_id,
                "label": action.label if action else r.action_id,
                "outcome": r.outcome.value,
            }
        )

    return {"nodes": nodes, "edges": edges}


def _compute_coverage(result: ExplorationResult) -> dict:
    """Compute page, interaction, and pass-rate coverage metrics."""
    # Page coverage: unique URLs touched in results vs total discovered states
    all_urls = {s.url for s in result.states.values()}
    tested_urls: set[str] = set()
    for r in result.results:
        if r.source_state_id in result.states:
            tested_urls.add(result.states[r.source_state_id].url)
        if r.target_state_id in result.states:
            tested_urls.add(result.states[r.target_state_id].url)

    # Interaction coverage: executed actions vs discovered
    executed_ids = {r.action_id for r in result.results}
    total_discovered = len(result.actions)

    # Pass rate
    passed = sum(
        1
        for f in result.flows
        if f.verdict and f.verdict.verdict.value == "pass"
    )
    total_flows = len(result.flows)

    return {
        "page": {
            "tested": len(tested_urls),
            "total": len(all_urls),
            "pct": round(len(tested_urls) / max(len(all_urls), 1) * 100),
        },
        "interaction": {
            "executed": len(executed_ids),
            "total": total_discovered,
            "pct": round(
                len(executed_ids) / max(total_discovered, 1) * 100,
            ),
        },
        "pass_rate": {
            "passed": passed,
            "total": total_flows,
            "pct": round(passed / max(total_flows, 1) * 100),
        },
    }


def _build_page_coverage_map(result: ExplorationResult) -> list[dict]:
    """For each page, list which test cases cover it."""
    state_to_flows: dict[str, list[dict]] = defaultdict(list)
    for flow in result.flows:
        verdict_val = (
            flow.verdict.verdict.value if flow.verdict else "inconclusive"
        )
        for sid in flow.state_ids:
            state_to_flows[sid].append(
                {
                    "flow_id": flow.flow_id,
                    "name": flow.name,
                    "verdict": verdict_val,
                }
            )

    page_map = []
    for sid, state in result.states.items():
        covering = state_to_flows.get(sid, [])
        page_map.append(
            {
                "state_id": sid,
                "title": state.title or state.url,
                "url": state.url,
                "test_cases": covering,
                "pass_count": sum(
                    1 for c in covering if c["verdict"] == "pass"
                ),
                "fail_count": sum(
                    1 for c in covering if c["verdict"] == "fail"
                ),
                "warn_count": sum(
                    1 for c in covering if c["verdict"] == "warn"
                ),
                "covered": len(covering) > 0,
            }
        )
    return page_map


def _build_defects(result: ExplorationResult) -> dict:
    """Partition flows into failures and warnings."""
    failures = [
        f
        for f in result.flows
        if f.verdict and f.verdict.verdict.value == "fail"
    ]
    warnings = [
        f
        for f in result.flows
        if f.verdict and f.verdict.verdict.value == "warn"
    ]
    return {"failures": failures, "warnings": warnings}


def _compute_step_verdicts(result: ExplorationResult) -> dict[str, int]:
    """Aggregate pass/fail/warn across all narrative steps."""
    counts: dict[str, int] = {"pass": 0, "fail": 0, "warn": 0}
    for flow in result.flows:
        if flow.narrative and flow.narrative.steps:
            for step in flow.narrative.steps:
                if step.verdict:
                    v = step.verdict.value
                    if v in counts:
                        counts[v] += 1
    return counts


def _compute_group_pass_rates(
    flow_groups: dict[str, list[Flow]],
) -> dict[str, int]:
    """Compute pass-rate percentage per test suite."""
    rates: dict[str, int] = {}
    for cat, flows in flow_groups.items():
        total = len(flows)
        passed = sum(
            1
            for f in flows
            if f.verdict and f.verdict.verdict.value == "pass"
        )
        rates[cat] = round(passed / max(total, 1) * 100)
    return rates

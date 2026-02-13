"""HTML report generation — Allure-style test report with vis.js graph."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader

from flowscout.analysis.element_inventory import (
    is_interactive_element_type,
    summarize_element_inventory,
)
from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.text_utils import strip_css_blocks
from flowscout.discovery.actions import ActionResult, OutcomeType
from flowscout.modeling.flows import FlowTemplate, deduplicate_flows
from flowscout.modeling.site_model import NavigationEdge, SiteModel

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_VENDOR_DIR = Path(__file__).parent / "vendor"
# CLI tool, not Flask — Jinja2 used directly with autoescape=True
# nosemgrep: python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2
_ENV = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=True,
)


class ReportDataBuilder:
    """Builds the complete template context dict from an ExplorationResult."""

    def __init__(self, result: ExplorationResult, *, report_dir: Path) -> None:
        self.result = result
        self.report_dir = report_dir

    def build(self) -> dict[str, Any]:
        """Compute and return the full Jinja2 template context."""
        result = self.result
        report_dir = self.report_dir

        site_model = _build_site_model(result=result)
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

        action_labels = {aid: a.label for aid, a in result.actions.items()}
        action_selectors = {aid: a.target_selector for aid, a in result.actions.items()}
        action_metadata = {
            aid: dict(a.metadata or {}) for aid, a in result.actions.items()
        }

        flow_templates, flow_groups = _build_template_flow_groups(
            result=result,
            site_model=site_model,
        )

        group_summaries: dict[str, dict[str, int]] = {}
        for cat, group_flows in flow_groups.items():
            group_summaries[cat] = {
                "pass": sum(1 for f in group_flows if _flow_status(f) == "pass"),
                "fail": sum(1 for f in group_flows if _flow_status(f) == "fail"),
                "warn": sum(1 for f in group_flows if _flow_status(f) == "warn"),
            }

        flow_counts = {
            "pass": sum(1 for f in result.flows if _flow_status(f) == "pass"),
            "fail": sum(1 for f in result.flows if _flow_status(f) == "fail"),
            "warn": sum(1 for f in result.flows if _flow_status(f) == "warn"),
        }
        flow_status_map = {flow.flow_id: _flow_status(flow) for flow in result.flows}

        coverage = _compute_coverage(result)
        page_coverage_map = _build_page_coverage_map(result)
        defects = _build_defects(result)
        step_verdicts_summary = _compute_step_verdicts(result)
        total_test_steps = sum(
            len(f.narrative.steps) if f.narrative and f.narrative.steps else f.depth
            for f in result.flows
        )
        group_pass_rates = _compute_group_pass_rates(flow_groups)

        result_screenshot_links = [
            _to_report_asset_href(r.screenshot_path, report_dir=report_dir)
            for r in result.results
        ]
        diagnostics = _build_diagnostics(
            result=result,
            action_labels=action_labels,
            action_selectors=action_selectors,
            screenshot_links=result_screenshot_links,
        )
        element_inventory = result.element_inventory
        if not element_inventory and result.smart_analyses:
            element_inventory = summarize_element_inventory(
                analyses=result.smart_analyses,
                states_by_id=result.states,
            )
        discovery_timeline = _build_discovery_timeline(
            result=result,
            element_inventory=element_inventory,
        )
        url_inventory_rows = _build_url_inventory_rows(
            element_inventory=element_inventory,
        )
        state_screenshot_links = {
            state_id: _to_report_asset_href(
                state.screenshot_path, report_dir=report_dir
            )
            for state_id, state in result.states.items()
        }
        execution_rows = _build_execution_rows(
            result=result,
            action_labels=action_labels,
            action_selectors=action_selectors,
            action_metadata=action_metadata,
            screenshot_links=result_screenshot_links,
        )
        element_drilldown_map = _build_element_drilldown_map(
            result=result,
            element_inventory=element_inventory,
            execution_rows=execution_rows,
            state_screenshot_links=state_screenshot_links,
        )
        (
            flow_execution_map,
            orphan_execution_rows,
            execution_step_map,
        ) = _build_flow_execution_map(
            result=result,
            execution_rows=execution_rows,
        )
        input_provenance = _build_input_provenance(
            result=result,
            action_metadata=action_metadata,
        )
        locator_quality_rows, locator_recommendations = _build_locator_quality_data(
            result=result,
            site_model=site_model,
        )
        mbt_coverage = _build_mbt_coverage_data(
            result=result,
            site_model=site_model,
        )

        return {
            "start_url": result.config.get("start_url", "unknown"),
            "started_at": result.started_at,
            "duration": result.duration_seconds,
            "config_strategy": result.config.get("strategy", "priority"),
            "flows": result.flows,
            "flow_templates": flow_templates,
            "flow_groups": dict(flow_groups),
            "group_summaries": group_summaries,
            "flow_counts": flow_counts,
            "flow_status_map": flow_status_map,
            "states": list(result.states.values()),
            "states_by_id": result.states,
            "results": result.results,
            "actions": action_labels,
            "action_metadata": action_metadata,
            "result_screenshot_links": result_screenshot_links,
            "error_results": error_results,
            "graph_json": graph_data,
            "execution_rows_json": execution_rows,
            "coverage": coverage,
            "page_coverage_map": page_coverage_map,
            "defects": defects,
            "total_test_steps": total_test_steps,
            "step_verdicts_summary": step_verdicts_summary,
            "group_pass_rates": group_pass_rates,
            "diagnostics": diagnostics,
            "element_inventory": element_inventory,
            "discovery_timeline": discovery_timeline,
            "url_inventory_rows": url_inventory_rows,
            "element_drilldown_map": element_drilldown_map,
            "execution_rows": execution_rows,
            "flow_execution_map": flow_execution_map,
            "orphan_execution_rows": orphan_execution_rows,
            "execution_step_map": execution_step_map,
            "input_provenance": input_provenance,
            "locator_quality_rows": locator_quality_rows,
            "locator_recommendations": locator_recommendations,
            "mbt_coverage": mbt_coverage,
            "site_model_available": bool(site_model),
            "site_model_summary": (
                site_model.summary.model_dump() if site_model is not None else {}
            ),
        }


class HTMLReporter:
    """Generates a standalone HTML report."""

    def generate(self, result: ExplorationResult, output_path: str) -> None:
        """Generate the HTML report file."""
        from flowscout import __version__

        report_dir = Path(output_path).parent
        builder = ReportDataBuilder(result, report_dir=report_dir)
        context = builder.build()

        vis_js = (_VENDOR_DIR / "vis-network.min.js").read_text()
        context["vis_network_js"] = vis_js
        context["version"] = __version__

        template = _ENV.get_template("report.html.j2")
        # All context is internal data, not user input
        html = template.render(**context)  # nosemgrep: direct-use-of-jinja2

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)


# ---------------------------------------------------------------------------
# Data preparation helpers
# ---------------------------------------------------------------------------


def _to_report_asset_href(path: str | None, *, report_dir: Path) -> str | None:
    """Build a report-friendly href for local screenshot assets."""
    if not path:
        return None
    report_dir_abs = report_dir.resolve()
    raw = Path(path)
    asset_path = raw if raw.is_absolute() else (Path.cwd() / raw)
    try:
        asset_abs = asset_path.resolve()
    except OSError:
        asset_abs = asset_path

    try:
        return str(asset_abs.relative_to(report_dir_abs))
    except ValueError:
        if raw.is_absolute():
            return raw.as_uri()
        if asset_abs.is_file():
            return asset_abs.as_uri()
        return str(raw)


def _build_graph_data(result: ExplorationResult) -> dict[str, Any]:
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


def _build_site_model(*, result: ExplorationResult) -> SiteModel | None:
    """Build SiteModel once for report structure data, falling back gracefully."""
    try:
        return SiteModel.from_exploration_result(result=result)
    except ValueError:
        return None


def _build_template_flow_groups(
    *,
    result: ExplorationResult,
    site_model: SiteModel | None = None,
) -> tuple[list[FlowTemplate], dict[str, list[Flow]]]:
    """Group flows by deduplicated page-type sequences for report suites."""
    if not result.flows:
        return [], {}

    templates: list[FlowTemplate] = []
    if site_model is not None and site_model.flow_templates:
        templates = list(site_model.flow_templates)
    else:
        state_to_page_type = _build_state_to_page_type_lookup(result=result)
        templates = deduplicate_flows(
            flows=result.flows,
            state_to_page_type=state_to_page_type,
            actions_by_id=result.actions,
        )

    flow_lookup = {flow.flow_id: flow for flow in result.flows}
    grouped: dict[str, list[Flow]] = {}
    for template in templates:
        group_flows = [
            flow_lookup[flow_id]
            for flow_id in template.instance_flow_ids
            if flow_id in flow_lookup
        ]
        if not group_flows:
            continue
        label = f"{template.name} ({template.occurrence_count} instances)"
        grouped[label] = group_flows

    # Fallback: retain legacy grouping if templates cannot be formed.
    if not grouped:
        fallback: dict[str, list[Flow]] = defaultdict(list)
        for flow in result.flows:
            fallback[flow.category or "Other"].append(flow)
        return [], dict(fallback)

    return templates, grouped


def _build_state_to_page_type_lookup(*, result: ExplorationResult) -> dict[str, str]:
    """Build a state_id -> page_type lookup from analysis signatures or URLs."""
    lookup: dict[str, str] = {}

    for state_id, payload in result.smart_analyses.items():
        if isinstance(payload, dict):
            signature = str(payload.get("structural_signature", "")).strip()
        else:
            signature = str(getattr(payload, "structural_signature", "")).strip()
        if signature:
            lookup[state_id] = signature

    if lookup:
        return lookup

    for state_id, state in result.states.items():
        lookup[state_id] = _url_to_template(state.url)
    return lookup


def _url_to_template(url: str) -> str:
    """Convert URL into a simple template string for fallback grouping."""
    parsed = urlparse(url)
    segments = [segment for segment in parsed.path.rstrip("/").split("/") if segment]
    template_parts: list[str] = []
    for segment in segments:
        if segment.isdigit():
            template_parts.append("{id}")
        else:
            template_parts.append(segment)
    template_path = "/" + "/".join(template_parts) if template_parts else "/"
    return f"{parsed.scheme}://{parsed.netloc}{template_path}"


def _clean_catalog_label(value: Any) -> str:
    """Normalize noisy catalog labels to concise, human-readable text."""
    text = str(value or "").strip()
    if not text:
        return ""

    # Some pages inline CSS pseudo-element content into extracted labels.
    text = str(strip_css_blocks(text))
    if len(text) > 120:
        return f"{text[:117].rstrip()}..."
    return text


def _build_locator_quality_data(
    *,
    result: ExplorationResult,
    site_model: SiteModel | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Build per-page locator quality metrics from the Layer-2 site model."""
    model = site_model or _build_site_model(result=result)
    if model is None:
        return [], []

    rows: list[dict[str, Any]] = []
    for page_type in model.page_types:
        rounded = int(round(page_type.locator_quality_score))
        rows.append(
            {
                "name": page_type.name,
                "page_type_id": page_type.page_type_id,
                "instance_count": page_type.instance_count,
                "selector_count": len(page_type.catalog.entries),
                "quality_score": rounded,
                "quality_text": f"Locator Quality: {rounded}% stable",
            }
        )

    rows.sort(key=lambda row: (-int(row["quality_score"]), str(row["name"])))
    return rows, model.locator_recommendations


def _build_mbt_coverage_data(
    *,
    result: ExplorationResult,
    site_model: SiteModel | None = None,
) -> dict[str, Any]:
    """Build MBT coverage metrics and matrix from the Layer-2 SiteModel."""
    model = site_model or _build_site_model(result=result)
    if model is None:
        return {}

    from flowscout.mbt.coverage import compute_model_coverage

    coverage = compute_model_coverage(model=model)
    if coverage.total_states == 0 and coverage.total_edges == 0:
        return {}

    page_names = {
        page_type.page_type_id: page_type.name for page_type in model.page_types
    }
    action_names = sorted(
        {
            action_name
            for row in coverage.coverage_matrix.values()
            for action_name in row
        },
    )
    matrix_rows: list[dict[str, Any]] = []
    for page_type_id in sorted(coverage.coverage_matrix):
        row = coverage.coverage_matrix[page_type_id]
        matrix_rows.append(
            {
                "page_type_id": page_type_id,
                "page_name": page_names.get(page_type_id, page_type_id),
                "actions": [
                    {
                        "action": action_name,
                        "covered": bool(row.get(action_name, False)),
                    }
                    for action_name in action_names
                ],
            },
        )

    model_edges_by_key: dict[tuple[str, str, str], NavigationEdge] = {}
    for edge in model.navigation_edges:
        edge_key = (edge.from_page_type, edge.to_page_type, edge.action_type.value)
        model_edges_by_key.setdefault(edge_key, edge)

    uncovered_edges = [
        _build_uncovered_edge_row(
            from_page_type=from_page_type,
            to_page_type=to_page_type,
            action_type=action_type,
            page_names=page_names,
            model_edges_by_key=model_edges_by_key,
        )
        for from_page_type, to_page_type, action_type in coverage.uncovered_edges
    ]

    return {
        "state": {
            "pct": coverage.state_coverage,
            "covered": coverage.covered_states,
            "total": coverage.total_states,
            "uncovered": coverage.uncovered_states,
        },
        "edge": {
            "pct": coverage.edge_coverage,
            "covered": coverage.covered_edges,
            "total": coverage.total_edges,
            "uncovered": uncovered_edges,
        },
        "path": {
            "pct": coverage.path_coverage,
            "covered": coverage.covered_paths,
            "total": coverage.total_paths,
        },
        "actions": action_names,
        "matrix_rows": matrix_rows,
    }


def _build_uncovered_edge_row(
    *,
    from_page_type: str,
    to_page_type: str,
    action_type: str,
    page_names: dict[str, str],
    model_edges_by_key: dict[tuple[str, str, str], Any],
) -> dict[str, Any]:
    """Build a report row for one uncovered transition."""
    edge = model_edges_by_key.get((from_page_type, to_page_type, action_type))
    guards = sorted(set(getattr(edge, "guards", []))) if edge else []
    inferred_from = str(getattr(edge, "inferred_from", "")).strip() if edge else ""
    return {
        "from_page_type": from_page_type,
        "to_page_type": to_page_type,
        "action_type": action_type,
        "from_name": page_names.get(from_page_type, from_page_type),
        "to_name": page_names.get(to_page_type, to_page_type),
        "guards": guards,
        "inferred_from": inferred_from,
    }


def _extract_dom_id_from_selector(selector: str) -> str:
    """Extract a DOM id token from an id-based CSS selector."""
    text = str(selector or "").strip()
    if not text.startswith("#"):
        return ""
    token = text[1:].split()[0]
    token = token.split(".")[0].split("[")[0].split(":")[0]
    return token.strip()


def _flow_status(flow: Flow) -> str:
    """Map flow stability and outcomes to report status labels."""
    if flow.is_stable:
        return "pass"
    severe_outcomes = {
        OutcomeType.NETWORK_ERROR,
        OutcomeType.TIMEOUT,
        OutcomeType.EXCEPTION,
    }
    if any(outcome in severe_outcomes for outcome in flow.outcomes):
        return "fail"
    return "warn"


def _compute_coverage(result: ExplorationResult) -> dict[str, Any]:
    """Compute page, interaction, and pass-rate coverage metrics."""
    all_urls = {s.url for s in result.states.values()}
    tested_urls: set[str] = set()
    for r in result.results:
        if r.source_state_id in result.states:
            tested_urls.add(result.states[r.source_state_id].url)
        if r.target_state_id in result.states:
            tested_urls.add(result.states[r.target_state_id].url)

    executed_ids = {r.action_id for r in result.results}
    total_discovered = len(result.actions)

    passed = sum(1 for f in result.flows if _flow_status(f) == "pass")
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


def _build_page_coverage_map(result: ExplorationResult) -> list[dict[str, Any]]:
    """For each page, list which test cases cover it."""
    state_to_flows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for flow in result.flows:
        verdict_val = _flow_status(flow)
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
                "pass_count": sum(1 for c in covering if c["verdict"] == "pass"),
                "fail_count": sum(1 for c in covering if c["verdict"] == "fail"),
                "warn_count": sum(1 for c in covering if c["verdict"] == "warn"),
                "covered": len(covering) > 0,
            }
        )
    return page_map


def _build_input_provenance(
    *,
    result: ExplorationResult,
    action_metadata: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """Summarize where generated input values came from."""
    source_counts: Counter[str] = Counter()
    samples: list[dict[str, str]] = []

    for action in result.actions.values():
        if action.action_type.value != "fill":
            continue
        metadata = action_metadata.get(action.action_id, {})
        source = metadata.get("input_source", "unknown")
        source_counts[source] += 1
        if len(samples) < 10:
            samples.append(
                {
                    "label": action.label,
                    "source": source,
                }
            )

    return {
        "profile": result.config.get("input_profile", "safe"),
        "fill_actions": sum(
            1 for a in result.actions.values() if a.action_type.value == "fill"
        ),
        "source_breakdown": [
            {"source": source, "count": count}
            for source, count in source_counts.most_common()
        ],
        "samples": samples,
    }


def _build_discovery_timeline(
    *,
    result: ExplorationResult,
    element_inventory: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Build per-state discovery progression showing newly seen elements."""
    if not element_inventory:
        return []

    per_page_rows = {
        str(row.get("state_id", "")): row
        for row in element_inventory.get("per_page", [])
        if isinstance(row, dict)
    }
    analyses = result.smart_analyses or {}

    rows: list[dict[str, Any]] = []
    seen_signatures: set[str] = set()
    for order, (state_id, state) in enumerate(result.states.items(), start=1):
        page_row = per_page_rows.get(state_id, {})
        analysis = analyses.get(state_id, {})
        catalog = analysis.get("catalog", {}) if isinstance(analysis, dict) else {}
        entries = catalog.get("entries", []) if isinstance(catalog, dict) else []

        signatures: set[str] = set()
        if isinstance(entries, list):
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                signatures.add(
                    "|".join(
                        [
                            str(entry.get("element_type", "")),
                            str(entry.get("selector", "")),
                            str(entry.get("label", "")),
                        ]
                    )
                )
        new_elements = len([sig for sig in signatures if sig not in seen_signatures])
        seen_signatures.update(signatures)

        rows.append(
            {
                "order": order,
                "state_id": state_id,
                "state_short": state_id[:8],
                "title": state.title or state.url,
                "url": state.url,
                "depth": state.depth,
                "interactive": int(page_row.get("interactive_elements", 0)),
                "non_interactive": int(page_row.get("non_interactive_elements", 0)),
                "total": int(page_row.get("total_elements", 0)),
                "new_elements": new_elements,
            }
        )
    return rows


def _build_url_inventory_rows(
    *,
    element_inventory: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Build URL-level aggregated inventory rows from per-state inventory."""
    if not element_inventory:
        return []

    per_state_rows = [
        row for row in element_inventory.get("per_page", []) if isinstance(row, dict)
    ]
    if not per_state_rows:
        return []

    grouped: dict[str, dict[str, Any]] = {}
    for row in per_state_rows:
        state_id = str(row.get("state_id", "")).strip()
        url = str(row.get("url", "")).strip()
        title = str(row.get("title", "")).strip()
        interactive = int(row.get("interactive_elements", 0))
        non_interactive = int(row.get("non_interactive_elements", 0))
        total = int(row.get("total_elements", interactive + non_interactive))

        group_key = url or f"state:{state_id}"
        bucket = grouped.setdefault(
            group_key,
            {
                "url": url,
                "title_counts": Counter(),
                "interactive_elements": 0,
                "non_interactive_elements": 0,
                "total_elements": 0,
                "state_ids": [],
            },
        )

        if title:
            bucket["title_counts"][title] += 1
        bucket["interactive_elements"] += interactive
        bucket["non_interactive_elements"] += non_interactive
        bucket["total_elements"] += total
        if state_id:
            bucket["state_ids"].append(state_id)

    rows: list[dict[str, Any]] = []
    for bucket in grouped.values():
        state_ids = list(dict.fromkeys(bucket["state_ids"]))
        title_counts: Counter[str] = bucket["title_counts"]
        title = title_counts.most_common(1)[0][0] if title_counts else ""
        rows.append(
            {
                "title": title,
                "url": bucket["url"],
                "interactive_elements": int(bucket["interactive_elements"]),
                "non_interactive_elements": int(bucket["non_interactive_elements"]),
                "total_elements": int(bucket["total_elements"]),
                "state_count": len(state_ids),
                "state_ids": state_ids,
                "state_ids_short": [sid[:8] for sid in state_ids],
            }
        )

    rows.sort(
        key=lambda row: (
            -int(row["total_elements"]),
            -int(row["state_count"]),
            str(row.get("url", "")),
        )
    )
    return rows


def _build_element_drilldown_map(
    *,
    result: ExplorationResult,
    element_inventory: dict[str, Any] | None,
    execution_rows: list[dict[str, Any]] | None = None,
    state_screenshot_links: dict[str, str | None] | None = None,
) -> dict[str, dict[str, Any]]:
    """Build per-state element drilldown data for the Elements modal."""
    per_page_rows = {
        str(row.get("state_id", "")): row
        for row in (element_inventory or {}).get("per_page", [])
        if isinstance(row, dict)
    }
    analyses = result.smart_analyses or {}
    state_screens = state_screenshot_links or {}

    evidence_by_state: dict[str, str] = {}
    evidence_by_state_selector: dict[tuple[str, str], str] = {}
    for row in execution_rows or []:
        state_id = str(row.get("source_state_id", "")).strip()
        selector = str(row.get("target_selector", "")).strip()
        screenshot = row.get("screenshot_link")
        if not state_id or not isinstance(screenshot, str) or not screenshot:
            continue
        evidence_by_state.setdefault(state_id, screenshot)
        if selector:
            evidence_by_state_selector.setdefault((state_id, selector), screenshot)

    drilldown: dict[str, dict[str, Any]] = {}
    for state_id, state in result.states.items():
        page_row = per_page_rows.get(state_id, {})
        analysis = analyses.get(state_id, {})
        catalog = analysis.get("catalog", {}) if isinstance(analysis, dict) else {}
        entries = catalog.get("entries", []) if isinstance(catalog, dict) else []

        type_counts: Counter[str] = Counter()
        zone_counts: Counter[str] = Counter()
        entry_rows: list[dict[str, Any]] = []
        interactive_count = int(page_row.get("interactive_elements", 0))
        non_interactive_count = int(page_row.get("non_interactive_elements", 0))
        visible_count = 0
        hidden_count = 0

        if isinstance(entries, list):
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                element_type = str(entry.get("element_type") or "other").strip().lower()
                zone_type = (
                    str(entry.get("zone_type") or "main_content").strip().lower()
                )
                if not element_type:
                    element_type = "other"
                if not zone_type:
                    zone_type = "main_content"

                type_counts[element_type] += 1
                zone_counts[zone_type] += 1

                if not page_row:
                    if is_interactive_element_type(element_type):
                        interactive_count += 1
                    else:
                        non_interactive_count += 1

                label = _clean_catalog_label(entry.get("label"))
                semantic_name = str(entry.get("semantic_name") or "").strip()
                selector = str(entry.get("selector") or "").strip()
                dom_id = str(entry.get("dom_id") or "").strip()
                if not dom_id:
                    dom_id = _extract_dom_id_from_selector(selector)
                tag = str(entry.get("tag") or "").strip().lower() or "unknown"
                aria_role = str(entry.get("aria_role") or "").strip().lower()
                input_type = str(entry.get("input_type") or "").strip().lower()
                raw_visible = entry.get("is_visible")
                if isinstance(raw_visible, bool):
                    is_visible = raw_visible
                else:
                    is_visible = bool(entry.get("bounding_box"))
                if is_visible:
                    visible_count += 1
                else:
                    hidden_count += 1
                is_interactive = is_interactive_element_type(element_type)
                display_label = label or semantic_name or f"{tag} element"
                screenshot_link = None
                screenshot_source = ""
                if selector and (state_id, selector) in evidence_by_state_selector:
                    screenshot_link = evidence_by_state_selector[(state_id, selector)]
                    screenshot_source = "action_target"
                elif state_id in evidence_by_state:
                    screenshot_link = evidence_by_state[state_id]
                    screenshot_source = "state_action"
                elif state_screens.get(state_id):
                    screenshot_link = state_screens.get(state_id)
                    screenshot_source = "state_snapshot"
                entry_rows.append(
                    {
                        "label": display_label,
                        "selector": selector,
                        "dom_id": dom_id,
                        "element_type": element_type,
                        "zone_type": zone_type,
                        "tag": tag,
                        "aria_role": aria_role,
                        "input_type": input_type,
                        "is_visible": is_visible,
                        "is_interactive": is_interactive,
                        "screenshot_link": screenshot_link,
                        "screenshot_source": screenshot_source,
                    }
                )

        entry_rows.sort(
            key=lambda row: (
                not bool(row.get("is_visible", True)),
                not bool(row.get("is_interactive")),
                str(row.get("element_type", "")),
                str(row.get("label", "")),
                str(row.get("selector", "")),
            )
        )
        max_modal_rows = 250
        entries_for_modal = entry_rows[:max_modal_rows]

        total_count = int(
            page_row.get("total_elements", interactive_count + non_interactive_count)
        )
        drilldown[state_id] = {
            "state_id": state_id,
            "state_short": state_id[:8],
            "title": state.title or state.url,
            "url": state.url,
            "depth": state.depth,
            "interactive": interactive_count,
            "non_interactive": non_interactive_count,
            "total": total_count,
            "visible": visible_count,
            "hidden": hidden_count,
            "catalog_entry_count": len(entry_rows),
            "entries_truncated": len(entry_rows) > max_modal_rows,
            "entries": entries_for_modal,
            "top_types": [
                {"name": name, "count": count}
                for name, count in sorted(
                    type_counts.items(),
                    key=lambda item: (-item[1], item[0]),
                )[:8]
            ],
            "top_zones": [
                {"name": name, "count": count}
                for name, count in sorted(
                    zone_counts.items(),
                    key=lambda item: (-item[1], item[0]),
                )[:6]
            ],
        }

    return drilldown


def _build_execution_rows(
    *,
    result: ExplorationResult,
    action_labels: dict[str, str],
    action_selectors: dict[str, str],
    action_metadata: dict[str, dict[str, str]],
    screenshot_links: list[str | None],
) -> list[dict[str, Any]]:
    """Build enriched execution rows for table + modal drill-down."""
    rows: list[dict[str, Any]] = []
    for index, action_result in enumerate(result.results, start=1):
        source_state = result.states.get(action_result.source_state_id)
        target_state = result.states.get(action_result.target_state_id)
        metadata = action_metadata.get(action_result.action_id, {})

        rows.append(
            {
                "index": index,
                "source_state_id": action_result.source_state_id,
                "target_state_id": action_result.target_state_id,
                "source_state_short": action_result.source_state_id[:8],
                "target_state_short": action_result.target_state_id[:8],
                "source_page": (
                    source_state.title
                    if source_state and source_state.title
                    else (source_state.url if source_state else "Unknown page")
                ),
                "target_page": (
                    target_state.title
                    if target_state and target_state.title
                    else (target_state.url if target_state else "Unknown page")
                ),
                "action_id": action_result.action_id,
                "action_label": action_labels.get(
                    action_result.action_id, action_result.action_id
                ),
                "target_selector": action_selectors.get(action_result.action_id, ""),
                "dom_id": (
                    metadata.get("dom_id", "")
                    or _extract_dom_id_from_selector(
                        action_selectors.get(action_result.action_id, ""),
                    )
                ),
                "expected": "",
                "actual": (
                    action_result.message
                    or action_result.observation_notes
                    or action_result.outcome.value
                ),
                "outcome": action_result.outcome.value,
                "verdict": (
                    "pass"
                    if float(action_result.stability_score or 0.0) >= 0.7
                    else "warn"
                ),
                "confidence_pct": round(
                    float(action_result.stability_score or 0.0) * 100
                ),
                "confidence_reason": action_result.observation_notes or "",
                "duration_ms": round(float(action_result.duration_ms or 0.0)),
                "url_before": action_result.url_before or "",
                "url_after": action_result.url_after or "",
                "message": action_result.message or "",
                "error_messages": list(action_result.error_messages or []),
                "console_errors": list(action_result.console_errors or []),
                "screenshot_link": screenshot_links[index - 1],
                "input_source": metadata.get("input_source", ""),
                "input_profile": metadata.get("input_profile", ""),
            }
        )
    return rows


def _build_flow_execution_map(
    *,
    result: ExplorationResult,
    execution_rows: list[dict[str, Any]],
) -> tuple[
    dict[str, list[dict[str, Any]]], list[dict[str, Any]], dict[int, dict[str, Any]]
]:
    """Map execution rows to flows and return unmatched rows."""
    rows_by_index = {int(row["index"]): row for row in execution_rows}
    indexes_by_action: dict[str, list[int]] = defaultdict(list)
    for row in execution_rows:
        indexes_by_action[str(row.get("action_id", ""))].append(int(row["index"]))

    used_indexes: set[int] = set()
    flow_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    step_map: dict[int, dict[str, Any]] = {}

    for flow in result.flows:
        for flow_step, action_id in enumerate(flow.action_ids, start=1):
            source_state_id = (
                flow.state_ids[flow_step - 1]
                if flow_step - 1 < len(flow.state_ids)
                else ""
            )
            step_index = _select_matching_step_index(
                action_id=action_id,
                source_state_id=source_state_id,
                rows_by_index=rows_by_index,
                indexes_by_action=indexes_by_action,
                used_indexes=used_indexes,
            )
            if step_index is None:
                continue

            matched = dict(rows_by_index[step_index])
            matched["flow_step"] = flow_step
            matched["flow_id"] = flow.flow_id
            matched["flow_name"] = flow.name
            flow_rows[flow.flow_id].append(matched)
            step_map[step_index] = {
                "flow_id": flow.flow_id,
                "flow_name": flow.name,
                "flow_step": flow_step,
            }
            used_indexes.add(step_index)

    orphans = [row for row in execution_rows if int(row["index"]) not in used_indexes]
    return dict(flow_rows), orphans, step_map


def _select_matching_step_index(
    *,
    action_id: str,
    source_state_id: str,
    rows_by_index: dict[int, dict[str, Any]],
    indexes_by_action: dict[str, list[int]],
    used_indexes: set[int],
) -> int | None:
    """Select the next execution step index for a flow step."""
    candidate_indexes = indexes_by_action.get(action_id, [])
    if not candidate_indexes:
        return None

    for index in candidate_indexes:
        if index in used_indexes:
            continue
        row_source = str(rows_by_index.get(index, {}).get("source_state_id", ""))
        if row_source == source_state_id:
            return index

    for index in candidate_indexes:
        if index not in used_indexes:
            return index
    return None


def _build_defects(result: ExplorationResult) -> dict[str, list[Flow]]:
    """Partition flows into failures and warnings."""
    failures = [f for f in result.flows if _flow_status(f) == "fail"]
    warnings = [f for f in result.flows if _flow_status(f) == "warn"]
    return {"failures": failures, "warnings": warnings}


def _compute_step_verdicts(result: ExplorationResult) -> dict[str, int]:
    """Aggregate pass/fail/warn across all narrative steps."""
    counts: dict[str, int] = {
        "pass": 0,
        "fail": 0,
        "warn": 0,
    }  # nosec B105 - verdict labels, not passwords
    for flow in result.flows:
        if flow.narrative and flow.narrative.steps:
            for step in flow.narrative.steps:
                if step.is_stable:
                    counts["pass"] += 1
                    continue
                if step.outcome in {
                    OutcomeType.NETWORK_ERROR,
                    OutcomeType.TIMEOUT,
                    OutcomeType.EXCEPTION,
                }:
                    counts["fail"] += 1
                    continue
                counts["warn"] += 1
    return counts


def _compute_group_pass_rates(
    flow_groups: dict[str, list[Flow]],
) -> dict[str, int]:
    """Compute pass-rate percentage per test suite."""
    rates: dict[str, int] = {}
    for cat, flows in flow_groups.items():
        total = len(flows)
        passed = sum(1 for f in flows if _flow_status(f) == "pass")
        rates[cat] = round(passed / max(total, 1) * 100)
    return rates


def _build_diagnostics(
    *,
    result: ExplorationResult,
    action_labels: dict[str, str],
    action_selectors: dict[str, str],
    screenshot_links: list[str | None],
    low_confidence_threshold: float = 0.6,
) -> dict[str, Any]:
    """Build report diagnostics for low-confidence and flaky transitions."""
    low_confidence_items: list[dict[str, Any]] = []
    reason_counts: Counter[str] = Counter()
    transition_outcomes: dict[tuple[str, str], set[str]] = defaultdict(set)
    transition_occurrences: Counter[tuple[str, str]] = Counter()

    for index, action_result in enumerate(result.results, start=1):
        key = (action_result.source_state_id, action_result.action_id)
        outcome = action_result.outcome.value
        transition_outcomes[key].add(outcome)
        transition_occurrences[key] += 1

        confidence = float(action_result.stability_score or 0.0)
        if confidence < low_confidence_threshold:
            reason = (action_result.observation_notes or "").strip() or "unspecified"
            reason_counts[reason] += 1
            low_confidence_items.append(
                {
                    "step_index": index,
                    "source_state_short": action_result.source_state_id[:8],
                    "target_state_short": action_result.target_state_id[:8],
                    "source_page": _state_display_name(
                        result,
                        action_result.source_state_id,
                    ),
                    "target_page": _state_display_name(
                        result,
                        action_result.target_state_id,
                    ),
                    "action_label": action_labels.get(
                        action_result.action_id,
                        action_result.action_id,
                    ),
                    "selector": action_selectors.get(action_result.action_id, ""),
                    "confidence_pct": round(confidence * 100),
                    "confidence_reason": reason,
                    "outcome": outcome,
                    "expected": "",
                    "actual": (
                        action_result.message
                        or action_result.observation_notes
                        or action_result.outcome.value
                    ),
                    "detail": _summarize_action_detail(action_result),
                    "evidence_link": screenshot_links[index - 1],
                }
            )

    flaky_items: list[dict[str, Any]] = []
    for transition_key, outcomes in transition_outcomes.items():
        if len(outcomes) < 2:
            continue
        source_state_id, action_id = transition_key
        flaky_items.append(
            {
                "source_state_short": source_state_id[:8],
                "source_page": _state_display_name(result, source_state_id),
                "action_label": action_labels.get(action_id, action_id),
                "action_id": action_id,
                "outcomes": sorted(outcomes),
                "occurrences": transition_occurrences[transition_key],
            }
        )

    flaky_items.sort(
        key=lambda item: (
            len(item["outcomes"]),
            item["occurrences"],
        ),
        reverse=True,
    )
    low_confidence_items.sort(
        key=lambda item: item["confidence_pct"],
    )

    total_steps = len(result.results)
    low_confidence_count = len(low_confidence_items)
    reason_breakdown = [
        {"reason": reason, "count": count}
        for reason, count in reason_counts.most_common(5)
    ]

    return {
        "low_confidence_threshold": low_confidence_threshold,
        "total_steps": total_steps,
        "low_confidence_count": low_confidence_count,
        "low_confidence_pct": round(
            low_confidence_count / max(total_steps, 1) * 100,
        ),
        "low_confidence_items": low_confidence_items[:25],
        "reason_breakdown": reason_breakdown,
        "flaky_items": flaky_items[:25],
        "flaky_paths_count": len(flaky_items),
    }


def _state_display_name(result: ExplorationResult, state_id: str) -> str:
    """Return human-readable page label for a state id."""
    state = result.states.get(state_id)
    if not state:
        return "Unknown page"
    if state.title and str(state.title).strip():
        return str(state.title).strip()
    if state.url and str(state.url).strip():
        return str(state.url).strip()
    return "Unknown page"


def _summarize_action_detail(action_result: ActionResult) -> str:
    """Return compact diagnostic detail from result error fields."""
    if getattr(action_result, "error_messages", None):
        errors = action_result.error_messages
        if errors:
            return str(errors[0])
    if getattr(action_result, "console_errors", None):
        console_errors = action_result.console_errors
        if console_errors:
            return str(console_errors[0])
    message = (getattr(action_result, "message", "") or "").strip()
    if message:
        return message
    return ""

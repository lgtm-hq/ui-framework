"""Markdown export for CI/CD integration and PR comments."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from flowscout.analysis.graph import ExplorationResult


def generate_markdown_report(result: ExplorationResult, output_path: str) -> None:
    """Generate a structured Markdown summary from an exploration result."""
    lines = _build_markdown(result)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def _build_markdown(result: ExplorationResult) -> list[str]:
    """Build Markdown content lines from an exploration result."""
    lines: list[str] = []
    start_url = result.config.get("start_url", "unknown")

    lines.append(f"# Flowscout Report — {start_url}")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Start URL | {start_url} |")
    lines.append(f"| Duration | {result.duration_seconds:.1f}s |")
    lines.append(f"| States discovered | {len(result.states)} |")
    lines.append(f"| Actions executed | {len(result.results)} |")
    lines.append(f"| Flows extracted | {len(result.flows)} |")

    # Verdict summary
    verdict_counts: Counter[str] = Counter()
    for flow in result.flows:
        if flow.verdict:
            verdict_counts[flow.verdict.verdict.value] += 1

    if verdict_counts:
        pass_count = verdict_counts.get("pass", 0)
        fail_count = verdict_counts.get("fail", 0)
        warn_count = verdict_counts.get("warn", 0)
        lines.append(f"| Passed | {pass_count} |")
        lines.append(f"| Failed | {fail_count} |")
        lines.append(f"| Warnings | {warn_count} |")
    lines.append("")

    # Outcome breakdown
    outcome_counts: Counter[str] = Counter()
    for r in result.results:
        outcome_counts[r.outcome.value] += 1

    if outcome_counts:
        lines.append("## Outcome Breakdown")
        lines.append("")
        lines.append("| Outcome | Count |")
        lines.append("|---------|-------|")
        for outcome, count in outcome_counts.most_common():
            lines.append(f"| {outcome} | {count} |")
        lines.append("")

    # Flow list
    if result.flows:
        lines.append("## Flows")
        lines.append("")
        for flow in result.flows:
            verdict_str = ""
            if flow.verdict:
                v = flow.verdict.verdict.value
                emoji = {
                    "pass": "PASS",
                    "fail": "FAIL",
                    "warn": "WARN",
                }.get(  # nosec B105 - verdict labels, not passwords
                    v, v.upper()
                )
                verdict_str = f" [{emoji}]"
            lines.append(f"- **{flow.name}**{verdict_str}")
            if flow.description:
                lines.append(f"  {flow.description}")
        lines.append("")

    # Coverage metrics
    all_urls = {s.url for s in result.states.values()}
    tested_urls: set[str] = set()
    for r in result.results:
        if r.source_state_id in result.states:
            tested_urls.add(result.states[r.source_state_id].url)
        if r.target_state_id in result.states:
            tested_urls.add(result.states[r.target_state_id].url)

    page_coverage = round(len(tested_urls) / max(len(all_urls), 1) * 100)
    executed_ids = {r.action_id for r in result.results}
    action_coverage = round(len(executed_ids) / max(len(result.actions), 1) * 100)

    lines.append("## Coverage")
    lines.append("")
    lines.append(
        f"- Page coverage: {page_coverage}% ({len(tested_urls)}/{len(all_urls)})"
    )
    lines.append(
        f"- Action coverage: {action_coverage}%"
        f" ({len(executed_ids)}/{len(result.actions)})"
    )
    lines.append("")

    return lines

"""BDD output — Gherkin feature files and Markdown test reports."""

from __future__ import annotations

from pathlib import Path

from flowscout.analysis.graph import ExplorationResult
from flowscout.discovery.actions import OutcomeType


def generate_feature_file(result: ExplorationResult, output_path: str) -> str:
    """Generate a Gherkin .feature file from exploration results.

    One Feature per run, one Scenario per flow.
    """
    start_url = result.config.get("start_url", "https://example.com")
    lines = [
        f"Feature: Exploration of {start_url}",
        "  Automated exploration performed by flowscout",
        "",
    ]

    for flow in result.flows:
        narrative = getattr(flow, "narrative", None)
        if narrative and narrative.gherkin:
            lines.append(narrative.gherkin)
        else:
            # Fallback: generate basic scenario from flow data
            lines.append(f"  Scenario: {flow.name}")
            lines.append("    Given I am on the start page")
            for i, action_id in enumerate(flow.action_ids):
                action = result.actions.get(action_id)
                if action:
                    lines.append(f'    When I perform "{action.label}"')
                    outcome = flow.outcomes[i] if i < len(flow.outcomes) else None
                    if outcome:
                        lines.append(f"    Then the outcome should be {outcome.value}")
        lines.append("")

    content = "\n".join(lines)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return str(path)


def generate_markdown_report(result: ExplorationResult, output_path: str) -> str:
    """Generate a Markdown test report with summary and step tables."""
    start_url = result.config.get("start_url", "https://example.com")

    # Count stability statuses across all flows
    pass_count = 0
    fail_count = 0
    warn_count = 0
    for flow in result.flows:
        if flow.is_stable:
            pass_count += 1
        elif any(
            outcome
            in {OutcomeType.NETWORK_ERROR, OutcomeType.TIMEOUT, OutcomeType.EXCEPTION}
            for outcome in flow.outcomes
        ):
            fail_count += 1
        else:
            warn_count += 1

    total = pass_count + fail_count + warn_count
    lines = [
        f"# Exploration Report: {start_url}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| States | {len(result.states)} |",
        f"| Actions Executed | {len(result.results)} |",
        f"| Flows | {len(result.flows)} |",
        f"| Passed | {pass_count} |",
        f"| Failed | {fail_count} |",
        f"| Warnings | {warn_count} |",
        f"| Total Steps | {total} |",
        "",
    ]

    # Per-journey sections
    for flow in result.flows:
        narrative = getattr(flow, "narrative", None)
        if flow.is_stable:
            verdict_label = "STABLE"
        elif any(
            outcome
            in {OutcomeType.NETWORK_ERROR, OutcomeType.TIMEOUT, OutcomeType.EXCEPTION}
            for outcome in flow.outcomes
        ):
            verdict_label = "UNSTABLE/SEVERE"
        else:
            verdict_label = "UNSTABLE"

        lines.append(f"## {flow.name} [{verdict_label}]")
        lines.append("")

        if narrative and narrative.precondition:
            lines.append(f"**Precondition:** {narrative.precondition}")
            lines.append("")

        if narrative and narrative.steps:
            lines.append("| Step | Action | Expected | Actual | Stability |")
            lines.append("|------|--------|----------|--------|-----------|")
            for step in narrative.steps:
                lines.append(
                    f"| {step.step_number} | {step.action_description[:50]} | "
                    f"{step.expected[:40]} | {step.actual[:40]} | "
                    f"{step.stability_score:.2f} |"
                )
            lines.append("")

        if narrative and narrative.conclusion:
            lines.append(f"**Conclusion:** {narrative.conclusion}")
            lines.append("")

    content = "\n".join(lines)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return str(path)

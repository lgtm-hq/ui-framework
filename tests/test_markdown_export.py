"""Tests for markdown export."""

from __future__ import annotations

from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.reporting.markdown_export import generate_markdown_report


def _make_result(
    *,
    num_states: int = 2,
    num_flows: int = 1,
) -> ExplorationResult:
    states = {}
    for i in range(num_states):
        sid = f"state-{i}"
        states[sid] = PageState(
            state_id=sid,
            url=f"https://example.com/page{i}",
            title=f"Page {i}",
            fingerprint=f"fp-{i}",
            depth=i,
            dom_structure_hash=f"dom-{i}",
            visible_text_hash=f"text-{i}",
            form_state_hash=f"form-{i}",
        )

    actions = {
        "act-0": Action(
            action_id="act-0",
            action_type=ActionType.CLICK,
            target_selector="button#go",
            label="Click go",
        ),
    }

    results = [
        ActionResult(
            action_id="act-0",
            source_state_id="state-0",
            target_state_id="state-1" if num_states > 1 else "state-0",
            outcome=OutcomeType.NAVIGATION,
            duration_ms=100.0,
            url_before="https://example.com/page0",
            url_after="https://example.com/page1",
        ),
    ]

    flows = [
        Flow(
            flow_id=f"flow-{i}",
            name=f"Flow {i}",
            description=f"Test flow {i}",
            state_ids=list(states.keys()),
            action_ids=list(actions.keys()),
            outcomes=[OutcomeType.NAVIGATION],
            depth=1,
        )
        for i in range(num_flows)
    ]

    return ExplorationResult(
        config={"start_url": "https://example.com"},
        started_at="2025-01-01T00:00:00Z",
        finished_at="2025-01-01T00:01:00Z",
        duration_seconds=60.0,
        states=states,
        actions=actions,
        results=results,
        flows=flows,
        stats={"total_states": num_states},
    )


class TestGenerateMarkdownReport:

    def test_generates_file(self, tmp_path: Path):
        result = _make_result()
        output = str(tmp_path / "report.md")
        generate_markdown_report(result, output)
        assert Path(output).exists()

    def test_contains_summary_table(self, tmp_path: Path):
        result = _make_result()
        output = str(tmp_path / "report.md")
        generate_markdown_report(result, output)
        content = Path(output).read_text()
        assert "## Summary" in content
        assert "| Start URL | https://example.com |" in content
        assert "| States discovered | 2 |" in content

    def test_contains_outcome_breakdown(self, tmp_path: Path):
        result = _make_result()
        output = str(tmp_path / "report.md")
        generate_markdown_report(result, output)
        content = Path(output).read_text()
        assert "## Outcome Breakdown" in content
        assert "navigation" in content

    def test_contains_flows(self, tmp_path: Path):
        result = _make_result(num_flows=2)
        output = str(tmp_path / "report.md")
        generate_markdown_report(result, output)
        content = Path(output).read_text()
        assert "## Flows" in content
        assert "Flow 0" in content
        assert "Flow 1" in content

    def test_contains_coverage(self, tmp_path: Path):
        result = _make_result()
        output = str(tmp_path / "report.md")
        generate_markdown_report(result, output)
        content = Path(output).read_text()
        assert "## Coverage" in content
        assert "Page coverage:" in content
        assert "Action coverage:" in content

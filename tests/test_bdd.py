"""Tests for BDD output generation."""

import tempfile
from pathlib import Path


from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.codegen.bdd import generate_feature_file, generate_markdown_report
from flowscout.discovery.actions import OutcomeType


def _make_result(flows: list[Flow] | None = None) -> ExplorationResult:
    return ExplorationResult(
        config={"start_url": "https://example.com"},
        started_at="2025-01-01T00:00:00Z",
        finished_at="2025-01-01T00:01:00Z",
        duration_seconds=60.0,
        states={},
        actions={},
        results=[],
        flows=flows or [],
    )


class TestGenerateFeatureFile:
    def test_creates_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "test.feature")
            result = generate_feature_file(_make_result(), path)
            assert Path(result).exists()

    def test_feature_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "test.feature")
            generate_feature_file(_make_result(), path)
            content = Path(path).read_text()
            assert "Feature:" in content
            assert "example.com" in content

    def test_flow_without_narrative(self) -> None:
        flow = Flow(
            flow_id="f1",
            name="Test Flow",
            description="Test",
            state_ids=["s1", "s2"],
            action_ids=["a1"],
            outcomes=[OutcomeType.NAVIGATION],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "test.feature")
            generate_feature_file(_make_result([flow]), path)
            content = Path(path).read_text()
            assert "Scenario: Test Flow" in content
            assert "Given" in content

    def test_valid_gherkin_structure(self) -> None:
        flow = Flow(
            flow_id="f1",
            name="Test Flow",
            description="Test",
            state_ids=["s1"],
            action_ids=[],
            outcomes=[],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "test.feature")
            generate_feature_file(_make_result([flow]), path)
            content = Path(path).read_text()
            assert content.startswith("Feature:")
            scenario_lines = [
                line for line in content.split("\n") if "Scenario:" in line
            ]
            assert len(scenario_lines) >= 1
            assert scenario_lines[0].startswith("  Scenario:")


class TestGenerateMarkdownReport:
    def test_creates_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "report.md")
            result = generate_markdown_report(_make_result(), path)
            assert Path(result).exists()

    def test_summary_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "report.md")
            generate_markdown_report(_make_result(), path)
            content = Path(path).read_text()
            assert "# Exploration Report" in content
            assert "| Metric | Value |" in content
            assert "States" in content
            assert "Passed" in content
            assert "Failed" in content

    def test_per_journey_sections(self) -> None:
        flow = Flow(
            flow_id="f1",
            name="Login Flow",
            description="Test login",
            state_ids=["s1", "s2"],
            action_ids=["a1"],
            outcomes=[OutcomeType.NAVIGATION],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "report.md")
            generate_markdown_report(_make_result([flow]), path)
            content = Path(path).read_text()
            assert "## Login Flow" in content

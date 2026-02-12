"""Tests for JUnit XML export."""

from __future__ import annotations

import xml.etree.ElementTree as ET  # nosec B405 - parsing our own generated XML in tests
from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.reporting.junit_export import generate_junit_report


def _make_result(
    *,
    num_flows: int = 2,
    verdicts: list[str] | None = None,
) -> ExplorationResult:
    states = {
        "s0": PageState(
            state_id="s0",
            url="https://example.com",
            title="Home",
            fingerprint="fp-0",
            depth=0,
            dom_structure_hash="dom-0",
            visible_text_hash="text-0",
            form_state_hash="form-0",
        ),
    }

    actions = {
        "a0": Action(
            action_id="a0",
            action_type=ActionType.CLICK,
            target_selector="button#go",
            label="Click go",
        ),
    }

    results = [
        ActionResult(
            action_id="a0",
            source_state_id="s0",
            target_state_id="s0",
            outcome=OutcomeType.NO_CHANGE,
            duration_ms=50.0,
            url_before="https://example.com",
            url_after="https://example.com",
        ),
    ]

    if verdicts is None:
        verdicts = ["pass"] * num_flows

    flows = []
    for i in range(num_flows):
        v = verdicts[i] if i < len(verdicts) else "pass"
        outcomes = [OutcomeType.NO_CHANGE]
        is_stable = True
        if v == "fail":
            outcomes = [OutcomeType.TIMEOUT]
            is_stable = False
        elif v == "warn":
            outcomes = [OutcomeType.NO_CHANGE]
            is_stable = False

        flow = Flow(
            flow_id=f"flow-{i}",
            name=f"Flow {i}",
            description=f"Test flow {i}",
            state_ids=["s0"],
            action_ids=["a0"],
            outcomes=outcomes,
            depth=1,
            stability_score=0.95 if is_stable else 0.45,
            is_stable=is_stable,
        )
        flows.append(flow)

    return ExplorationResult(
        config={"start_url": "https://example.com"},
        started_at="2025-01-01T00:00:00Z",
        finished_at="2025-01-01T00:01:00Z",
        duration_seconds=60.0,
        states=states,
        actions=actions,
        results=results,
        flows=flows,
        stats={},
    )


class TestGenerateJunitReport:
    def test_generates_file(self, tmp_path: Path) -> None:
        result = _make_result()
        output = str(tmp_path / "junit.xml")
        generate_junit_report(result, output)
        assert Path(output).exists()

    def test_valid_xml(self, tmp_path: Path) -> None:
        result = _make_result()
        output = str(tmp_path / "junit.xml")
        generate_junit_report(result, output)
        # Parsing our own generated JUnit XML, not untrusted input
        # nosemgrep: python.lang.security.use-defused-xml-parse.use-defused-xml-parse
        tree = ET.parse(output)  # nosec B314
        root = tree.getroot()
        assert root.tag == "testsuites"

    def test_test_count_matches(self, tmp_path: Path) -> None:
        result = _make_result(num_flows=3)
        output = str(tmp_path / "junit.xml")
        generate_junit_report(result, output)
        # Parsing our own generated JUnit XML, not untrusted input
        # nosemgrep: python.lang.security.use-defused-xml-parse.use-defused-xml-parse
        tree = ET.parse(output)  # nosec B314
        root = tree.getroot()
        assert root.get("tests") == "3"

    def test_failures_counted(self, tmp_path: Path) -> None:
        result = _make_result(num_flows=3, verdicts=["pass", "fail", "pass"])
        output = str(tmp_path / "junit.xml")
        generate_junit_report(result, output)
        # Parsing our own generated JUnit XML, not untrusted input
        # nosemgrep: python.lang.security.use-defused-xml-parse.use-defused-xml-parse
        tree = ET.parse(output)  # nosec B314
        root = tree.getroot()
        assert root.get("failures") == "1"

    def test_failure_element_present(self, tmp_path: Path) -> None:
        result = _make_result(num_flows=1, verdicts=["fail"])
        output = str(tmp_path / "junit.xml")
        generate_junit_report(result, output)
        # Parsing our own generated JUnit XML, not untrusted input
        # nosemgrep: python.lang.security.use-defused-xml-parse.use-defused-xml-parse
        tree = ET.parse(output)  # nosec B314
        root = tree.getroot()
        failures = root.findall(".//failure")
        assert len(failures) == 1

    def test_pass_has_no_failure_element(self, tmp_path: Path) -> None:
        result = _make_result(num_flows=1, verdicts=["pass"])
        output = str(tmp_path / "junit.xml")
        generate_junit_report(result, output)
        # Parsing our own generated JUnit XML, not untrusted input
        # nosemgrep: python.lang.security.use-defused-xml-parse.use-defused-xml-parse
        tree = ET.parse(output)  # nosec B314
        root = tree.getroot()
        failures = root.findall(".//failure")
        assert len(failures) == 0

    def test_xml_declaration_present(self, tmp_path: Path) -> None:
        result = _make_result()
        output = str(tmp_path / "junit.xml")
        generate_junit_report(result, output)
        content = Path(output).read_text()
        assert content.startswith("<?xml")

"""Tests for flow-based playwright test code generation."""

import tempfile
from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.codegen.playwright_tests import generate_test_suite
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType


def _make_state(state_id: str, url: str, *, title: str) -> PageState:
    return PageState(
        state_id=state_id,
        url=url,
        title=title,
        fingerprint=f"{state_id * 6}fingerprint",
        depth=0,
        dom_structure_hash="dom",
        visible_text_hash="text",
        form_state_hash="form",
    )


def _build_result(*, stability: float, reason: str) -> ExplorationResult:
    flow = Flow(
        flow_id="flow-1",
        name="Home to target",
        description="Click CTA",
        state_ids=["s1", "s2"],
        action_ids=["a1"],
        outcomes=[OutcomeType.NAVIGATION],
        depth=1,
    )
    return ExplorationResult(
        config={"start_url": "https://example.com"},
        states={
            "s1": _make_state("s1", "https://example.com", title="Home"),
            "s2": _make_state("s2", "https://example.com/target", title="Target"),
        },
        actions={
            "a1": Action(
                action_id="a1",
                action_type=ActionType.CLICK,
                target_selector="#cta",
                label="Click CTA",
            )
        },
        results=[
            ActionResult(
                action_id="a1",
                source_state_id="s1",
                target_state_id="s2",
                outcome=OutcomeType.NAVIGATION,
                url_after="https://example.com/target",
                stability_score=stability,
                observation_notes=reason,
            )
        ],
        flows=[flow],
    )


def test_pytest_codegen_marks_low_confidence_transition() -> None:
    result = _build_result(
        stability=0.55,
        reason="No visible transition detected",
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "tests.py"
        generate_test_suite(result, str(output), framework="pytest")
        code = output.read_text()

    assert "Stability: score=0.55 (55%)" in code
    assert "reason=No visible transition detected" in code
    assert "Stability flag: LOW_STABILITY transition" in code
    assert "Trace: action_id=a1 | edge=s1->s2 | outcome=navigation" in code


def test_pytest_codegen_does_not_flag_high_confidence_transition() -> None:
    result = _build_result(
        stability=0.95,
        reason="URL changed and navigation completed",
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "tests.py"
        generate_test_suite(result, str(output), framework="pytest")
        code = output.read_text()

    assert "Stability: score=0.95 (95%)" in code
    assert "reason=URL changed and navigation completed" in code
    assert "Stability flag: LOW_STABILITY transition" not in code
    assert "Trace: action_id=a1 | edge=s1->s2 | outcome=navigation" in code


def test_playwright_codegen_marks_low_confidence_transition() -> None:
    result = _build_result(
        stability=0.3,
        reason="Action timed out",
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "tests.spec.ts"
        generate_test_suite(result, str(output), framework="playwright")
        code = output.read_text()

    assert "// Stability: score=0.30 (30%)" in code
    assert "reason=Action timed out" in code
    assert "// Stability flag: LOW_STABILITY transition" in code
    assert "// Trace: action_id=a1 | edge=s1->s2 | outcome=navigation" in code

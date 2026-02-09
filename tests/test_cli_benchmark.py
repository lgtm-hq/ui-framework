"""Tests for benchmark metric aggregation."""

from flowscout.analysis.graph import ExplorationResult
from flowscout.cli import _compute_benchmark_metrics
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType


def _make_state(state_id: str, url: str) -> PageState:
    return PageState(
        state_id=state_id,
        url=url,
        title=state_id,
        fingerprint=f"{state_id * 6}fingerprint",
        depth=0,
        dom_structure_hash="dom",
        visible_text_hash="text",
        form_state_hash="form",
    )


def test_compute_benchmark_metrics_counts_low_confidence_and_coverage() -> None:
    result = ExplorationResult(
        duration_seconds=42.5,
        states={
            "s1": _make_state("s1", "https://example.com"),
            "s2": _make_state("s2", "https://example.com/details"),
        },
        actions={
            "a1": Action(
                action_id="a1",
                action_type=ActionType.CLICK,
                target_selector="#go",
                label="Go",
            ),
            "a2": Action(
                action_id="a2",
                action_type=ActionType.CLICK,
                target_selector="#stay",
                label="Stay",
            ),
            "a3": Action(
                action_id="a3",
                action_type=ActionType.CLICK,
                target_selector="#unused",
                label="Unused",
            ),
        },
        results=[
            ActionResult(
                action_id="a1",
                source_state_id="s1",
                target_state_id="s2",
                outcome=OutcomeType.NAVIGATION,
                confidence=0.92,
            ),
            ActionResult(
                action_id="a2",
                source_state_id="s2",
                target_state_id="s2",
                outcome=OutcomeType.NO_CHANGE,
                confidence=0.4,
            ),
        ],
        stats={
            "total_states": 5,
            "total_actions_executed": 2,
            "total_unique_actions": 3,
        },
    )

    metrics = _compute_benchmark_metrics(result, low_confidence_threshold=0.6)

    assert metrics["duration_seconds"] == 42.5
    assert metrics["total_states"] == 5
    assert metrics["total_actions_executed"] == 2
    assert metrics["total_unique_actions"] == 3
    assert metrics["page_coverage_pct"] == 100
    assert metrics["action_coverage_pct"] == 67
    assert metrics["confidence_sample_count"] == 2
    assert metrics["low_confidence_transitions"] == 1
    assert metrics["avg_transition_confidence"] == 0.66
    assert metrics["coverage_target_met"] is True
    assert metrics["interactive_elements"] == 0
    assert metrics["non_interactive_elements"] == 0
    assert metrics["total_catalog_elements"] == 0
    assert metrics["interactive_mix_pct"] == 0


def test_compute_benchmark_metrics_handles_empty_results() -> None:
    result = ExplorationResult(
        duration_seconds=1.0,
        states={"s1": _make_state("s1", "https://example.com")},
        actions={
            "a1": Action(
                action_id="a1",
                action_type=ActionType.CLICK,
                target_selector="#go",
                label="Go",
            )
        },
        results=[],
    )

    metrics = _compute_benchmark_metrics(result, low_confidence_threshold=0.6)

    assert metrics["page_coverage_pct"] == 0
    assert metrics["action_coverage_pct"] == 0
    assert metrics["confidence_sample_count"] == 0
    assert metrics["low_confidence_transitions"] == 0
    assert metrics["avg_transition_confidence"] == 0.0
    assert metrics["coverage_target_met"] is False
    assert metrics["interactive_elements"] == 0
    assert metrics["non_interactive_elements"] == 0
    assert metrics["total_catalog_elements"] == 0
    assert metrics["interactive_mix_pct"] == 0


def test_compute_benchmark_metrics_ignores_missing_legacy_confidence() -> None:
    result = ExplorationResult(
        duration_seconds=3.0,
        states={
            "s1": _make_state("s1", "https://example.com"),
            "s2": _make_state("s2", "https://example.com/next"),
        },
        actions={
            "a1": Action(
                action_id="a1",
                action_type=ActionType.CLICK,
                target_selector="#go",
                label="Go",
            )
        },
        results=[
            ActionResult(
                action_id="a1",
                source_state_id="s1",
                target_state_id="s2",
                outcome=OutcomeType.NAVIGATION,
                confidence=0.0,
                confidence_reason="",
            )
        ],
    )

    metrics = _compute_benchmark_metrics(result, low_confidence_threshold=0.6)

    assert metrics["confidence_sample_count"] == 0
    assert metrics["low_confidence_transitions"] == 0
    assert metrics["avg_transition_confidence"] == 0.0


def test_compute_benchmark_metrics_includes_element_inventory() -> None:
    result = ExplorationResult(
        duration_seconds=2.0,
        states={"s1": _make_state("s1", "https://example.com")},
        actions={
            "a1": Action(
                action_id="a1",
                action_type=ActionType.CLICK,
                target_selector="#go",
                label="Go",
            )
        },
        results=[
            ActionResult(
                action_id="a1",
                source_state_id="s1",
                target_state_id="s1",
                outcome=OutcomeType.NO_CHANGE,
                confidence=0.7,
            )
        ],
        element_inventory={
            "interactive_elements": 7,
            "non_interactive_elements": 3,
            "total_elements": 10,
        },
    )

    metrics = _compute_benchmark_metrics(result, low_confidence_threshold=0.6)

    assert metrics["interactive_elements"] == 7
    assert metrics["non_interactive_elements"] == 3
    assert metrics["total_catalog_elements"] == 10
    assert metrics["interactive_mix_pct"] == 70

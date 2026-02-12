"""Tests for observation-first stability modeling."""

from __future__ import annotations

from flowscout.analysis.verdict import ObservationComputer, ObservationResult
from flowscout.discovery.actions import OutcomeType


def test_compute_observation_returns_stability_score_and_notes() -> None:
    """Navigation outcomes should produce high stability observations."""
    computer = ObservationComputer()

    observation = computer.compute_observation(OutcomeType.NAVIGATION)

    assert observation.outcome == OutcomeType.NAVIGATION
    assert observation.stability_score == 0.95
    assert "navigation" in observation.observation_notes.lower()


def test_compute_observation_handles_invalid_scenario_validation() -> None:
    """Invalid-input validation feedback should be treated as stable."""
    computer = ObservationComputer()

    observation = computer.compute_observation(
        OutcomeType.VALIDATION_ERROR,
        is_invalid_scenario=True,
    )

    assert observation.stability_score >= 0.9
    assert "expected" in observation.observation_notes.lower()


def test_summarize_flow_marks_unstable_on_severe_outcomes() -> None:
    """Timeouts and similar severe outcomes should force flow instability."""
    computer = ObservationComputer()

    summary = computer.summarize_flow(
        [
            ObservationResult(
                outcome=OutcomeType.DOM_CHANGE,
                stability_score=0.9,
            ),
            ObservationResult(
                outcome=OutcomeType.TIMEOUT,
                stability_score=0.2,
            ),
        ]
    )

    assert summary.stability_score == 0.55
    assert summary.is_stable is False

"""Tests for stability observation computation."""

from __future__ import annotations

from flowscout.analysis.verdict import ObservationComputer, ObservationResult
from flowscout.discovery.actions import OutcomeType


def test_network_error_has_low_stability() -> None:
    computer = ObservationComputer()

    observation = computer.compute_observation(OutcomeType.NETWORK_ERROR)

    assert observation.stability_score <= 0.25
    assert "error" in observation.observation_notes.lower()


def test_invalid_navigation_is_penalized() -> None:
    computer = ObservationComputer()

    observation = computer.compute_observation(
        OutcomeType.NAVIGATION,
        is_invalid_scenario=True,
    )

    assert observation.stability_score <= 0.25
    assert "unexpectedly" in observation.observation_notes.lower()


def test_flow_summary_defaults_for_empty_input() -> None:
    computer = ObservationComputer()

    summary = computer.summarize_flow([])

    assert summary.stability_score == 0.0
    assert summary.is_stable is False


def test_flow_summary_is_stable_for_consistent_high_scores() -> None:
    computer = ObservationComputer()

    summary = computer.summarize_flow(
        [
            ObservationResult(
                outcome=OutcomeType.NAVIGATION,
                stability_score=0.95,
            ),
            ObservationResult(
                outcome=OutcomeType.DOM_CHANGE,
                stability_score=0.85,
            ),
        ]
    )

    assert summary.stability_score >= 0.9
    assert summary.is_stable is True

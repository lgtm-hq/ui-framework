"""Tests for transition confidence scoring."""

from flowscout.core.navigator import Navigator
from flowscout.discovery.actions import OutcomeType


def test_navigation_has_high_confidence() -> None:
    score, reason = Navigator._compute_transition_confidence(OutcomeType.NAVIGATION)
    assert score >= 0.9
    assert "navigation" in reason.lower()


def test_timeout_has_low_confidence() -> None:
    score, reason = Navigator._compute_transition_confidence(OutcomeType.TIMEOUT)
    assert score <= 0.3
    assert "timed out" in reason.lower()


def test_no_change_has_mid_confidence() -> None:
    score, _ = Navigator._compute_transition_confidence(OutcomeType.NO_CHANGE)
    assert 0.5 <= score <= 0.6

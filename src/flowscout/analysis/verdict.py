"""Observation model — stability-focused outcome summaries."""

from __future__ import annotations

from pydantic import BaseModel, Field

from flowscout.discovery.actions import OutcomeType


class ObservationResult(BaseModel):
    """Outcome observation for a single executed action."""

    outcome: OutcomeType
    stability_score: float
    observation_notes: str = ""


class FlowSummary(BaseModel):
    """Aggregate stability view for a flow."""

    outcomes: list[OutcomeType] = Field(default_factory=list)
    stability_score: float = 0.0
    is_stable: bool = False


class ObservationComputer:
    """Computes stability-focused observations for actions and flows."""

    _OUTCOME_STABILITY: dict[OutcomeType, tuple[float, str]] = {
        OutcomeType.NAVIGATION: (0.95, "URL changed and navigation completed"),
        OutcomeType.DOM_CHANGE: (0.85, "DOM changed after interaction"),
        OutcomeType.VALIDATION_ERROR: (0.8, "Validation feedback detected"),
        OutcomeType.VISUAL_CHANGE: (0.7, "Visual state changed"),
        OutcomeType.NO_CHANGE: (0.55, "No visible transition detected"),
        OutcomeType.TIMEOUT: (0.3, "Action timed out"),
        OutcomeType.NETWORK_ERROR: (0.25, "HTTP/network errors detected"),
        OutcomeType.CONSOLE_ERROR: (0.25, "Console errors detected"),
        OutcomeType.EXCEPTION: (0.2, "Action raised an exception"),
    }
    _FLOW_STABLE_THRESHOLD = 0.7

    def compute_observation(
        self,
        outcome: OutcomeType,
        *,
        observed_detail: str = "",
        is_invalid_scenario: bool = False,
    ) -> ObservationResult:
        """Build a step observation from an outcome."""
        base_score, base_note = self._OUTCOME_STABILITY.get(
            outcome,
            (0.5, "Unknown outcome"),
        )
        if is_invalid_scenario:
            if outcome == OutcomeType.VALIDATION_ERROR:
                base_score = max(base_score, 0.9)
                base_note = "Form rejected invalid input as expected"
            elif outcome == OutcomeType.NAVIGATION:
                base_score = min(base_score, 0.25)
                base_note = "Form accepted invalid input unexpectedly"

        note = base_note
        detail = observed_detail.strip()
        if detail:
            note = f"{base_note}: {detail}"

        return ObservationResult(
            outcome=outcome,
            stability_score=base_score,
            observation_notes=note,
        )

    def summarize_flow(
        self,
        observations: list[ObservationResult],
    ) -> FlowSummary:
        """Aggregate per-step observations into a flow-level summary."""
        if not observations:
            return FlowSummary()
        outcomes = [observation.outcome for observation in observations]
        average_stability = sum(
            observation.stability_score for observation in observations
        ) / len(observations)
        has_severe_outcome = any(
            outcome
            in (OutcomeType.NETWORK_ERROR, OutcomeType.TIMEOUT, OutcomeType.EXCEPTION)
            for outcome in outcomes
        )
        is_stable = (average_stability >= self._FLOW_STABLE_THRESHOLD) and (
            not has_severe_outcome
        )
        return FlowSummary(
            outcomes=outcomes,
            stability_score=round(average_stability, 3),
            is_stable=is_stable,
        )

"""Verdict system — compares action intent to observed outcome."""

from __future__ import annotations

from enum import StrEnum, auto

from pydantic import BaseModel, Field

from flowscout.discovery.actions import OutcomeType
from flowscout.discovery.intent import ActionIntent, IntentClass


class Verdict(StrEnum):
    PASS = auto()
    FAIL = auto()
    WARN = auto()
    INCONCLUSIVE = auto()


class StepVerdict(BaseModel):
    """Verdict for a single action step."""

    verdict: Verdict
    reason: str
    expected: str = ""
    actual: str = ""


class JourneyVerdict(BaseModel):
    """Aggregate verdict for a complete flow/journey."""

    verdict: Verdict
    summary: str
    step_verdicts: list[StepVerdict] = Field(default_factory=list)
    pass_count: int = 0
    fail_count: int = 0
    warn_count: int = 0


class VerdictComputer:
    """Computes pass/fail/warn verdicts by comparing intent to outcome."""

    def compute_step_verdict(
        self,
        outcome: OutcomeType,
        intent: ActionIntent | None,
        *,
        is_invalid_scenario: bool = False,
        observed_detail: str = "",
    ) -> StepVerdict:
        """Compute verdict for a single action result."""
        detail_suffix = f": {observed_detail}" if observed_detail else ""

        # Always-fail outcomes
        if outcome == OutcomeType.NETWORK_ERROR:
            return StepVerdict(
                verdict=Verdict.FAIL,
                reason="Network error occurred",
                expected=intent.expected_effect if intent else "Successful action",
                actual=f"Network error (4xx/5xx response){detail_suffix}",
            )

        if outcome == OutcomeType.EXCEPTION:
            return StepVerdict(
                verdict=Verdict.FAIL,
                reason="Exception thrown during action",
                expected=intent.expected_effect if intent else "Successful action",
                actual=f"JavaScript exception or browser error{detail_suffix}",
            )

        # Invalid form scenario special handling
        if is_invalid_scenario:
            if outcome == OutcomeType.VALIDATION_ERROR:
                return StepVerdict(
                    verdict=Verdict.PASS,
                    reason="Form correctly rejected invalid input",
                    expected="Validation errors for invalid input",
                    actual=f"Validation error displayed{detail_suffix}",
                )
            if outcome == OutcomeType.NAVIGATION:
                return StepVerdict(
                    verdict=Verdict.FAIL,
                    reason="Form accepted invalid input (should have shown validation error)",
                    expected="Validation errors for invalid input",
                    actual="Page navigated (form was accepted)",
                )

        # No intent — limited analysis
        if intent is None:
            if outcome in (OutcomeType.TIMEOUT,):
                return StepVerdict(
                    verdict=Verdict.WARN,
                    reason="Action timed out",
                    expected="Unknown",
                    actual="Timeout",
                )
            return StepVerdict(
                verdict=Verdict.INCONCLUSIVE,
                reason="No intent available for comparison",
                expected="Unknown",
                actual=outcome.value,
            )

        expected = intent.expected_effect
        actual = self._actual_outcome_text(outcome, observed_detail=observed_detail)

        # Console error is always a warning
        if outcome == OutcomeType.CONSOLE_ERROR:
            return StepVerdict(
                verdict=Verdict.WARN,
                reason="Console error detected during action",
                expected=expected,
                actual="Console error",
            )

        # Intent-based rules
        ic = intent.intent_class

        if ic == IntentClass.NAVIGATE:
            if outcome == OutcomeType.NAVIGATION:
                return StepVerdict(
                    verdict=Verdict.PASS,
                    reason="Navigation successful",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.TIMEOUT:
                return StepVerdict(
                    verdict=Verdict.FAIL,
                    reason="Navigation timed out",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.DOM_CHANGE:
                return StepVerdict(
                    verdict=Verdict.WARN,
                    reason="DOM changed but URL did not change",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.NO_CHANGE:
                return StepVerdict(
                    verdict=Verdict.WARN,
                    reason="No observable change after navigation attempt",
                    expected=expected,
                    actual=actual,
                )

        if ic == IntentClass.INPUT:
            if outcome in (OutcomeType.DOM_CHANGE, OutcomeType.NO_CHANGE):
                return StepVerdict(
                    verdict=Verdict.PASS,
                    reason="Input accepted",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.VALIDATION_ERROR:
                return StepVerdict(
                    verdict=Verdict.WARN,
                    reason="Validation error on input",
                    expected=expected,
                    actual=actual,
                )

        if ic == IntentClass.SUBMIT:
            if outcome in (OutcomeType.NAVIGATION, OutcomeType.DOM_CHANGE):
                return StepVerdict(
                    verdict=Verdict.PASS,
                    reason="Form submission processed",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.VALIDATION_ERROR:
                return StepVerdict(
                    verdict=Verdict.WARN,
                    reason="Form validation error",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.TIMEOUT:
                return StepVerdict(
                    verdict=Verdict.FAIL,
                    reason="Form submission timed out",
                    expected=expected,
                    actual=actual,
                )

        if ic == IntentClass.TOGGLE:
            if outcome == OutcomeType.DOM_CHANGE:
                return StepVerdict(
                    verdict=Verdict.PASS,
                    reason="Toggle changed state",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.NO_CHANGE:
                return StepVerdict(
                    verdict=Verdict.WARN,
                    reason="Toggle did not visibly change",
                    expected=expected,
                    actual=actual,
                )

        if ic == IntentClass.REVEAL:
            if outcome == OutcomeType.DOM_CHANGE:
                return StepVerdict(
                    verdict=Verdict.PASS,
                    reason="Content revealed",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.TIMEOUT:
                return StepVerdict(
                    verdict=Verdict.FAIL,
                    reason="Element not interactable (timeout)",
                    expected=expected,
                    actual=actual,
                )

        if ic == IntentClass.SELECT:
            if outcome in (OutcomeType.DOM_CHANGE, OutcomeType.NAVIGATION):
                return StepVerdict(
                    verdict=Verdict.PASS,
                    reason="Selection applied",
                    expected=expected,
                    actual=actual,
                )
            if outcome == OutcomeType.NO_CHANGE:
                return StepVerdict(
                    verdict=Verdict.WARN,
                    reason="Selection had no visible effect",
                    expected=expected,
                    actual=actual,
                )

        # Fallback
        return StepVerdict(
            verdict=Verdict.INCONCLUSIVE,
            reason=f"Cannot determine verdict for {ic.value} intent with {outcome.value} outcome",
            expected=expected,
            actual=actual,
        )

    @staticmethod
    def _actual_outcome_text(
        outcome: OutcomeType,
        *,
        observed_detail: str = "",
    ) -> str:
        """Return human-readable observed result text."""
        detail_suffix = f": {observed_detail}" if observed_detail else ""
        match outcome:
            case OutcomeType.NAVIGATION:
                return "Page navigation occurred"
            case OutcomeType.DOM_CHANGE:
                return "Visible DOM/content change observed"
            case OutcomeType.NO_CHANGE:
                return "No visible UI change observed"
            case OutcomeType.VALIDATION_ERROR:
                return f"Validation error was shown{detail_suffix}"
            case OutcomeType.NETWORK_ERROR:
                return f"Network error response was observed{detail_suffix}"
            case OutcomeType.CONSOLE_ERROR:
                return f"Browser console error was detected{detail_suffix}"
            case OutcomeType.TIMEOUT:
                return "Action timed out"
            case OutcomeType.EXCEPTION:
                return f"Exception occurred during action{detail_suffix}"
            case OutcomeType.VISUAL_CHANGE:
                return "Visual-only change observed"
        return outcome.value

    def compute_journey_verdict(
        self, step_verdicts: list[StepVerdict]
    ) -> JourneyVerdict:
        """Aggregate step verdicts into a journey-level verdict."""
        if not step_verdicts:
            return JourneyVerdict(
                verdict=Verdict.INCONCLUSIVE, summary="No steps to evaluate"
            )

        pass_count = sum(1 for sv in step_verdicts if sv.verdict == Verdict.PASS)
        fail_count = sum(1 for sv in step_verdicts if sv.verdict == Verdict.FAIL)
        warn_count = sum(1 for sv in step_verdicts if sv.verdict == Verdict.WARN)
        total = len(step_verdicts)

        if fail_count > 0:
            verdict = Verdict.FAIL
            summary = f"{fail_count} failure(s) out of {total} steps"
        elif warn_count > 0:
            verdict = Verdict.WARN
            summary = f"All steps passed but {warn_count} warning(s) detected"
        else:
            verdict = Verdict.PASS
            summary = f"All {total} steps passed"

        return JourneyVerdict(
            verdict=verdict,
            summary=summary,
            step_verdicts=step_verdicts,
            pass_count=pass_count,
            fail_count=fail_count,
            warn_count=warn_count,
        )

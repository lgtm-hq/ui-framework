"""Tests for the verdict system."""

import pytest

from flowscout.analysis.verdict import (
    StepVerdict,
    Verdict,
    VerdictComputer,
)
from flowscout.discovery.actions import OutcomeType
from flowscout.discovery.intent import ActionIntent, IntentClass


@pytest.fixture
def computer():
    return VerdictComputer()


def _intent(cls: IntentClass, expected: str = "Test effect") -> ActionIntent:
    return ActionIntent(
        intent_class=cls,
        target_description="test element",
        expected_effect=expected,
    )


class TestStepVerdict:
    def test_network_error_always_fails(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NETWORK_ERROR, _intent(IntentClass.NAVIGATE)
        )
        assert sv.verdict == Verdict.FAIL

    def test_exception_always_fails(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.EXCEPTION, _intent(IntentClass.INPUT)
        )
        assert sv.verdict == Verdict.FAIL

    def test_exception_includes_observed_detail(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.EXCEPTION,
            _intent(IntentClass.INPUT),
            observed_detail="TimeoutError",
        )
        assert "TimeoutError" in sv.actual

    def test_invalid_scenario_validation_error_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.VALIDATION_ERROR,
            _intent(IntentClass.SUBMIT),
            is_invalid_scenario=True,
        )
        assert sv.verdict == Verdict.PASS

    def test_invalid_scenario_navigation_fails(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NAVIGATION,
            _intent(IntentClass.SUBMIT),
            is_invalid_scenario=True,
        )
        assert sv.verdict == Verdict.FAIL

    @pytest.mark.parametrize(
        ("outcome", "intent_class", "expected_verdict"),
        [
            # NAVIGATE intent
            (OutcomeType.NAVIGATION, IntentClass.NAVIGATE, Verdict.PASS),
            (OutcomeType.TIMEOUT, IntentClass.NAVIGATE, Verdict.FAIL),
            (OutcomeType.DOM_CHANGE, IntentClass.NAVIGATE, Verdict.WARN),
            (OutcomeType.NO_CHANGE, IntentClass.NAVIGATE, Verdict.WARN),
            (OutcomeType.CONSOLE_ERROR, IntentClass.NAVIGATE, Verdict.WARN),
            # INPUT intent
            (OutcomeType.DOM_CHANGE, IntentClass.INPUT, Verdict.PASS),
            (OutcomeType.NO_CHANGE, IntentClass.INPUT, Verdict.PASS),
            (OutcomeType.VALIDATION_ERROR, IntentClass.INPUT, Verdict.WARN),
            # SUBMIT intent
            (OutcomeType.NAVIGATION, IntentClass.SUBMIT, Verdict.PASS),
            (OutcomeType.DOM_CHANGE, IntentClass.SUBMIT, Verdict.PASS),
            (OutcomeType.VALIDATION_ERROR, IntentClass.SUBMIT, Verdict.WARN),
            (OutcomeType.TIMEOUT, IntentClass.SUBMIT, Verdict.FAIL),
            # TOGGLE intent
            (OutcomeType.DOM_CHANGE, IntentClass.TOGGLE, Verdict.PASS),
            (OutcomeType.NO_CHANGE, IntentClass.TOGGLE, Verdict.WARN),
            # REVEAL intent
            (OutcomeType.DOM_CHANGE, IntentClass.REVEAL, Verdict.PASS),
            (OutcomeType.TIMEOUT, IntentClass.REVEAL, Verdict.FAIL),
            # SELECT intent
            (OutcomeType.DOM_CHANGE, IntentClass.SELECT, Verdict.PASS),
            (OutcomeType.NAVIGATION, IntentClass.SELECT, Verdict.PASS),
            (OutcomeType.NO_CHANGE, IntentClass.SELECT, Verdict.WARN),
        ],
        ids=lambda val: val.value if hasattr(val, "value") else str(val),
    )
    def test_intent_outcome_verdict(self, computer, outcome, intent_class, expected_verdict):
        sv = computer.compute_step_verdict(outcome, _intent(intent_class))
        assert sv.verdict == expected_verdict

    def test_validation_error_includes_observed_detail(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.VALIDATION_ERROR,
            _intent(IntentClass.SUBMIT),
            observed_detail="Username is required",
        )
        assert "Username is required" in sv.actual

    def test_no_intent_timeout_warns(self, computer):
        sv = computer.compute_step_verdict(OutcomeType.TIMEOUT, None)
        assert sv.verdict == Verdict.WARN

    def test_no_intent_other_inconclusive(self, computer):
        sv = computer.compute_step_verdict(OutcomeType.DOM_CHANGE, None)
        assert sv.verdict == Verdict.INCONCLUSIVE

    def test_fallback_inconclusive(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.VISUAL_CHANGE, _intent(IntentClass.NAVIGATE)
        )
        assert sv.verdict == Verdict.INCONCLUSIVE


class TestJourneyVerdict:
    def test_all_pass(self, computer):
        steps = [
            StepVerdict(verdict=Verdict.PASS, reason="ok"),
            StepVerdict(verdict=Verdict.PASS, reason="ok"),
        ]
        jv = computer.compute_journey_verdict(steps)
        assert jv.verdict == Verdict.PASS
        assert jv.pass_count == 2
        assert jv.fail_count == 0

    def test_any_fail_means_fail(self, computer):
        steps = [
            StepVerdict(verdict=Verdict.PASS, reason="ok"),
            StepVerdict(verdict=Verdict.FAIL, reason="broken"),
        ]
        jv = computer.compute_journey_verdict(steps)
        assert jv.verdict == Verdict.FAIL
        assert jv.fail_count == 1

    def test_warn_without_fail_means_warn(self, computer):
        steps = [
            StepVerdict(verdict=Verdict.PASS, reason="ok"),
            StepVerdict(verdict=Verdict.WARN, reason="hmm"),
        ]
        jv = computer.compute_journey_verdict(steps)
        assert jv.verdict == Verdict.WARN
        assert jv.warn_count == 1

    def test_empty_steps_inconclusive(self, computer):
        jv = computer.compute_journey_verdict([])
        assert jv.verdict == Verdict.INCONCLUSIVE

    def test_fail_takes_priority_over_warn(self, computer):
        steps = [
            StepVerdict(verdict=Verdict.WARN, reason="hmm"),
            StepVerdict(verdict=Verdict.FAIL, reason="broken"),
            StepVerdict(verdict=Verdict.PASS, reason="ok"),
        ]
        jv = computer.compute_journey_verdict(steps)
        assert jv.verdict == Verdict.FAIL
        assert jv.pass_count == 1
        assert jv.fail_count == 1
        assert jv.warn_count == 1

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

    def test_navigate_navigation_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NAVIGATION, _intent(IntentClass.NAVIGATE)
        )
        assert sv.verdict == Verdict.PASS

    def test_navigate_timeout_fails(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.TIMEOUT, _intent(IntentClass.NAVIGATE)
        )
        assert sv.verdict == Verdict.FAIL

    def test_navigate_dom_change_warns(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.DOM_CHANGE, _intent(IntentClass.NAVIGATE)
        )
        assert sv.verdict == Verdict.WARN

    def test_navigate_no_change_warns(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NO_CHANGE, _intent(IntentClass.NAVIGATE)
        )
        assert sv.verdict == Verdict.WARN

    def test_input_dom_change_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.DOM_CHANGE, _intent(IntentClass.INPUT)
        )
        assert sv.verdict == Verdict.PASS

    def test_input_no_change_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NO_CHANGE, _intent(IntentClass.INPUT)
        )
        assert sv.verdict == Verdict.PASS

    def test_input_validation_error_warns(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.VALIDATION_ERROR, _intent(IntentClass.INPUT)
        )
        assert sv.verdict == Verdict.WARN

    def test_submit_navigation_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NAVIGATION, _intent(IntentClass.SUBMIT)
        )
        assert sv.verdict == Verdict.PASS

    def test_submit_dom_change_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.DOM_CHANGE, _intent(IntentClass.SUBMIT)
        )
        assert sv.verdict == Verdict.PASS

    def test_submit_validation_error_warns(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.VALIDATION_ERROR, _intent(IntentClass.SUBMIT)
        )
        assert sv.verdict == Verdict.WARN

    def test_submit_timeout_fails(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.TIMEOUT, _intent(IntentClass.SUBMIT)
        )
        assert sv.verdict == Verdict.FAIL

    def test_toggle_dom_change_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.DOM_CHANGE, _intent(IntentClass.TOGGLE)
        )
        assert sv.verdict == Verdict.PASS

    def test_toggle_no_change_warns(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NO_CHANGE, _intent(IntentClass.TOGGLE)
        )
        assert sv.verdict == Verdict.WARN

    def test_reveal_dom_change_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.DOM_CHANGE, _intent(IntentClass.REVEAL)
        )
        assert sv.verdict == Verdict.PASS

    def test_reveal_timeout_fails(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.TIMEOUT, _intent(IntentClass.REVEAL)
        )
        assert sv.verdict == Verdict.FAIL

    def test_select_dom_change_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.DOM_CHANGE, _intent(IntentClass.SELECT)
        )
        assert sv.verdict == Verdict.PASS

    def test_select_navigation_passes(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NAVIGATION, _intent(IntentClass.SELECT)
        )
        assert sv.verdict == Verdict.PASS

    def test_select_no_change_warns(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.NO_CHANGE, _intent(IntentClass.SELECT)
        )
        assert sv.verdict == Verdict.WARN

    def test_console_error_warns(self, computer):
        sv = computer.compute_step_verdict(
            OutcomeType.CONSOLE_ERROR, _intent(IntentClass.NAVIGATE)
        )
        assert sv.verdict == Verdict.WARN

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

"""Tests for narrative generation."""

import pytest

from flowscout.analysis.narrative import FlowNarrative, NarrativeGenerator
from flowscout.analysis.verdict import StepVerdict, Verdict
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.discovery.intent import ActionIntent, IntentClass


@pytest.fixture
def generator():
    return NarrativeGenerator()


def _make_state(
    state_id: str = "s1", url: str = "https://example.com", title: str = "Example"
) -> PageState:
    return PageState(
        state_id=state_id,
        url=url,
        title=title,
        fingerprint=state_id * 6,
        depth=0,
        dom_structure_hash="dom",
        visible_text_hash="text",
        form_state_hash="form",
    )


def _make_action(
    action_type: ActionType = ActionType.CLICK, label: str = "Click: Login"
) -> Action:
    return Action(
        action_id="a1",
        action_type=action_type,
        target_selector="button",
        label=label,
    )


def _make_result(outcome: OutcomeType = OutcomeType.NAVIGATION) -> ActionResult:
    return ActionResult(
        action_id="a1",
        source_state_id="s1",
        target_state_id="s2",
        outcome=outcome,
        url_before="https://example.com",
        url_after="https://example.com/login",
    )


class TestNarrateStep:
    def test_click_description(self, generator):
        action = _make_action()
        result = _make_result()
        step = generator.narrate_step(
            action, result, _make_state(), _make_state("s2", title="Login"), 1
        )
        assert step.action_description == "Click the 'Login' element"
        assert step.step_number == 1

    def test_fill_description(self, generator):
        action = _make_action(ActionType.FILL, label="Fill: Username = 'Jane Doe'")
        action.value = "test@example.com"
        result = _make_result(OutcomeType.DOM_CHANGE)
        step = generator.narrate_step(action, result, _make_state(), _make_state(), 1)
        assert "Enter" in step.action_description
        assert "test@example.com" in step.action_description
        assert " = " not in step.action_description

    def test_submit_description(self, generator):
        action = _make_action(ActionType.SUBMIT_FORM, label="Submit form")
        result = _make_result(OutcomeType.NAVIGATION)
        step = generator.narrate_step(action, result, _make_state(), _make_state(), 1)
        assert "Submit" in step.action_description

    def test_gherkin_when_click(self, generator):
        action = _make_action()
        result = _make_result()
        step = generator.narrate_step(action, result, _make_state(), _make_state(), 1)
        assert step.gherkin_when.startswith("When I click")

    def test_gherkin_then_navigation(self, generator):
        result = _make_result(OutcomeType.NAVIGATION)
        step = generator.narrate_step(
            _make_action(),
            result,
            _make_state(),
            _make_state("s2", title="Dashboard"),
            1,
        )
        assert "navigate" in step.gherkin_then.lower()

    def test_gherkin_then_dom_change(self, generator):
        result = _make_result(OutcomeType.DOM_CHANGE)
        step = generator.narrate_step(
            _make_action(), result, _make_state(), _make_state(), 1
        )
        assert "update" in step.gherkin_then.lower()

    def test_gherkin_then_validation_error(self, generator):
        result = _make_result(OutcomeType.VALIDATION_ERROR)
        result.error_messages = ["Email is required"]
        step = generator.narrate_step(
            _make_action(), result, _make_state(), _make_state(), 1
        )
        assert "validation" in step.gherkin_then.lower()

    def test_verdict_attached(self, generator):
        sv = StepVerdict(verdict=Verdict.PASS, reason="ok")
        step = generator.narrate_step(
            _make_action(),
            _make_result(),
            _make_state(),
            _make_state(),
            1,
            step_verdict=sv,
        )
        assert step.verdict == Verdict.PASS

    def test_expected_from_intent(self, generator):
        intent = ActionIntent(
            intent_class=IntentClass.NAVIGATE,
            target_description="Login link",
            expected_effect="Navigate to login page",
        )
        step = generator.narrate_step(
            _make_action(),
            _make_result(),
            _make_state(),
            _make_state(),
            1,
            intent=intent,
        )
        assert step.expected == "Navigate to login page"


class TestNarrateFlow:
    def test_basic_flow(self, generator):
        actions = [_make_action()]
        results = [_make_result()]
        states = [_make_state(), _make_state("s2", title="Login")]
        narrative = generator.narrate_flow("Login Flow", actions, results, states)
        assert narrative.title == "Login Flow"
        assert len(narrative.steps) == 1
        assert "example.com" in narrative.precondition

    def test_conclusion_all_passed(self, generator):
        svs = [StepVerdict(verdict=Verdict.PASS, reason="ok")]
        narrative = generator.narrate_flow(
            "Flow 1",
            [_make_action()],
            [_make_result()],
            [_make_state(), _make_state("s2")],
            step_verdicts=svs,
        )
        assert "1 steps passed" in narrative.conclusion

    def test_conclusion_with_failures(self, generator):
        svs = [StepVerdict(verdict=Verdict.FAIL, reason="broken")]
        narrative = generator.narrate_flow(
            "Flow 1",
            [_make_action()],
            [_make_result()],
            [_make_state(), _make_state("s2")],
            step_verdicts=svs,
        )
        assert "failure" in narrative.conclusion

    def test_conclusion_with_warning(self, generator):
        svs = [StepVerdict(verdict=Verdict.WARN, reason="hmm")]
        narrative = generator.narrate_flow(
            "Flow 1",
            [_make_action()],
            [_make_result(OutcomeType.NO_CHANGE)],
            [_make_state(), _make_state("s2")],
            step_verdicts=svs,
        )
        assert "warning" in narrative.conclusion.lower()

    def test_gherkin_has_scenario(self, generator):
        narrative = generator.narrate_flow(
            "Login Flow",
            [_make_action()],
            [_make_result()],
            [_make_state(), _make_state("s2")],
        )
        assert "Scenario: Login Flow" in narrative.gherkin
        assert "Given" in narrative.gherkin
        assert "When" in narrative.gherkin
        assert "Then" in narrative.gherkin


class TestToGherkin:
    def test_returns_gherkin_string(self, generator):
        narrative = FlowNarrative(
            title="Test",
            precondition="I am on the home page",
            steps=[],
            gherkin="  Scenario: Test\n    Given I am on the home page",
        )
        result = generator.to_gherkin(narrative)
        assert "Scenario" in result

    def test_toggle_then_clause_is_expectation_based(self, generator):
        action = _make_action(ActionType.CHECK, label="Check: Toggle Switch")
        action.intent = ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description="Toggle Switch",
            expected_effect="The toggle state should change",
        )
        result = _make_result(OutcomeType.NO_CHANGE)
        step = generator.narrate_step(
            action,
            result,
            _make_state(),
            _make_state("s2"),
            1,
            intent=action.intent,
        )
        assert "state should change" in step.gherkin_then


class TestToPlainEnglish:
    def test_returns_markdown(self, generator):
        narrative = generator.narrate_flow(
            "Test Flow",
            [_make_action()],
            [_make_result()],
            [_make_state(), _make_state("s2")],
        )
        md = generator.to_plain_english(narrative)
        assert "## Test Flow" in md
        assert "Step 1" in md

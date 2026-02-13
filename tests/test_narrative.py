"""Tests for narrative generation."""

from __future__ import annotations

import pytest

from flowscout.analysis.narrative import FlowNarrative, NarrativeGenerator
from flowscout.analysis.verdict import ObservationResult
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.discovery.intent import ActionIntent, IntentClass


@pytest.fixture
def generator() -> NarrativeGenerator:
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
    def test_click_description(self, generator: NarrativeGenerator) -> None:
        action = _make_action()
        result = _make_result()
        step = generator.narrate_step(
            action, result, _make_state(), _make_state("s2", title="Login"), 1
        )
        assert step.action_description == "Click the 'Login' element"
        assert step.step_number == 1

    def test_attaches_observation_data(self, generator: NarrativeGenerator) -> None:
        observation = ObservationResult(
            outcome=OutcomeType.DOM_CHANGE,
            stability_score=0.82,
            observation_notes="DOM changed after interaction",
        )
        step = generator.narrate_step(
            _make_action(),
            _make_result(OutcomeType.DOM_CHANGE),
            _make_state(),
            _make_state(),
            1,
            observation=observation,
        )
        assert step.stability_score == 0.82
        assert step.observation_notes == "DOM changed after interaction"
        assert step.is_stable is True

    def test_expected_from_intent(self, generator: NarrativeGenerator) -> None:
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
    def test_basic_flow(self, generator: NarrativeGenerator) -> None:
        actions = [_make_action()]
        results = [_make_result()]
        states: list[PageState | None] = [
            _make_state(),
            _make_state("s2", title="Login"),
        ]
        narrative = generator.narrate_flow("Login Flow", actions, results, states)
        assert narrative.title == "Login Flow"
        assert len(narrative.steps) == 1
        assert "example.com" in narrative.precondition

    def test_conclusion_reports_average_stability(
        self, generator: NarrativeGenerator
    ) -> None:
        narrative = generator.narrate_flow(
            "Flow 1",
            [_make_action()],
            [_make_result()],
            [_make_state(), _make_state("s2")],
            observations=[
                ObservationResult(
                    outcome=OutcomeType.NAVIGATION,
                    stability_score=0.9,
                    observation_notes="Navigation completed",
                )
            ],
        )
        assert "Average stability" in narrative.conclusion
        assert "stable" in narrative.conclusion

    def test_gherkin_has_scenario(self, generator: NarrativeGenerator) -> None:
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
    def test_returns_gherkin_string(self, generator: NarrativeGenerator) -> None:
        narrative = FlowNarrative(
            title="Test",
            precondition="I am on the home page",
            steps=[],
            gherkin="  Scenario: Test\n    Given I am on the home page",
        )
        result = generator.to_gherkin(narrative)
        assert "Scenario" in result

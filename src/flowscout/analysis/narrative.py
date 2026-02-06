"""Narrative generation — plain-English and Gherkin descriptions for flows."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from flowscout.core.state import PageState

from flowscout.analysis.verdict import StepVerdict, Verdict
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.discovery.intent import ActionIntent, IntentClass


class NarrativeStep(BaseModel):
    """A single step in a flow narrative."""

    step_number: int
    action_description: str
    expected: str = ""
    actual: str = ""
    verdict: Verdict | None = None
    gherkin_when: str = ""
    gherkin_then: str = ""


class FlowNarrative(BaseModel):
    """Complete narrative for a flow."""

    title: str
    precondition: str = ""
    steps: list[NarrativeStep] = Field(default_factory=list)
    conclusion: str = ""
    gherkin: str = ""


class NarrativeGenerator:
    """Generates human-readable narratives and Gherkin from flow data."""

    def narrate_step(
        self,
        action: Action,
        result: ActionResult,
        source_state: PageState | None,
        target_state: PageState | None,
        step_number: int,
        *,
        intent: ActionIntent | None = None,
        step_verdict: StepVerdict | None = None,
    ) -> NarrativeStep:
        """Generate a narrative for a single action step."""
        desc = self._action_description(action, result)
        expected = intent.expected_effect if intent else ""
        actual = self._outcome_description(result, target_state)

        gherkin_when = self._gherkin_when(action)
        gherkin_then = self._gherkin_then(result, target_state)

        return NarrativeStep(
            step_number=step_number,
            action_description=desc,
            expected=expected,
            actual=actual,
            verdict=step_verdict.verdict if step_verdict else None,
            gherkin_when=gherkin_when,
            gherkin_then=gherkin_then,
        )

    def narrate_flow(
        self,
        flow_name: str,
        actions: list[Action],
        results: list[ActionResult],
        states: list[PageState | None],
        *,
        intents: list[ActionIntent | None] | None = None,
        step_verdicts: list[StepVerdict | None] | None = None,
    ) -> FlowNarrative:
        """Generate a complete narrative for a flow."""
        steps: list[NarrativeStep] = []
        first_state = states[0] if states else None
        precondition = ""
        if first_state:
            precondition = (
                f'I am on the "{first_state.title or "start"}" page ({first_state.url})'
            )

        for i, (action, result) in enumerate(zip(actions, results)):
            source = states[i] if i < len(states) else None
            target = states[i + 1] if (i + 1) < len(states) else None
            intent = intents[i] if intents and i < len(intents) else None
            sv = step_verdicts[i] if step_verdicts and i < len(step_verdicts) else None

            step = self.narrate_step(
                action,
                result,
                source,
                target,
                i + 1,
                intent=intent,
                step_verdict=sv,
            )
            steps.append(step)

        # Conclusion from verdict counts
        sum(1 for s in steps if s.verdict == Verdict.PASS)
        fail_count = sum(1 for s in steps if s.verdict == Verdict.FAIL)
        total = len(steps)
        if fail_count > 0:
            conclusion = f"{fail_count} failure(s) out of {total} steps"
        elif total > 0:
            conclusion = f"All {total} steps passed"
        else:
            conclusion = "No steps executed"

        gherkin = self._build_gherkin(flow_name, precondition, steps)

        return FlowNarrative(
            title=flow_name,
            precondition=precondition,
            steps=steps,
            conclusion=conclusion,
            gherkin=gherkin,
        )

    def to_gherkin(self, narrative: FlowNarrative) -> str:
        """Generate a Gherkin feature block from a narrative."""
        return narrative.gherkin

    def to_plain_english(self, narrative: FlowNarrative) -> str:
        """Generate a Markdown plain-English report from a narrative."""
        lines = [f"## {narrative.title}", ""]
        if narrative.precondition:
            lines.append(f"**Precondition:** {narrative.precondition}")
            lines.append("")

        for step in narrative.steps:
            verdict_tag = f" [{step.verdict.value.upper()}]" if step.verdict else ""
            lines.append(f"### Step {step.step_number}{verdict_tag}")
            lines.append(f"**Action:** {step.action_description}")
            if step.expected:
                lines.append(f"**Expected:** {step.expected}")
            if step.actual:
                lines.append(f"**Actual:** {step.actual}")
            lines.append("")

        lines.append(f"**Conclusion:** {narrative.conclusion}")
        return "\n".join(lines)

    @staticmethod
    def _clean_label(action: Action) -> str:
        """Get the element label, stripping the action-type prefix."""
        label = action.label
        prefixes = (
            "Click: ",
            "Fill: ",
            "Select ",
            "Check: ",
            "Uncheck: ",
            "Submit: ",
            "Hover: ",
        )
        for prefix in prefixes:
            if label.startswith(prefix):
                return label[len(prefix) :]
        return label

    @staticmethod
    def _page_name(
        state: PageState | None,
        fallback_url: str | None = None,
    ) -> str:
        """Get a human-readable page name from state title or URL."""
        if state and state.title:
            return state.title
        url = (state.url if state else fallback_url) or ""
        if url:
            path = urlparse(url).path.rstrip("/")
            if path:
                return path.split("/")[-1] or url
        return "the next page"

    def _action_description(self, action: Action, result: ActionResult) -> str:
        """Generate a context-aware plain-English action description."""
        label = self._clean_label(action)
        match action.action_type:
            case ActionType.CLICK:
                return self._describe_click(action, label)
            case ActionType.FILL:
                return f"Enter '{action.value}' into the {label} field"
            case ActionType.SELECT_OPTION:
                return f"Select '{action.value}' from the {label} dropdown"
            case ActionType.CHECK:
                return f"Check the {label} checkbox"
            case ActionType.UNCHECK:
                return f"Uncheck the {label} checkbox"
            case ActionType.SUBMIT_FORM:
                return f"Submit the form by clicking '{label}'"
            case ActionType.HOVER:
                return f"Hover over the '{label}' element"
            case ActionType.PRESS_KEY:
                return f"Press the '{action.value}' key"
            case ActionType.NAVIGATE:
                return f"Navigate directly to {action.value}"
        return f"Perform {action.action_type.value} on {label}"

    def _describe_click(self, action: Action, label: str) -> str:
        """Generate a context-aware description for a click action."""
        # Dropdown option selection
        if action.metadata.get("requires_open"):
            return f"Select '{label}' from the dropdown"

        # Search trigger
        if action.metadata.get("is_search") == "true":
            return "Search for 'test query'"

        # Use intent for semantic context
        intent = action.intent
        if intent:
            if intent.intent_class == IntentClass.SELECT:
                return f"Select '{label}'"
            if intent.intent_class == IntentClass.REVEAL:
                return f"Open the '{label}' dropdown"
            if intent.intent_class == IntentClass.TOGGLE:
                return f"Toggle '{label}'"
            if intent.intent_class == IntentClass.NAVIGATE:
                return f"Navigate to '{label}'"

        return f"Click the '{label}' element"

    def _outcome_description(
        self,
        result: ActionResult,
        target_state: PageState | None,
    ) -> str:
        """Generate a plain-English outcome description."""
        match result.outcome:
            case OutcomeType.NAVIGATION:
                name = self._page_name(target_state, result.url_after)
                return f"Page navigated to '{name}'"
            case OutcomeType.DOM_CHANGE:
                return "Page content updated"
            case OutcomeType.NO_CHANGE:
                return "No visible change"
            case OutcomeType.VALIDATION_ERROR:
                errors = (
                    ", ".join(result.error_messages[:2])
                    if result.error_messages
                    else "validation errors"
                )
                return f"Validation errors appeared: {errors}"
            case OutcomeType.NETWORK_ERROR:
                return "Network error occurred"
            case OutcomeType.CONSOLE_ERROR:
                return "Console error detected"
            case OutcomeType.TIMEOUT:
                return "Action timed out (element may be hidden)"
            case OutcomeType.EXCEPTION:
                return (
                    f"Error: {result.message[:80]}"
                    if result.message
                    else "An error occurred"
                )
        return result.outcome.value

    def _gherkin_when(self, action: Action) -> str:
        """Generate a Gherkin When clause."""
        label = self._clean_label(action)
        match action.action_type:
            case ActionType.CLICK:
                return self._gherkin_when_click(action, label)
            case ActionType.FILL:
                return f'When I enter "{action.value}" into the "{label}" field'
            case ActionType.SELECT_OPTION:
                return f'When I select "{action.value}" from the "{label}" dropdown'
            case ActionType.CHECK:
                return f'When I check the "{label}" checkbox'
            case ActionType.UNCHECK:
                return f'When I uncheck the "{label}" checkbox'
            case ActionType.SUBMIT_FORM:
                return f'When I submit the form by clicking "{label}"'
            case ActionType.HOVER:
                return f'When I hover over the "{label}" element'
            case ActionType.PRESS_KEY:
                return f'When I press the "{action.value}" key'
            case ActionType.NAVIGATE:
                return f'When I navigate to "{action.value}"'
        return f'When I perform {action.action_type.value} on "{label}"'

    def _gherkin_when_click(self, action: Action, label: str) -> str:
        """Generate a Gherkin When clause for click actions with context."""
        if action.metadata.get("requires_open"):
            return f'When I select "{label}" from the dropdown'
        if action.metadata.get("is_search") == "true":
            return 'When I search for "test query"'

        intent = action.intent
        if intent:
            if intent.intent_class == IntentClass.SELECT:
                return f'When I select "{label}"'
            if intent.intent_class == IntentClass.REVEAL:
                return f'When I open the "{label}" dropdown'
            if intent.intent_class == IntentClass.TOGGLE:
                return f'When I toggle "{label}"'
            if intent.intent_class == IntentClass.NAVIGATE:
                return f'When I navigate to "{label}"'

        return f'When I click the "{label}" element'

    def _gherkin_then(
        self,
        result: ActionResult,
        target_state: PageState | None,
    ) -> str:
        """Generate a Gherkin Then clause."""
        match result.outcome:
            case OutcomeType.NAVIGATION:
                name = self._page_name(target_state, result.url_after)
                return f'Then the page should navigate to "{name}"'
            case OutcomeType.DOM_CHANGE:
                return "Then the page content should update"
            case OutcomeType.NO_CHANGE:
                return "Then no visible change should occur"
            case OutcomeType.VALIDATION_ERROR:
                return "Then validation errors should appear"
            case OutcomeType.TIMEOUT:
                return "Then the action should time out"
            case OutcomeType.NETWORK_ERROR:
                return "Then a network error should occur"
            case OutcomeType.CONSOLE_ERROR:
                return "Then a console error should be logged"
            case OutcomeType.EXCEPTION:
                return "Then an error should occur"
        return f"Then the outcome should be {result.outcome.value}"

    def _build_gherkin(
        self, flow_name: str, precondition: str, steps: list[NarrativeStep]
    ) -> str:
        """Build a complete Gherkin scenario."""
        lines = [f"  Scenario: {flow_name}"]
        if precondition:
            lines.append(f"    Given {precondition}")

        for step in steps:
            if step.gherkin_when:
                lines.append(f"    {step.gherkin_when}")
            if step.gherkin_then:
                lines.append(f"    {step.gherkin_then}")

        return "\n".join(lines)

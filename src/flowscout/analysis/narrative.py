"""Narrative generation — plain-English and Gherkin descriptions for flows."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from flowscout.core.state import PageState

from flowscout.analysis.verdict import ObservationResult
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.discovery.intent import ActionIntent, IntentClass


class NarrativeStep(BaseModel):
    """A single step in a flow narrative."""

    step_number: int
    action_description: str
    expected: str = ""
    actual: str = ""
    outcome: OutcomeType | None = None
    stability_score: float = 0.0
    observation_notes: str = ""
    is_stable: bool = False
    gherkin_when: str = ""
    gherkin_then: str = ""
    target_selector: str = ""
    target_description: str = ""
    element_type: str = ""


class FlowNarrative(BaseModel):
    """Complete narrative for a flow."""

    title: str
    precondition: str = ""
    steps: list[NarrativeStep] = Field(default_factory=list)
    conclusion: str = ""
    gherkin: str = ""


def _is_css_selector(text: str) -> bool:
    """Detect if text looks like a CSS selector rather than a human label."""
    indicators = (
        " > ",
        "nth-of-type",
        "nth-child",
        "#__",
        "div >",
        "header >",
        "form >",
        ":nth-",
        "[data-",
        "div:nth",
        "span:nth",
    )
    return any(ind in text for ind in indicators)


def _humanize(text: str) -> str:
    """Replace CSS selector fragments in text with clean descriptions."""
    if not _is_css_selector(text):
        return text
    import re

    # "Submit the <selector> form and process the data"
    if "form and process the data" in text:
        return "Submit the form and process the data"
    # "Form should display validation errors..."
    if "should display validation errors" in text:
        return "Form should display validation errors for invalid/missing input"
    # Generic: replace selector-like fragments
    return re.sub(
        r"[#.]?[\w-]*(?:\s*>\s*[\w.#:\[\]=\"-]+)+",
        "the element",
        text,
    ).strip()


class NarrativeGenerator:
    """Generates human-readable narratives and Gherkin from flow data."""

    _STEP_STABLE_THRESHOLD = 0.7

    def narrate_step(
        self,
        action: Action,
        result: ActionResult,
        source_state: PageState | None,
        target_state: PageState | None,
        step_number: int,
        *,
        intent: ActionIntent | None = None,
        observation: ObservationResult | None = None,
    ) -> NarrativeStep:
        """Generate a narrative for a single action step."""
        desc = self._action_description(action, result, source_state)
        expected = _humanize(intent.expected_effect) if intent else ""
        actual = self._outcome_description(result, target_state)
        stability_score = (
            observation.stability_score
            if observation
            else float(result.stability_score or 0.0)
        )
        observation_notes = (
            observation.observation_notes
            if observation
            else (result.observation_notes or "").strip()
        )

        gherkin_when = self._gherkin_when(action)
        gherkin_then = self._gherkin_then(
            action=action,
            result=result,
            target_state=target_state,
            intent=intent,
        )

        # Determine element type from metadata or action type
        elem_type = action.meta.element_type
        if not elem_type and action.intent:
            elem_type = action.intent.intent_class.value

        return NarrativeStep(
            step_number=step_number,
            action_description=desc,
            expected=expected,
            actual=actual,
            outcome=result.outcome,
            stability_score=stability_score,
            observation_notes=observation_notes,
            is_stable=stability_score >= self._STEP_STABLE_THRESHOLD,
            gherkin_when=gherkin_when,
            gherkin_then=gherkin_then,
            target_selector=action.target_selector,
            target_description=(
                intent.target_description
                if intent and intent.target_description
                else ""
            ),
            element_type=elem_type,
        )

    def narrate_flow(
        self,
        flow_name: str,
        actions: list[Action],
        results: list[ActionResult],
        states: list[PageState | None],
        *,
        intents: list[ActionIntent | None] | None = None,
        observations: list[ObservationResult | None] | None = None,
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
            observation = (
                observations[i] if observations and i < len(observations) else None
            )

            step = self.narrate_step(
                action,
                result,
                source,
                target,
                i + 1,
                intent=intent,
                observation=observation,
            )
            steps.append(step)

        # Conclusion from stability observations.
        total = len(steps)
        if total == 0:
            conclusion = "No steps executed"
        else:
            avg_stability = sum(step.stability_score for step in steps) / total
            stable_count = sum(1 for step in steps if step.is_stable)
            unstable_count = total - stable_count
            conclusion = (
                f"Average stability {avg_stability:.2f}"
                f" ({stable_count} stable, {unstable_count} unstable)"
            )

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
            lines.append(f"### Step {step.step_number}")
            lines.append(f"**Action:** {step.action_description}")
            if step.outcome:
                lines.append(f"**Outcome:** {step.outcome.value}")
            lines.append(
                f"**Stability:** {step.stability_score:.2f}"
                f" ({'stable' if step.is_stable else 'unstable'})"
            )
            if step.observation_notes:
                lines.append(f"**Observation:** {step.observation_notes}")
            if step.expected:
                lines.append(f"**Expected:** {step.expected}")
            if step.actual:
                lines.append(f"**Actual:** {step.actual}")
            lines.append("")

        lines.append(f"**Conclusion:** {narrative.conclusion}")
        return "\n".join(lines)

    @staticmethod
    def _clean_label(action: Action) -> str:
        """Get the element label, stripping the action-type prefix and selectors."""
        import re

        label = action.label
        prefixes = (
            "Click: ",
            "Fill: ",
            "Select ",
            "Check: ",
            "Uncheck: ",
            "Submit form (invalid): ",
            "Submit form: ",
            "Submit: ",
            "Hover: ",
            "Open dropdown: ",
            "Select option: ",
            "Select radio: ",
            "Tab: ",
            "Toggle: ",
        )
        for prefix in prefixes:
            if label.startswith(prefix):
                label = label[len(prefix) :]
                break
        if action.action_type == ActionType.FILL:
            label = re.sub(r"\s*=\s*'.*'$", "", label).strip()
        # If the result is a CSS selector, try the intent target description
        if _is_css_selector(label) and action.intent:
            target = action.intent.target_description
            if target and not _is_css_selector(target):
                return str(target)
        return str(label)

    @staticmethod
    def _page_name(
        state: PageState | None,
        fallback_url: str | None = None,
    ) -> str:
        """Get a human-readable page name from state title or URL."""
        if state and state.title:
            return str(state.title)
        url = (state.url if state else fallback_url) or ""
        if url:
            path = urlparse(url).path.rstrip("/")
            if path:
                return path.split("/")[-1] or url
        return "the next page"

    def _action_description(
        self,
        action: Action,
        result: ActionResult,
        source_state: PageState | None,
    ) -> str:
        """Generate a context-aware plain-English action description."""
        label = self._clean_label(action)
        # Final safety: if label still looks like a selector, use generic text
        if _is_css_selector(label):
            label = action.intent.target_description if action.intent else "the element"
            if _is_css_selector(label):
                label = "the element"
        match action.action_type:
            case ActionType.CLICK:
                return self._describe_click(action, label)
            case ActionType.FILL:
                return f"Enter '{action.value}' into the '{label}' field"
            case ActionType.SELECT_OPTION:
                return f"Select '{action.value}' from the '{label}' dropdown"  # nosec B608 - narrative text, not SQL
            case ActionType.CHECK:
                return self._describe_toggle(
                    label=label,
                    source_state=source_state,
                    action_word="Enable",
                )
            case ActionType.UNCHECK:
                return self._describe_toggle(
                    label=label,
                    source_state=source_state,
                    action_word="Disable",
                )
            case ActionType.SUBMIT_FORM:
                return self._describe_submit(action, label)
            case ActionType.HOVER:
                return f"Hover over '{label}'"
            case ActionType.PRESS_KEY:
                return f"Press the '{action.value}' key"
            case ActionType.NAVIGATE:
                return f"Navigate directly to {action.value}"
        return f"Perform {action.action_type.value} on '{label}'"

    def _describe_toggle(
        self,
        *,
        label: str,
        source_state: PageState | None,
        action_word: str,
    ) -> str:
        """Generate an explicit toggle description with page context."""
        control = "toggle switch" if "toggle" in label.lower() else "option"
        location = self._page_name(source_state) if source_state else "current page"
        if label and label != "the element":
            return f"{action_word} '{label}' ({control}) on '{location}'"
        return f"{action_word} the {control} on '{location}'"

    def _describe_submit(self, action: Action, label: str) -> str:
        """Generate a context-aware description for form submission."""
        scenario = action.meta.scenario
        if scenario == "invalid":
            return "Submit the form with invalid data"
        if label and label != "the element":
            return f"Submit the form via '{label}'"
        return "Submit the form"

    def _describe_click(self, action: Action, label: str) -> str:
        """Generate a context-aware description for a click action."""
        # Dropdown option selection
        if action.meta.is_dropdown_option:
            return f"Select '{label}' from the dropdown"  # nosec B608 - narrative text, not SQL

        # Search trigger
        if action.meta.is_search:
            return "Search for 'test query'"

        # Use intent for semantic context
        intent = action.intent
        if intent:
            if intent.intent_class == IntentClass.SELECT:
                return f"Click '{label}'"
            if intent.intent_class == IntentClass.REVEAL:
                reveal_text = intent.expected_effect.lower()
                if any(word in reveal_text for word in ("close", "dismiss", "hide")):
                    return f"Dismiss '{label}'"
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
        return str(result.outcome.value)

    def _gherkin_when(self, action: Action) -> str:
        """Generate a Gherkin When clause."""
        label = self._clean_label(action)
        match action.action_type:
            case ActionType.CLICK:
                return self._gherkin_when_click(action, label)
            case ActionType.FILL:
                return f'When I enter "{action.value}" into the "{label}" field'
            case ActionType.SELECT_OPTION:
                return f'When I select "{action.value}" from the "{label}" dropdown'  # nosec B608 - narrative text, not SQL
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
        if action.meta.is_dropdown_option:
            return f'When I select "{label}" from the dropdown'  # nosec B608 - narrative text, not SQL
        if action.meta.is_search:
            return 'When I search for "test query"'

        intent = action.intent
        if intent:
            if intent.intent_class == IntentClass.SELECT:
                return f'When I click "{label}"'
            if intent.intent_class == IntentClass.REVEAL:
                reveal_text = intent.expected_effect.lower()
                if any(word in reveal_text for word in ("close", "dismiss", "hide")):
                    return f'When I dismiss "{label}"'
                return f'When I open the "{label}" dropdown'
            if intent.intent_class == IntentClass.TOGGLE:
                return f'When I toggle "{label}"'
            if intent.intent_class == IntentClass.NAVIGATE:
                return f'When I navigate to "{label}"'

        return f'When I click the "{label}" element'

    def _gherkin_then(
        self,
        *,
        action: Action,
        result: ActionResult,
        target_state: PageState | None,
        intent: ActionIntent | None,
    ) -> str:
        """Generate a Gherkin Then clause."""
        if intent:
            label = self._clean_label(action)
            match intent.intent_class:
                case IntentClass.NAVIGATE:
                    name = self._page_name(target_state, result.url_after)
                    return f'Then the page should navigate to "{name}"'
                case IntentClass.INPUT:
                    return f'Then the "{label}" field should reflect the entered input'
                case IntentClass.TOGGLE:
                    return (
                        f'Then the "{label}" control state should change '
                        "(enabled/disabled or checked/unchecked)"
                    )
                case IntentClass.SUBMIT:
                    return "Then the form submission should be processed or validated"
                case IntentClass.REVEAL:
                    reveal_text = intent.expected_effect.lower()
                    if any(
                        word in reveal_text for word in ("close", "dismiss", "hide")
                    ):
                        return (
                            f'Then the message or panel for "{label}" should be closed'
                        )
                    return (
                        f'Then additional content for "{label}" should become visible'
                    )
                case IntentClass.SELECT:
                    if action.action_type == ActionType.CLICK:
                        return (
                            f'Then the application should respond to clicking "{label}"'
                        )
                    return f'Then the selection for "{label}" should be applied'

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

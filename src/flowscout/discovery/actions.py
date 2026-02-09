"""Action generation from discovered interactive elements."""

from __future__ import annotations

from enum import StrEnum, auto
from hashlib import md5

from pydantic import BaseModel, Field

from flowscout.discovery.elements import ElementType, InteractiveElement
from flowscout.discovery.inputs import generate_input_value
from flowscout.discovery.intent import ActionIntent, infer_intent


class ActionType(StrEnum):
    CLICK = auto()
    FILL = auto()
    SELECT_OPTION = auto()
    CHECK = auto()
    UNCHECK = auto()
    SUBMIT_FORM = auto()
    PRESS_KEY = auto()
    HOVER = auto()
    NAVIGATE = auto()


class OutcomeType(StrEnum):
    NAVIGATION = auto()
    DOM_CHANGE = auto()
    VISUAL_CHANGE = auto()
    NO_CHANGE = auto()
    VALIDATION_ERROR = auto()
    NETWORK_ERROR = auto()
    CONSOLE_ERROR = auto()
    TIMEOUT = auto()
    EXCEPTION = auto()


class Action(BaseModel):
    """A concrete action to perform on an element."""

    action_id: str
    action_type: ActionType
    target_selector: str
    label: str
    value: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    priority: int = Field(default=50)
    source_element_id: str | None = None
    intent: ActionIntent | None = None


class ActionResult(BaseModel):
    """Result of executing an action."""

    action_id: str
    source_state_id: str = ""
    target_state_id: str = ""
    outcome: OutcomeType
    duration_ms: float = 0.0
    message: str = ""
    url_before: str = ""
    url_after: str = ""
    dom_changes_summary: str = ""
    error_messages: list[str] = Field(default_factory=list)
    console_errors: list[str] = Field(default_factory=list)
    screenshot_path: str | None = None
    timestamp: str = ""
    verdict: str | None = None
    verdict_reason: str | None = None
    expected: str | None = None
    actual: str | None = None


def build_action_id(selector: str, action_type: str, value: str = "") -> str:
    """Create a stable hash ID for an action."""
    return md5(f"{selector}:{action_type}:{value}".encode()).hexdigest()[:12]


# Element types that represent fillable inputs
_FILLABLE_TYPES = {
    ElementType.INPUT_TEXT,
    ElementType.INPUT_EMAIL,
    ElementType.INPUT_PASSWORD,
    ElementType.INPUT_NUMBER,
    ElementType.INPUT_TEL,
    ElementType.INPUT_URL,
    ElementType.INPUT_SEARCH,
    ElementType.INPUT_DATE,
    ElementType.TEXTAREA,
}


def generate_actions(
    elements: list[InteractiveElement],
    *,
    base_url: str = "",
) -> list[Action]:
    """Generate a list of actions from discovered elements."""
    actions: list[Action] = []

    for elem in elements:
        if elem.is_disabled or not elem.is_visible:
            continue

        new_actions = _actions_for_element(elem, base_url=base_url)
        actions.extend(new_actions)

    # Sort by priority
    actions.sort(key=lambda a: a.priority)
    return actions


def _actions_for_element(
    elem: InteractiveElement,
    *,
    base_url: str = "",
) -> list[Action]:
    """Generate actions for a single element based on its type."""
    actions: list[Action] = []
    etype = elem.element_type

    def _make(action_type: ActionType, **kwargs) -> Action:
        a = Action(action_type=action_type, **kwargs)
        a.intent = infer_intent(
            elem, action_type.value, value=kwargs.get("value"), form_selector=None
        )
        return a

    # Links and buttons → CLICK
    if etype in (ElementType.LINK, ElementType.BUTTON, ElementType.GENERIC_CLICKABLE):
        # Skip external links
        if etype == ElementType.LINK and elem.href:
            if (
                base_url
                and not elem.href.startswith(base_url)
                and elem.href.startswith("http")
            ):
                return []
            if elem.href.startswith("javascript:"):
                return []

        click_meta: dict[str, str] = {}
        if elem.href:
            click_meta["href"] = elem.href
        if elem.aria_role == "search":
            click_meta["is_search"] = "true"

        actions.append(
            _make(
                ActionType.CLICK,
                action_id=build_action_id(elem.selector, "click"),
                target_selector=elem.selector,
                label=(
                    f"Click: {elem.label}" if elem.label else f"Click: {elem.selector}"
                ),
                priority=elem.priority,
                source_element_id=elem.element_id,
                metadata=click_meta,
            )
        )

    # Fillable inputs → FILL with heuristic value
    elif etype in _FILLABLE_TYPES:
        value = generate_input_value(elem, scenario="valid")
        meta: dict[str, str] = {"element_type": etype.value}
        actions.append(
            _make(
                ActionType.FILL,
                action_id=build_action_id(elem.selector, "fill", value),
                target_selector=elem.selector,
                label=f"Fill: {elem.label or elem.name or elem.selector} = '{value}'",
                value=value,
                priority=elem.priority,
                source_element_id=elem.element_id,
                metadata=meta,
            )
        )

    # Select elements → one SELECT_OPTION per option
    elif etype == ElementType.SELECT:
        for option in elem.options:
            actions.append(
                _make(
                    ActionType.SELECT_OPTION,
                    action_id=build_action_id(elem.selector, "select", option),
                    target_selector=elem.selector,
                    label=f"Select '{option}' in {elem.label or elem.selector}",
                    value=option,
                    priority=elem.priority,
                    source_element_id=elem.element_id,
                )
            )

    # Tabs → CLICK
    elif etype == ElementType.TAB:
        actions.append(
            _make(
                ActionType.CLICK,
                action_id=build_action_id(elem.selector, "click"),
                target_selector=elem.selector,
                label=f"Tab: {elem.label}",
                priority=elem.priority,
                source_element_id=elem.element_id,
            )
        )

    # Dropdown triggers → CLICK to open
    elif etype == ElementType.DROPDOWN_TRIGGER:
        actions.append(
            _make(
                ActionType.CLICK,
                action_id=build_action_id(elem.selector, "click"),
                target_selector=elem.selector,
                label=f"Open dropdown: {elem.label}",
                priority=elem.priority,
                source_element_id=elem.element_id,
            )
        )

    # Dropdown options → CLICK with requires_open metadata
    elif etype == ElementType.DROPDOWN_OPTION:
        option_meta: dict[str, str] = {}
        if "requires_open" in elem.data_attributes:
            option_meta["requires_open"] = elem.data_attributes["requires_open"]
        actions.append(
            _make(
                ActionType.CLICK,
                action_id=build_action_id(elem.selector, "click"),
                target_selector=elem.selector,
                label=f"Select option: {elem.label}",
                priority=elem.priority,
                source_element_id=elem.element_id,
                metadata=option_meta,
            )
        )

    # Checkboxes → CHECK/UNCHECK
    elif etype == ElementType.INPUT_CHECKBOX:
        actions.append(
            _make(
                ActionType.CHECK,
                action_id=build_action_id(elem.selector, "check"),
                target_selector=elem.selector,
                label=f"Check: {elem.label or elem.name or elem.selector}",
                priority=elem.priority,
                source_element_id=elem.element_id,
            )
        )

    # Radio buttons → CLICK
    elif etype == ElementType.INPUT_RADIO:
        actions.append(
            _make(
                ActionType.CLICK,
                action_id=build_action_id(elem.selector, "click"),
                target_selector=elem.selector,
                label=f"Select radio: {elem.label or elem.name or elem.selector}",
                priority=elem.priority,
                source_element_id=elem.element_id,
            )
        )

    # Toggles → CLICK
    elif etype == ElementType.TOGGLE:
        actions.append(
            _make(
                ActionType.CLICK,
                action_id=build_action_id(elem.selector, "click"),
                target_selector=elem.selector,
                label=f"Toggle: {elem.label or elem.selector}",
                priority=elem.priority,
                source_element_id=elem.element_id,
            )
        )

    return actions


def generate_form_submit_actions(
    elements: list[InteractiveElement],
) -> list[Action]:
    """Generate form submission actions by grouping inputs with submit buttons."""
    # Group elements by parent form
    forms: dict[str, list[InteractiveElement]] = {}
    for elem in elements:
        if elem.parent_form_selector:
            forms.setdefault(elem.parent_form_selector, []).append(elem)

    actions: list[Action] = []
    for form_selector, form_elements in forms.items():
        inputs = [e for e in form_elements if e.element_type in _FILLABLE_TYPES]
        submits = [
            e
            for e in form_elements
            if e.element_type == ElementType.BUTTON
            and any(
                w in e.label.lower()
                for w in ("submit", "save", "login", "sign", "create", "send")
            )
        ]

        if not submits:
            # Look for any button in the form
            submits = [e for e in form_elements if e.element_type == ElementType.BUTTON]

        if not inputs and not submits:
            continue

        # Generate field values
        field_values: dict[str, str] = {}
        for inp in inputs:
            value = generate_input_value(inp, scenario="valid")
            field_values[inp.selector] = value

        submit_selector = submits[0].selector if submits else form_selector
        import json

        # Valid submission
        valid_intent = ActionIntent(
            intent_class="submit",
            target_description=f"Submit form: {form_selector}",
            expected_effect=f"Submit the {form_selector} form and process the data",
            context={"form_selector": form_selector},
        )
        actions.append(
            Action(
                action_id=build_action_id(form_selector, "submit"),
                action_type=ActionType.SUBMIT_FORM,
                target_selector=submit_selector,
                label=f"Submit form: {form_selector}",
                value=None,
                metadata={
                    "field_values_json": json.dumps(field_values),
                    "form_selector": form_selector,
                },
                priority=15,
                intent=valid_intent,
            )
        )

        # Invalid submission (Phase 5)
        if inputs:
            invalid_values: dict[str, str] = {}
            for inp in inputs:
                if inp.is_required:
                    invalid_values[inp.selector] = ""
                else:
                    invalid_values[inp.selector] = generate_input_value(
                        inp, scenario="invalid"
                    )

            invalid_intent = ActionIntent(
                intent_class="submit",
                target_description=f"Submit form (invalid): {form_selector}",
                expected_effect="Form should display validation errors for invalid/missing input",
                context={"form_selector": form_selector, "scenario": "invalid"},
            )
            actions.append(
                Action(
                    action_id=build_action_id(form_selector, "submit_invalid"),
                    action_type=ActionType.SUBMIT_FORM,
                    target_selector=submit_selector,
                    label=f"Submit form (invalid): {form_selector}",
                    value=None,
                    metadata={
                        "field_values_json": json.dumps(invalid_values),
                        "form_selector": form_selector,
                        "scenario": "invalid",
                        "expected_outcome": "validation_error",
                    },
                    priority=16,
                    intent=invalid_intent,
                )
            )

    return actions

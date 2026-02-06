"""Intent modeling for actions — attaches structured intent to every Action."""

from __future__ import annotations

from enum import StrEnum, auto
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from flowscout.discovery.elements import InteractiveElement

from flowscout.discovery.elements import ElementType


class IntentClass(StrEnum):
    NAVIGATE = auto()
    INPUT = auto()
    TOGGLE = auto()
    SUBMIT = auto()
    REVEAL = auto()
    SELECT = auto()


class ActionIntent(BaseModel):
    """Structured intent describing what an action is expected to achieve."""

    intent_class: IntentClass
    target_description: str = Field(description="Human-readable element name")
    expected_effect: str = Field(description="What should happen after this action")
    context: dict[str, str] = Field(default_factory=dict)


def infer_intent(
    element: InteractiveElement,
    action_type: str,
    *,
    value: str | None = None,
    form_selector: str | None = None,
) -> ActionIntent:
    """Infer structured intent from an element and action type.

    Uses heuristic rules based on element type, action type, and metadata.
    """
    from flowscout.discovery.actions import ActionType

    target = _build_target_description(element)

    at = ActionType(action_type) if isinstance(action_type, str) else action_type

    if at == ActionType.FILL:
        field_name = (
            element.name or element.aria_label or element.placeholder or "field"
        )
        return ActionIntent(
            intent_class=IntentClass.INPUT,
            target_description=target,
            expected_effect=f"Enter data into the {field_name} field",
            context={"field": field_name, "value": value or ""},
        )

    if at == ActionType.SELECT_OPTION:
        return ActionIntent(
            intent_class=IntentClass.SELECT,
            target_description=target,
            expected_effect=f"Select '{value}' from {target}",
            context={"value": value or ""},
        )

    if at == ActionType.CHECK:
        return ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description=target,
            expected_effect=f"Check the {target} checkbox",
        )

    if at == ActionType.UNCHECK:
        return ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description=target,
            expected_effect=f"Uncheck the {target} checkbox",
        )

    if at == ActionType.HOVER:
        return ActionIntent(
            intent_class=IntentClass.REVEAL,
            target_description=target,
            expected_effect=f"Reveal content by hovering over {target}",
        )

    if at == ActionType.PRESS_KEY:
        return ActionIntent(
            intent_class=IntentClass.INPUT,
            target_description=target,
            expected_effect=f"Press key '{value}'",
            context={"key": value or ""},
        )

    if at == ActionType.NAVIGATE:
        return ActionIntent(
            intent_class=IntentClass.NAVIGATE,
            target_description=target,
            expected_effect=f"Navigate directly to {value}",
            context={"url": value or ""},
        )

    if at == ActionType.SUBMIT_FORM:
        form_name = form_selector or "form"
        return ActionIntent(
            intent_class=IntentClass.SUBMIT,
            target_description=target,
            expected_effect=f"Submit the {form_name} form and process the data",
            context={"form_selector": form_selector or ""},
        )

    # CLICK — dispatch further on ElementType
    if at == ActionType.CLICK:
        return _infer_click_intent(element, target)

    return ActionIntent(
        intent_class=IntentClass.SELECT,
        target_description=target,
        expected_effect=f"Interact with {target}",
    )


def _infer_click_intent(element: InteractiveElement, target: str) -> ActionIntent:
    """Secondary dispatch for CLICK actions based on ElementType."""
    etype = element.element_type

    if etype == ElementType.LINK:
        href = element.href or ""
        return ActionIntent(
            intent_class=IntentClass.NAVIGATE,
            target_description=target,
            expected_effect=f"Navigate to a new page via the '{target}' link",
            context={"href": href},
        )

    if etype == ElementType.TAB:
        return ActionIntent(
            intent_class=IntentClass.SELECT,
            target_description=target,
            expected_effect=f"Switch to the '{target}' tab and display its content",
        )

    if etype == ElementType.DROPDOWN_TRIGGER:
        return ActionIntent(
            intent_class=IntentClass.REVEAL,
            target_description=target,
            expected_effect=f"Open the '{target}' dropdown menu",
        )

    if etype == ElementType.DROPDOWN_OPTION:
        return ActionIntent(
            intent_class=IntentClass.SELECT,
            target_description=target,
            expected_effect=f"Select the '{target}' option from the dropdown",
        )

    if etype == ElementType.TOGGLE:
        return ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description=target,
            expected_effect=f"Toggle the '{target}' switch",
        )

    if etype == ElementType.INPUT_CHECKBOX:
        return ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description=target,
            expected_effect=f"Toggle the '{target}' checkbox",
        )

    if etype == ElementType.INPUT_RADIO:
        return ActionIntent(
            intent_class=IntentClass.SELECT,
            target_description=target,
            expected_effect=f"Select the '{target}' radio option",
        )

    # Button — check if label suggests submit/navigation
    if etype == ElementType.BUTTON:
        label_lower = element.label.lower()
        if any(
            w in label_lower
            for w in ("submit", "save", "create", "login", "sign", "send", "confirm")
        ):
            return ActionIntent(
                intent_class=IntentClass.SUBMIT,
                target_description=target,
                expected_effect=f"Submit by clicking the '{target}' button",
            )
        if any(
            w in label_lower
            for w in (
                "get started",
                "explore",
                "view",
                "open",
                "go",
                "next",
                "continue",
            )
        ):
            return ActionIntent(
                intent_class=IntentClass.NAVIGATE,
                target_description=target,
                expected_effect=f"Navigate forward by clicking '{target}'",
            )

    return ActionIntent(
        intent_class=IntentClass.SELECT,
        target_description=target,
        expected_effect=f"Click the '{target}' element and observe the result",
    )


def _build_target_description(element: InteractiveElement) -> str:
    """Build a human-readable element name from metadata, prioritizing stable labels."""
    if element.aria_label:
        return element.aria_label
    if element.label and element.label.strip():
        return element.label.strip()
    if element.name:
        return element.name
    if element.placeholder:
        return element.placeholder
    return element.selector

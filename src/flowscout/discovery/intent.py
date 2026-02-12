"""Intent modeling for actions — attaches structured intent to every Action."""

from __future__ import annotations

from enum import StrEnum, auto
import re
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


_GENERIC_LABELS = frozenset(
    {
        "a",
        "link",
        "button",
        "input",
        "checkbox",
        "radio",
        "switch",
        "toggle switch",
        "element",
        "form",
    }
)

_CLOSE_LABELS = frozenset({"x", "×", "✕", "✖", "close"})
_THEME_TOGGLE_HINTS = (
    "theme",
    "dark mode",
    "light mode",
    "color scheme",
    "appearance",
)


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
            expected_effect=f"The {field_name} field should contain the entered value",
            context={"field": field_name, "value": value or ""},
        )

    if at == ActionType.SELECT_OPTION:
        return ActionIntent(
            intent_class=IntentClass.SELECT,
            target_description=target,
            expected_effect=f"The selected value should be '{value}' for {target}",
            context={"value": value or ""},
        )

    if at == ActionType.CHECK:
        return ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description=target,
            expected_effect=f"The {target} should become enabled/checked",
        )

    if at == ActionType.UNCHECK:
        return ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description=target,
            expected_effect=f"The {target} should become disabled/unchecked",
        )

    if at == ActionType.HOVER:
        return ActionIntent(
            intent_class=IntentClass.REVEAL,
            target_description=target,
            expected_effect=(
                f"Additional content related to {target} should become visible"
            ),
        )

    if at == ActionType.PRESS_KEY:
        return ActionIntent(
            intent_class=IntentClass.INPUT,
            target_description=target,
            expected_effect=f"The page should react to '{value}' key input",
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
            expected_effect=(
                f"The {form_name} submission should be processed or validated"
            ),
            context={"form_selector": form_selector or ""},
        )

    # CLICK — dispatch further on ElementType
    if at == ActionType.CLICK:
        return _infer_click_intent(element, target)

    return ActionIntent(
        intent_class=IntentClass.SELECT,
        target_description=target,
        expected_effect=f"The UI should react to interaction with {target}",
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
            expected_effect=f"Select the '{target}' option from the dropdown",  # nosec B608 - narrative text, not SQL
        )

    if etype == ElementType.TOGGLE:
        return ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description=target,
            expected_effect=f"The {target} state should change",
        )

    if etype == ElementType.INPUT_CHECKBOX:
        return ActionIntent(
            intent_class=IntentClass.TOGGLE,
            target_description=target,
            expected_effect=f"The {target} state should change",
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
        if _looks_like_dismiss_button(
            label=label_lower,
            target=target,
            selector=element.selector,
        ):
            return ActionIntent(
                intent_class=IntentClass.REVEAL,
                target_description=target,
                expected_effect=(
                    f"The inline message or panel related to '{target}' should close"
                ),
            )
        if any(
            w in label_lower
            for w in ("submit", "save", "create", "login", "sign", "send", "confirm")
        ):
            return ActionIntent(
                intent_class=IntentClass.SUBMIT,
                target_description=target,
                expected_effect=(
                    f"The action triggered by '{target}' should be processed"
                ),
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
        expected_effect=(
            f"A visible application response should occur after clicking '{target}'"
        ),
    )


def _build_target_description(element: InteractiveElement) -> str:
    """Build a human-readable element name from metadata, prioritizing stable labels."""
    theme_toggle_target = _infer_theme_toggle_target(element)
    if theme_toggle_target:
        return theme_toggle_target

    candidates = [
        (element.aria_label or "").strip(),
        (element.label or "").strip(),
        (element.name or "").strip(),
        (element.placeholder or "").strip(),
    ]
    for value in candidates:
        if value.lower() in _CLOSE_LABELS:
            return "close button"
        if _is_meaningful_target(value):
            return value

    if element.href and element.href.strip():
        href = element.href.strip()
        if href.startswith("/"):
            parts = [part for part in href.split("/") if part]
            if parts:
                leaf = parts[-1]
                leaf = re.sub(r"[-_]+", " ", leaf)
                if _is_meaningful_target(leaf):
                    return f"{leaf} link"
            return "internal link"
        if href.startswith("http"):
            return "external link"

    if element.dom_id and element.dom_id.strip():
        return _selector_hint(f"#{element.dom_id}")
    return _selector_hint(element.selector)


def _infer_theme_toggle_target(element: InteractiveElement) -> str | None:
    """Infer a semantic theme-toggle target from selector/id/labels."""
    if element.element_type not in (ElementType.TOGGLE, ElementType.INPUT_CHECKBOX):
        return None

    fragments = [
        (element.dom_id or "").strip(),
        (element.selector or "").strip(),
        (element.aria_label or "").strip(),
        (element.label or "").strip(),
        (element.name or "").strip(),
    ]
    joined = " ".join(fragments).lower()

    if any(hint in joined for hint in _THEME_TOGGLE_HINTS):
        return "theme toggle"
    if "toggle-track-mobile" in joined or "toggle-track-desktop" in joined:
        return "theme toggle"
    return None


def _is_meaningful_target(text: str) -> bool:
    """Return whether a discovered label is descriptive enough for reporting."""
    value = text.strip()
    if not value:
        return False
    normalized = value.lower()
    if normalized in _CLOSE_LABELS:
        return True
    if normalized in _GENERIC_LABELS:
        return False
    if len(normalized) == 1:
        return False
    return True


def _selector_hint(selector: str) -> str:
    """Produce a concise human hint from a CSS selector."""
    text = selector.strip()
    if not text:
        return "target element"
    if "#" in text:
        segment = text.split("#", 1)[1].split()[0]
        segment = segment.split(".")[0].split("[")[0]
        segment = re.sub(r"[-_](mobile|desktop)$", "", segment, flags=re.IGNORECASE)
        clean = re.sub(r"[-_]+", " ", segment).strip()
        if clean:
            return clean
    if text.startswith("[data-testid="):
        return "test-id element"
    return "target element"


def _looks_like_dismiss_button(*, label: str, target: str, selector: str) -> bool:
    """Detect dismiss/close utility buttons that hide inline messages."""
    low = " ".join((label or "", target or "", selector or "")).lower()
    if any(token in low for token in ("close", "dismiss", "alert", "toast", "error")):
        return True
    return "h3 > button" in low

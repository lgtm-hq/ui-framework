"""Interactive element discovery via accessibility tree, CSS sweep, and pattern detection."""

from __future__ import annotations

import asyncio
import logging
import re
from enum import StrEnum, auto
from hashlib import md5

from pydantic import BaseModel, Field

from flowscout.js import load_script

logger = logging.getLogger(__name__)

_CSS_BLOCK_RE = re.compile(r"\.[a-zA-Z0-9_-]+(?::[\w-]+)?\s*\{[^}]*\}")
_BRACE_RE = re.compile(r"\{[^}]*\}")
_WHITESPACE_RE = re.compile(r"\s+")


def _sanitize_label(raw: str) -> str:
    """Strip CSS pseudo-element declarations and other noise from element labels."""
    cleaned = _CSS_BLOCK_RE.sub("", raw)
    cleaned = _BRACE_RE.sub("", cleaned)
    cleaned = _WHITESPACE_RE.sub(" ", cleaned).strip()
    return cleaned


class ElementType(StrEnum):
    LINK = auto()
    BUTTON = auto()
    INPUT_TEXT = auto()
    INPUT_EMAIL = auto()
    INPUT_PASSWORD = auto()
    INPUT_NUMBER = auto()
    INPUT_TEL = auto()
    INPUT_URL = auto()
    INPUT_SEARCH = auto()
    INPUT_DATE = auto()
    INPUT_CHECKBOX = auto()
    INPUT_RADIO = auto()
    SELECT = auto()
    TEXTAREA = auto()
    TAB = auto()
    DROPDOWN_TRIGGER = auto()
    DROPDOWN_OPTION = auto()
    TOGGLE = auto()
    GENERIC_CLICKABLE = auto()


# Map HTML input type attribute to ElementType
INPUT_TYPE_MAP: dict[str, ElementType] = {
    "text": ElementType.INPUT_TEXT,
    "email": ElementType.INPUT_EMAIL,
    "password": ElementType.INPUT_PASSWORD,
    "number": ElementType.INPUT_NUMBER,
    "tel": ElementType.INPUT_TEL,
    "url": ElementType.INPUT_URL,
    "search": ElementType.INPUT_SEARCH,
    "date": ElementType.INPUT_DATE,
    "datetime-local": ElementType.INPUT_DATE,
    "checkbox": ElementType.INPUT_CHECKBOX,
    "radio": ElementType.INPUT_RADIO,
}

# Map accessibility tree roles to ElementType
A11Y_ROLE_MAP: dict[str, ElementType] = {
    "link": ElementType.LINK,
    "button": ElementType.BUTTON,
    "textbox": ElementType.INPUT_TEXT,
    "searchbox": ElementType.INPUT_SEARCH,
    "search": ElementType.GENERIC_CLICKABLE,
    "combobox": ElementType.SELECT,
    "listbox": ElementType.SELECT,
    "tab": ElementType.TAB,
    "checkbox": ElementType.INPUT_CHECKBOX,
    "radio": ElementType.INPUT_RADIO,
    "switch": ElementType.TOGGLE,
    "option": ElementType.DROPDOWN_OPTION,
    "menuitem": ElementType.DROPDOWN_OPTION,
}


class InteractiveElement(BaseModel):
    """A discovered interactive element on the page."""

    element_id: str = Field(description="Stable hash for deduplication")
    element_type: ElementType
    selector: str = Field(description="CSS selector to target this element")
    label: str = Field(description="Human-readable label")
    tag: str = Field(description="HTML tag name")
    href: str | None = None
    input_type: str | None = None
    is_required: bool = False
    is_disabled: bool = False
    is_visible: bool = True
    aria_role: str | None = None
    aria_label: str | None = None
    placeholder: str | None = None
    name: str | None = None
    value: str | None = None
    options: list[str] = Field(default_factory=list)
    parent_form_selector: str | None = None
    bounding_box: dict[str, float] | None = None
    data_attributes: dict[str, str] = Field(default_factory=dict)
    priority: int = Field(default=50)


def build_element_id(selector: str, label: str) -> str:
    """Create a stable hash ID for an element."""
    return md5(f"{selector}:{label}".encode()).hexdigest()[:12]


def classify_element(
    tag: str,
    input_type: str | None = None,
    role: str | None = None,
    aria_expanded: str | None = None,
    data_attrs: dict[str, str] | None = None,
) -> ElementType:
    """Classify an HTML element into an ElementType using heuristics."""
    data = data_attrs or {}

    # Check ARIA role first
    if role and role in A11Y_ROLE_MAP:
        return A11Y_ROLE_MAP[role]

    # Tag-based classification
    if tag == "a":
        return ElementType.LINK
    if tag == "button":
        # Check if it's a dropdown trigger
        if aria_expanded is not None:
            return ElementType.DROPDOWN_TRIGGER
        return ElementType.BUTTON
    if tag == "select":
        return ElementType.SELECT
    if tag == "textarea":
        return ElementType.TEXTAREA
    if tag == "input":
        return INPUT_TYPE_MAP.get(input_type or "text", ElementType.INPUT_TEXT)

    # Data attribute patterns
    if "data-tab" in data or "data-panel" in data:
        return ElementType.TAB

    # Elements with click handlers or cursor pointer
    if aria_expanded is not None:
        return ElementType.DROPDOWN_TRIGGER

    return ElementType.GENERIC_CLICKABLE


def compute_priority(element: InteractiveElement, base_url: str = "") -> int:
    """Compute exploration priority for an element. Lower = higher priority."""
    if element.is_disabled:
        return 100

    etype = element.element_type

    # Navigation links are top priority (discover new pages)
    if etype == ElementType.LINK and element.href:
        href = element.href
        if base_url and not href.startswith(base_url) and href.startswith("http"):
            return 90  # External link
        if href.startswith("#"):
            return 40  # Anchor link
        return 10  # Internal navigation

    # Submit/action buttons
    if etype == ElementType.BUTTON:
        text = element.label.lower()
        if any(
            w in text
            for w in (
                "submit",
                "save",
                "create",
                "add",
                "delete",
                "confirm",
                "login",
                "sign",
            )
        ):
            return 15
        if any(w in text for w in ("get started", "explore", "view", "open", "show")):
            return 20
        return 30

    # Search widgets — clicking reveals search input, a key interactive path
    if element.aria_role == "search":
        return 18

    # Form inputs
    if etype in (
        ElementType.INPUT_TEXT,
        ElementType.INPUT_EMAIL,
        ElementType.INPUT_PASSWORD,
        ElementType.INPUT_SEARCH,
    ):
        return 25

    # Tabs and dropdowns
    if etype in (ElementType.TAB, ElementType.DROPDOWN_TRIGGER):
        return 35

    # Select elements
    if etype == ElementType.SELECT:
        return 40

    # Dropdown options — high value interactive actions (select from a dropdown)
    if etype == ElementType.DROPDOWN_OPTION:
        return 15

    # Checkboxes, radios, toggles
    if etype in (
        ElementType.INPUT_CHECKBOX,
        ElementType.INPUT_RADIO,
        ElementType.TOGGLE,
    ):
        return 50

    return 55


DISCOVERY_JS = load_script("discovery")
KEYBOARD_HINTS_JS = load_script("keyboard_hints")


async def discover_elements(page: object) -> list[InteractiveElement]:
    """Discover all interactive elements on the current page.

    Uses a three-layer approach:
    1. CSS selector sweep via in-browser JavaScript
    2. Accessibility tree parsing (for additional context)
    3. Pattern detection (dropdowns, tabs, toggles)
    """
    # Layer 1: CSS selector sweep
    raw_elements = await page.evaluate(DISCOVERY_JS)  # type: ignore[union-attr]

    elements: list[InteractiveElement] = []
    for raw in raw_elements:
        etype = classify_element(
            tag=raw["tag"],
            input_type=raw.get("input_type"),
            role=raw.get("role"),
            aria_expanded=raw.get("aria_expanded"),
            data_attrs=raw.get("data_attrs", {}),
        )

        elem = InteractiveElement(
            element_id=build_element_id(raw["selector"], raw.get("label", "")),
            element_type=etype,
            selector=raw["selector"],
            label=_sanitize_label(raw.get("label", "")),
            tag=raw["tag"],
            href=raw.get("href"),
            input_type=raw.get("input_type"),
            is_required=raw.get("required", False),
            is_disabled=raw.get("disabled", False),
            is_visible=raw.get("visible", True),
            aria_role=raw.get("role"),
            aria_label=raw.get("aria_label"),
            placeholder=raw.get("placeholder"),
            name=raw.get("name"),
            value=raw.get("value"),
            options=raw.get("options", []),
            parent_form_selector=raw.get("parent_form"),
            bounding_box=raw.get("bbox"),
            data_attributes=raw.get("data_attrs", {}),
        )
        elements.append(elem)

    # Layer 2: Accessibility tree enrichment
    try:
        a11y_snapshot = await page.accessibility.snapshot()  # type: ignore[union-attr]
        if a11y_snapshot:
            _enrich_from_a11y(elements, a11y_snapshot)
    except Exception:
        logger.debug("Accessibility tree enrichment failed", exc_info=True)

    # Layer 3: Pattern detection — detect dropdown trigger/option relationships
    elements = _detect_dropdown_patterns(elements)

    # Layer 4: Click-to-reveal — open dropdown triggers to discover hidden options
    elements = await _discover_dropdown_options(page, elements)

    # Compute priorities
    base_url = str(await page.evaluate("() => window.location.origin"))  # type: ignore[union-attr]
    for elem in elements:
        elem.priority = compute_priority(elem, base_url)

    return elements


_MAX_REVEAL_TRIGGERS = 5
_OPTION_ROLES = frozenset({"option", "menuitem", "menuitemradio", "menuitemcheckbox"})


async def _discover_dropdown_options(
    page: object,
    elements: list[InteractiveElement],
) -> list[InteractiveElement]:
    """Click dropdown triggers to discover hidden options.

    Many React apps (downshift, headless-ui, radix) render dropdown options
    inside display:none containers. This clicks each visible trigger, re-runs
    discovery to find the now-visible options, then closes the dropdown.
    """
    # Dropdown triggers + SELECT elements with no native options (custom comboboxes)
    triggers = [
        e
        for e in elements
        if e.is_visible
        and (
            e.element_type == ElementType.DROPDOWN_TRIGGER
            or (
                e.element_type == ElementType.SELECT
                and not e.options
                and e.tag != "select"
            )
        )
    ]
    if not triggers:
        return elements

    # Check if visible dropdown options already exist (use list — model not hashable)
    visible_options = [
        e
        for e in elements
        if e.element_type == ElementType.DROPDOWN_OPTION and e.is_visible
    ]

    seen_selectors = {e.selector for e in elements}
    new_elements = list(elements)

    for trigger in triggers[:_MAX_REVEAL_TRIGGERS]:
        # Skip triggers that already have associated visible options
        trigger_prefix = (
            trigger.selector.rsplit(" > ", 1)[0] if " > " in trigger.selector else ""
        )
        if trigger_prefix and any(
            opt.selector.startswith(trigger_prefix) for opt in visible_options
        ):
            continue

        try:
            # Click the trigger to open the dropdown
            await page.click(trigger.selector, timeout=3000)  # type: ignore[union-attr]
            await asyncio.sleep(0.35)

            # Re-run discovery to find newly visible elements
            raw_elements = await page.evaluate(DISCOVERY_JS)  # type: ignore[union-attr]

            for raw in raw_elements:
                if not raw.get("visible", False):
                    continue
                selector = raw["selector"]
                if selector in seen_selectors:
                    continue

                role = raw.get("role", "")
                # Accept elements with option-like roles
                if role not in _OPTION_ROLES:
                    continue

                label = _sanitize_label(raw.get("label", ""))
                elem = InteractiveElement(
                    element_id=build_element_id(selector, label),
                    element_type=ElementType.DROPDOWN_OPTION,
                    selector=selector,
                    label=label,
                    tag=raw["tag"],
                    href=raw.get("href"),
                    input_type=raw.get("input_type"),
                    is_required=raw.get("required", False),
                    is_disabled=raw.get("disabled", False),
                    is_visible=True,
                    aria_role=role,
                    aria_label=raw.get("aria_label"),
                    placeholder=raw.get("placeholder"),
                    name=raw.get("name"),
                    value=raw.get("value"),
                    options=raw.get("options", []),
                    parent_form_selector=raw.get("parent_form"),
                    bounding_box=raw.get("bbox"),
                    data_attributes={
                        **raw.get("data_attrs", {}),
                        "requires_open": trigger.selector,
                    },
                )
                new_elements.append(elem)
                seen_selectors.add(selector)

            # Close the dropdown: Escape, then fallback to re-clicking trigger
            try:
                await page.keyboard.press("Escape")  # type: ignore[union-attr]
            except Exception:
                logger.debug("Failed to close dropdown via Escape", exc_info=True)
                try:
                    await page.click(trigger.selector, timeout=2000)  # type: ignore[union-attr]
                except Exception:
                    logger.debug("Failed to close dropdown by re-clicking", exc_info=True)
            await asyncio.sleep(0.2)

        except Exception:
            logger.debug(
                "Dropdown discovery failed for %s", trigger.selector, exc_info=True,
            )
            continue

    return new_elements


def _enrich_from_a11y(
    elements: list[InteractiveElement],
    a11y_node: dict,
) -> None:
    """Enrich element data with accessibility tree info."""
    name = a11y_node.get("name", "")
    role = a11y_node.get("role", "")

    # Try to match a11y nodes to discovered elements by name
    if role in A11Y_ROLE_MAP and name:
        for elem in elements:
            if elem.label == name or elem.aria_label == name:
                if not elem.aria_role:
                    elem.aria_role = role
                break

    for child in a11y_node.get("children", []):
        _enrich_from_a11y(elements, child)


def _detect_dropdown_patterns(
    elements: list[InteractiveElement],
) -> list[InteractiveElement]:
    """Detect dropdown trigger/option relationships from element patterns."""
    triggers = [e for e in elements if e.element_type == ElementType.DROPDOWN_TRIGGER]
    options = [e for e in elements if e.element_type == ElementType.DROPDOWN_OPTION]

    # If we have triggers but no options, look for options in the same
    # container (elements that share a common parent selector prefix)
    if triggers and not options:
        for trigger in triggers:
            trigger_prefix = (
                trigger.selector.rsplit(" > ", 1)[0]
                if " > " in trigger.selector
                else ""
            )
            if not trigger_prefix:
                continue
            for elem in elements:
                if (
                    elem.element_id != trigger.element_id
                    and elem.selector.startswith(trigger_prefix)
                    and elem.element_type
                    in (
                        ElementType.LINK,
                        ElementType.BUTTON,
                        ElementType.GENERIC_CLICKABLE,
                    )
                    and "data-theme" in elem.data_attributes
                ):
                    elem.element_type = ElementType.DROPDOWN_OPTION

    return elements

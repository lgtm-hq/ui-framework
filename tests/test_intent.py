"""Tests for intent modeling."""

from typing import Any

from flowscout.discovery.elements import ElementType, InteractiveElement
from flowscout.discovery.intent import (
    IntentClass,
    _build_target_description,
    infer_intent,
)


def _make_elem(**kwargs: Any) -> InteractiveElement:
    defaults: dict[str, Any] = {
        "element_id": "test",
        "element_type": ElementType.BUTTON,
        "selector": "button#test",
        "label": "Test Button",
        "tag": "button",
    }
    defaults.update(kwargs)
    return InteractiveElement.model_validate(defaults)


class TestInferIntent:
    def test_click_link_is_navigate(self) -> None:
        elem = _make_elem(element_type=ElementType.LINK, tag="a", href="/page")
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.NAVIGATE

    def test_click_button_submit_label(self) -> None:
        elem = _make_elem(label="Submit form")
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SUBMIT

    def test_click_button_navigate_label(self) -> None:
        elem = _make_elem(label="Get Started")
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.NAVIGATE

    def test_click_tab_is_select(self) -> None:
        elem = _make_elem(element_type=ElementType.TAB)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SELECT

    def test_click_dropdown_trigger_is_reveal(self) -> None:
        elem = _make_elem(element_type=ElementType.DROPDOWN_TRIGGER)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.REVEAL

    def test_click_dropdown_option_is_select(self) -> None:
        elem = _make_elem(element_type=ElementType.DROPDOWN_OPTION)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SELECT

    def test_click_toggle_is_toggle(self) -> None:
        elem = _make_elem(element_type=ElementType.TOGGLE)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.TOGGLE

    def test_click_checkbox_is_toggle(self) -> None:
        elem = _make_elem(element_type=ElementType.INPUT_CHECKBOX)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.TOGGLE

    def test_click_radio_is_select(self) -> None:
        elem = _make_elem(element_type=ElementType.INPUT_RADIO)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SELECT

    def test_click_generic_button_is_select(self) -> None:
        elem = _make_elem(label="Click me")
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SELECT

    def test_fill_is_input(self) -> None:
        elem = _make_elem(element_type=ElementType.INPUT_TEXT, tag="input")
        intent = infer_intent(elem, "fill", value="hello")
        assert intent.intent_class == IntentClass.INPUT

    def test_select_option_is_select(self) -> None:
        elem = _make_elem(element_type=ElementType.SELECT, tag="select")
        intent = infer_intent(elem, "select_option", value="opt1")
        assert intent.intent_class == IntentClass.SELECT

    def test_check_is_toggle(self) -> None:
        elem = _make_elem(element_type=ElementType.INPUT_CHECKBOX, tag="input")
        intent = infer_intent(elem, "check")
        assert intent.intent_class == IntentClass.TOGGLE

    def test_uncheck_is_toggle(self) -> None:
        elem = _make_elem(element_type=ElementType.INPUT_CHECKBOX, tag="input")
        intent = infer_intent(elem, "uncheck")
        assert intent.intent_class == IntentClass.TOGGLE

    def test_hover_is_reveal(self) -> None:
        elem = _make_elem()
        intent = infer_intent(elem, "hover")
        assert intent.intent_class == IntentClass.REVEAL

    def test_navigate_is_navigate(self) -> None:
        elem = _make_elem()
        intent = infer_intent(elem, "navigate", value="https://example.com")
        assert intent.intent_class == IntentClass.NAVIGATE

    def test_submit_form_is_submit(self) -> None:
        elem = _make_elem()
        intent = infer_intent(elem, "submit_form", form_selector="#form")
        assert intent.intent_class == IntentClass.SUBMIT

    def test_press_key_is_input(self) -> None:
        elem = _make_elem()
        intent = infer_intent(elem, "press_key", value="Enter")
        assert intent.intent_class == IntentClass.INPUT


class TestBuildTargetDescription:
    def test_prefers_aria_label(self) -> None:
        elem = _make_elem(aria_label="Close dialog", label="X", name="close_btn")
        assert _build_target_description(elem) == "Close dialog"

    def test_falls_back_to_label(self) -> None:
        elem = _make_elem(label="Submit", name="submit_btn")
        assert _build_target_description(elem) == "Submit"

    def test_falls_back_to_name(self) -> None:
        elem = _make_elem(label="", name="email")
        assert _build_target_description(elem) == "email"

    def test_falls_back_to_placeholder(self) -> None:
        elem = _make_elem(label="", name=None, placeholder="Enter email")
        assert _build_target_description(elem) == "Enter email"

    def test_falls_back_to_selector(self) -> None:
        elem = _make_elem(label="", name=None, placeholder=None)
        assert _build_target_description(elem) == "test"

    def test_generic_label_uses_selector_hint(self) -> None:
        elem = _make_elem(label="a", name=None, placeholder=None)
        assert _build_target_description(elem) == "test"

    def test_toggle_expected_effect_is_outcome_based(self) -> None:
        elem = _make_elem(element_type=ElementType.TOGGLE, label="Toggle Switch")
        intent = infer_intent(elem, "click")
        assert "state should change" in intent.expected_effect.lower()

    def test_close_glyph_maps_to_close_button_target(self) -> None:
        elem = _make_elem(label="×", aria_label=None, name=None, placeholder=None)
        assert _build_target_description(elem) == "close button"

    def test_h3_button_is_inferred_as_dismiss_intent(self) -> None:
        elem = _make_elem(
            label="",
            selector=(
                "#login_button_container > div > form"
                " > div:nth-of-type(3) > h3 > button"
            ),
            aria_label=None,
            name=None,
        )
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.REVEAL
        assert "close" in intent.expected_effect.lower()

    def test_theme_toggle_target_is_inferred_from_dom_id(self) -> None:
        elem = _make_elem(
            element_type=ElementType.INPUT_CHECKBOX,
            dom_id="toggle-track-mobile",
            selector="#toggle-track-mobile",
            label="Toggle Switch",
            aria_label=None,
            name=None,
        )
        intent = infer_intent(elem, "check")
        assert intent.target_description == "theme toggle"
        assert "enabled/checked" in intent.expected_effect

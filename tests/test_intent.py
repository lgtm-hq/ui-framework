"""Tests for intent modeling."""

from flowscout.discovery.elements import ElementType, InteractiveElement
from flowscout.discovery.intent import (
    IntentClass,
    _build_target_description,
    infer_intent,
)


def _make_elem(**kwargs) -> InteractiveElement:
    defaults = {
        "element_id": "test",
        "element_type": ElementType.BUTTON,
        "selector": "button#test",
        "label": "Test Button",
        "tag": "button",
    }
    defaults.update(kwargs)
    return InteractiveElement(**defaults)


class TestInferIntent:
    def test_click_link_is_navigate(self):
        elem = _make_elem(element_type=ElementType.LINK, tag="a", href="/page")
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.NAVIGATE

    def test_click_button_submit_label(self):
        elem = _make_elem(label="Submit form")
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SUBMIT

    def test_click_button_navigate_label(self):
        elem = _make_elem(label="Get Started")
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.NAVIGATE

    def test_click_tab_is_select(self):
        elem = _make_elem(element_type=ElementType.TAB)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SELECT

    def test_click_dropdown_trigger_is_reveal(self):
        elem = _make_elem(element_type=ElementType.DROPDOWN_TRIGGER)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.REVEAL

    def test_click_dropdown_option_is_select(self):
        elem = _make_elem(element_type=ElementType.DROPDOWN_OPTION)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SELECT

    def test_click_toggle_is_toggle(self):
        elem = _make_elem(element_type=ElementType.TOGGLE)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.TOGGLE

    def test_click_checkbox_is_toggle(self):
        elem = _make_elem(element_type=ElementType.INPUT_CHECKBOX)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.TOGGLE

    def test_click_radio_is_select(self):
        elem = _make_elem(element_type=ElementType.INPUT_RADIO)
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SELECT

    def test_click_generic_button_is_select(self):
        elem = _make_elem(label="Click me")
        intent = infer_intent(elem, "click")
        assert intent.intent_class == IntentClass.SELECT

    def test_fill_is_input(self):
        elem = _make_elem(element_type=ElementType.INPUT_TEXT, tag="input")
        intent = infer_intent(elem, "fill", value="hello")
        assert intent.intent_class == IntentClass.INPUT

    def test_select_option_is_select(self):
        elem = _make_elem(element_type=ElementType.SELECT, tag="select")
        intent = infer_intent(elem, "select_option", value="opt1")
        assert intent.intent_class == IntentClass.SELECT

    def test_check_is_toggle(self):
        elem = _make_elem(element_type=ElementType.INPUT_CHECKBOX, tag="input")
        intent = infer_intent(elem, "check")
        assert intent.intent_class == IntentClass.TOGGLE

    def test_uncheck_is_toggle(self):
        elem = _make_elem(element_type=ElementType.INPUT_CHECKBOX, tag="input")
        intent = infer_intent(elem, "uncheck")
        assert intent.intent_class == IntentClass.TOGGLE

    def test_hover_is_reveal(self):
        elem = _make_elem()
        intent = infer_intent(elem, "hover")
        assert intent.intent_class == IntentClass.REVEAL

    def test_navigate_is_navigate(self):
        elem = _make_elem()
        intent = infer_intent(elem, "navigate", value="https://example.com")
        assert intent.intent_class == IntentClass.NAVIGATE

    def test_submit_form_is_submit(self):
        elem = _make_elem()
        intent = infer_intent(elem, "submit_form", form_selector="#form")
        assert intent.intent_class == IntentClass.SUBMIT

    def test_press_key_is_input(self):
        elem = _make_elem()
        intent = infer_intent(elem, "press_key", value="Enter")
        assert intent.intent_class == IntentClass.INPUT


class TestBuildTargetDescription:
    def test_prefers_aria_label(self):
        elem = _make_elem(aria_label="Close dialog", label="X", name="close_btn")
        assert _build_target_description(elem) == "Close dialog"

    def test_falls_back_to_label(self):
        elem = _make_elem(label="Submit", name="submit_btn")
        assert _build_target_description(elem) == "Submit"

    def test_falls_back_to_name(self):
        elem = _make_elem(label="", name="email")
        assert _build_target_description(elem) == "email"

    def test_falls_back_to_placeholder(self):
        elem = _make_elem(label="", name=None, placeholder="Enter email")
        assert _build_target_description(elem) == "Enter email"

    def test_falls_back_to_selector(self):
        elem = _make_elem(label="", name=None, placeholder=None)
        assert _build_target_description(elem) == "button#test"

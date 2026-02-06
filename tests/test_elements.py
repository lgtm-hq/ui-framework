"""Tests for element discovery and classification."""

import pytest

from flowscout.discovery.elements import (
    ElementType,
    InteractiveElement,
    build_element_id,
    classify_element,
    compute_priority,
)


class TestClassifyElement:
    @pytest.mark.parametrize(
        ("tag", "kwargs", "expected"),
        [
            ("a", {}, ElementType.LINK),
            ("button", {}, ElementType.BUTTON),
            ("button", {"aria_expanded": "false"}, ElementType.DROPDOWN_TRIGGER),
            ("select", {}, ElementType.SELECT),
            ("textarea", {}, ElementType.TEXTAREA),
            ("input", {"input_type": "email"}, ElementType.INPUT_EMAIL),
            ("input", {"input_type": "password"}, ElementType.INPUT_PASSWORD),
            ("input", {"input_type": "checkbox"}, ElementType.INPUT_CHECKBOX),
            ("input", {"input_type": "radio"}, ElementType.INPUT_RADIO),
            ("input", {}, ElementType.INPUT_TEXT),
            ("div", {"role": "tab"}, ElementType.TAB),
            ("div", {"role": "button"}, ElementType.BUTTON),
            ("div", {"data_attrs": {"data-tab": "install"}}, ElementType.TAB),
            ("div", {}, ElementType.GENERIC_CLICKABLE),
        ],
        ids=[
            "link",
            "button",
            "button_aria_expanded_dropdown",
            "select",
            "textarea",
            "input_email",
            "input_password",
            "input_checkbox",
            "input_radio",
            "input_default_text",
            "role_tab",
            "role_button",
            "data_tab_attribute",
            "generic_div",
        ],
    )
    def test_classify(self, tag, kwargs, expected):
        assert classify_element(tag, **kwargs) == expected


class TestComputePriority:
    def _make_elem(self, **kwargs) -> InteractiveElement:
        defaults = {
            "element_id": "test",
            "element_type": ElementType.BUTTON,
            "selector": "button",
            "label": "Click me",
            "tag": "button",
        }
        defaults.update(kwargs)
        return InteractiveElement(**defaults)

    @pytest.mark.parametrize(
        ("elem_kwargs", "base_url", "expected_priority"),
        [
            (
                {"element_type": ElementType.LINK, "tag": "a", "href": "/themes/"},
                "https://example.com",
                10,
            ),
            (
                {
                    "element_type": ElementType.LINK,
                    "tag": "a",
                    "href": "https://github.com/other",
                },
                "https://example.com",
                90,
            ),
            (
                {"element_type": ElementType.LINK, "tag": "a", "href": "#section"},
                None,
                40,
            ),
            ({"label": "Submit form"}, None, 15),
            ({"label": "Login"}, None, 15),
            ({"label": "Click me"}, None, 30),
            ({"is_disabled": True}, None, 100),
            ({"element_type": ElementType.TAB}, None, 35),
        ],
        ids=[
            "internal_link",
            "external_link",
            "anchor_link",
            "submit_button",
            "login_button",
            "generic_button",
            "disabled",
            "tab",
        ],
    )
    def test_priority(self, elem_kwargs, base_url, expected_priority):
        elem = self._make_elem(**elem_kwargs)
        if base_url:
            assert compute_priority(elem, base_url) == expected_priority
        else:
            assert compute_priority(elem) == expected_priority


class TestBuildElementId:
    def test_deterministic(self):
        id1 = build_element_id("button#login", "Login")
        id2 = build_element_id("button#login", "Login")
        assert id1 == id2

    def test_different_inputs_different_ids(self):
        id1 = build_element_id("button#login", "Login")
        id2 = build_element_id("button#signup", "Sign Up")
        assert id1 != id2

    def test_12_chars(self):
        result = build_element_id("selector", "label")
        assert len(result) == 12

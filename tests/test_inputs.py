"""Tests for heuristic input data generation."""

import pytest

from flowscout.discovery.elements import ElementType, InteractiveElement
from flowscout.discovery.inputs import generate_input_value


def _make_input(
    input_type: str | None = None,
    name: str | None = None,
    aria_label: str | None = None,
    placeholder: str | None = None,
    label: str = "",
    element_type: ElementType = ElementType.INPUT_TEXT,
) -> InteractiveElement:
    return InteractiveElement(
        element_id="test",
        element_type=element_type,
        selector="input",
        label=label,
        tag="input",
        input_type=input_type,
        name=name,
        aria_label=aria_label,
        placeholder=placeholder,
    )


class TestGenerateInputValue:
    @pytest.mark.parametrize(
        ("kwargs", "assertion"),
        [
            ({"input_type": "email"}, lambda v: "@" in v),
            ({"input_type": "password"}, lambda v: len(v) > 5),
            ({"input_type": "tel"}, lambda v: v.startswith("+")),
            ({"input_type": "url"}, lambda v: v.startswith("https://")),
            ({"input_type": "search"}, lambda v: isinstance(v, str) and len(v) > 0),
            ({"name": "email"}, lambda v: "@" in v),
            ({"name": "zipcode"}, lambda v: v.isdigit()),
            ({"placeholder": "Enter your phone number"}, lambda v: v.startswith("+")),
        ],
        ids=[
            "email_by_type",
            "password_by_type",
            "tel_by_type",
            "url_by_type",
            "search_by_type",
            "email_by_name",
            "zip_by_name",
            "phone_by_placeholder",
        ],
    )
    def test_type_and_name_matching(self, kwargs, assertion):
        elem = _make_input(**kwargs)
        result = generate_input_value(elem)
        assert assertion(result), f"Failed for {kwargs}: got {result!r}"

    def test_username_by_name(self):
        elem = _make_input(name="username")
        result = generate_input_value(elem)
        assert len(result) >= 3, f"Username should be at least 3 chars, got {result!r}"
        assert result.strip(), f"Username should not be blank, got {result!r}"

    def test_invalid_scenario(self):
        elem = _make_input(input_type="email")
        result = generate_input_value(elem, scenario="invalid")
        assert "@" not in result

    def test_fallback_for_unknown(self):
        elem = _make_input(name="custom_field_xyz")
        result = generate_input_value(elem)
        assert result == "test input"

    def test_safe_profile_uses_safe_fallback(self):
        elem = _make_input(name="custom_field_xyz")
        result = generate_input_value(elem, input_profile="safe")
        assert result == "test input"

    def test_contextual_profile_uses_contextual_fallback(self):
        elem = _make_input(name="custom_field_xyz")
        result = generate_input_value(elem, input_profile="contextual")
        assert result == "test input value"

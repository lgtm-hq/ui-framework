"""Verify ActionMetadata typed accessor against all metadata keys in the codebase."""

from __future__ import annotations

import json

from flowscout.core.metadata import ActionMetadata
from flowscout.discovery.actions import Action, ActionType


def _action_with_metadata(meta: dict[str, str]) -> Action:
    """Create a minimal Action with the given metadata dict."""
    return Action(
        action_id="test-001",
        action_type=ActionType.CLICK,
        target_selector="button#ok",
        label="Test action",
        metadata=meta,
    )


class TestElementIdentityKeys:
    def test_selector(self) -> None:
        m = ActionMetadata(_action_with_metadata({"selector": "div.main"}))
        assert m.selector == "div.main"

    def test_dom_id(self) -> None:
        m = ActionMetadata(_action_with_metadata({"dom_id": "login-btn"}))
        assert m.dom_id == "login-btn"

    def test_name(self) -> None:
        m = ActionMetadata(_action_with_metadata({"name": "username"}))
        assert m.name == "username"

    def test_aria_label(self) -> None:
        m = ActionMetadata(_action_with_metadata({"aria_label": "Close dialog"}))
        assert m.aria_label == "Close dialog"


class TestClickKeys:
    def test_href(self) -> None:
        m = ActionMetadata(_action_with_metadata({"href": "/about"}))
        assert m.href == "/about"

    def test_is_search_true(self) -> None:
        m = ActionMetadata(_action_with_metadata({"is_search": "true"}))
        assert m.is_search is True

    def test_is_search_false_when_absent(self) -> None:
        m = ActionMetadata(_action_with_metadata({}))
        assert m.is_search is False

    def test_is_search_false_when_other_value(self) -> None:
        m = ActionMetadata(_action_with_metadata({"is_search": "false"}))
        assert m.is_search is False


class TestFillKeys:
    def test_element_type(self) -> None:
        m = ActionMetadata(_action_with_metadata({"element_type": "input_email"}))
        assert m.element_type == "input_email"

    def test_input_source(self) -> None:
        m = ActionMetadata(_action_with_metadata({"input_source": "pattern_match"}))
        assert m.input_source == "pattern_match"

    def test_input_profile(self) -> None:
        m = ActionMetadata(_action_with_metadata({"input_profile": "safe"}))
        assert m.input_profile == "safe"


class TestDropdownKeys:
    def test_requires_open(self) -> None:
        m = ActionMetadata(
            _action_with_metadata({"requires_open": "button#dropdown-trigger"})
        )
        assert m.requires_open == "button#dropdown-trigger"

    def test_is_dropdown_option(self) -> None:
        m = ActionMetadata(_action_with_metadata({"requires_open": "button#trigger"}))
        assert m.is_dropdown_option is True

    def test_is_not_dropdown_option(self) -> None:
        m = ActionMetadata(_action_with_metadata({}))
        assert m.is_dropdown_option is False


class TestFormSubmissionKeys:
    def test_field_values_parses_json(self) -> None:
        vals = {"input#email": "test@example.com", "input#pass": "secret"}
        m = ActionMetadata(
            _action_with_metadata({"field_values_json": json.dumps(vals)})
        )
        assert m.field_values == vals

    def test_field_values_empty_on_missing(self) -> None:
        m = ActionMetadata(_action_with_metadata({}))
        assert m.field_values == {}

    def test_field_values_empty_on_malformed_json(self) -> None:
        m = ActionMetadata(_action_with_metadata({"field_values_json": "not json!!!"}))
        assert m.field_values == {}

    def test_field_sources_parses_json(self) -> None:
        sources = {"input#email": "pattern_match"}
        m = ActionMetadata(
            _action_with_metadata({"field_sources_json": json.dumps(sources)})
        )
        assert m.field_sources == sources

    def test_field_sources_empty_on_missing(self) -> None:
        m = ActionMetadata(_action_with_metadata({}))
        assert m.field_sources == {}

    def test_form_selector(self) -> None:
        m = ActionMetadata(_action_with_metadata({"form_selector": "#login-form"}))
        assert m.form_selector == "#login-form"

    def test_scenario(self) -> None:
        m = ActionMetadata(_action_with_metadata({"scenario": "invalid"}))
        assert m.scenario == "invalid"

    def test_is_invalid_scenario(self) -> None:
        m = ActionMetadata(_action_with_metadata({"scenario": "invalid"}))
        assert m.is_invalid_scenario is True

    def test_is_not_invalid_scenario(self) -> None:
        m = ActionMetadata(_action_with_metadata({"scenario": "valid"}))
        assert m.is_invalid_scenario is False

    def test_expected_outcome(self) -> None:
        m = ActionMetadata(
            _action_with_metadata({"expected_outcome": "validation_error"})
        )
        assert m.expected_outcome == "validation_error"


class TestPolicyKeys:
    def test_url(self) -> None:
        m = ActionMetadata(_action_with_metadata({"url": "http://example.com/page"}))
        assert m.url == "http://example.com/page"


class TestDefaults:
    """All properties return sensible empty defaults when key is absent."""

    def test_all_string_defaults_are_empty(self) -> None:
        m = ActionMetadata(_action_with_metadata({}))
        assert m.selector == ""
        assert m.dom_id == ""
        assert m.name == ""
        assert m.aria_label == ""
        assert m.href == ""
        assert m.element_type == ""
        assert m.input_source == ""
        assert m.input_profile == ""
        assert m.requires_open == ""
        assert m.form_selector == ""
        assert m.scenario == ""
        assert m.expected_outcome == ""
        assert m.url == ""

    def test_bool_defaults_are_false(self) -> None:
        m = ActionMetadata(_action_with_metadata({}))
        assert m.is_search is False
        assert m.is_invalid_scenario is False
        assert m.is_dropdown_option is False

    def test_dict_defaults_are_empty(self) -> None:
        m = ActionMetadata(_action_with_metadata({}))
        assert m.field_values == {}
        assert m.field_sources == {}


class TestEscapeHatch:
    def test_get_returns_value(self) -> None:
        m = ActionMetadata(_action_with_metadata({"custom_key": "custom_val"}))
        assert m.get("custom_key") == "custom_val"

    def test_get_returns_default(self) -> None:
        m = ActionMetadata(_action_with_metadata({}))
        assert m.get("missing", "fallback") == "fallback"

    def test_contains(self) -> None:
        m = ActionMetadata(_action_with_metadata({"is_search": "true"}))
        assert "is_search" in m
        assert "missing" not in m

    def test_repr(self) -> None:
        m = ActionMetadata(_action_with_metadata({"selector": "a"}))
        assert "ActionMetadata" in repr(m)
        assert "'selector'" in repr(m)

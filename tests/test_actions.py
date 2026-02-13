"""Tests for action generation."""

import json
from typing import Any

from flowscout.discovery.actions import (
    ActionType,
    build_action_id,
    generate_actions,
    generate_form_submit_actions,
)
from flowscout.discovery.elements import ElementType, InteractiveElement


def _make_elem(**kwargs: Any) -> InteractiveElement:
    defaults: dict[str, Any] = {
        "element_id": "test",
        "element_type": ElementType.BUTTON,
        "selector": "button#test",
        "label": "Test",
        "tag": "button",
        "is_visible": True,
        "is_disabled": False,
    }
    defaults.update(kwargs)
    return InteractiveElement.model_validate(defaults)


class TestGenerateActions:
    def test_button_generates_click(self) -> None:
        elem = _make_elem()
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CLICK

    def test_link_generates_click(self) -> None:
        elem = _make_elem(
            element_type=ElementType.LINK,
            tag="a",
            href="/page",
        )
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CLICK
        assert actions[0].metadata["href"] == "/page"

    def test_external_link_filtered(self) -> None:
        elem = _make_elem(
            element_type=ElementType.LINK,
            tag="a",
            href="https://external.com/page",
        )
        actions = generate_actions([elem], base_url="https://mysite.com")
        assert len(actions) == 0

    def test_input_generates_fill(self) -> None:
        elem = _make_elem(
            element_type=ElementType.INPUT_EMAIL,
            tag="input",
            input_type="email",
            name="email",
        )
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.FILL
        assert "@" in (actions[0].value or "")
        assert actions[0].metadata["input_profile"] == "safe"
        assert "input_source" in actions[0].metadata

    def test_select_generates_option_actions(self) -> None:
        elem = _make_elem(
            element_type=ElementType.SELECT,
            tag="select",
            options=["a", "b", "c"],
        )
        actions = generate_actions([elem])
        assert len(actions) == 3
        assert all(a.action_type == ActionType.SELECT_OPTION for a in actions)

    def test_disabled_element_skipped(self) -> None:
        elem = _make_elem(is_disabled=True)
        actions = generate_actions([elem])
        assert len(actions) == 0

    def test_invisible_element_skipped(self) -> None:
        elem = _make_elem(is_visible=False)
        actions = generate_actions([elem])
        assert len(actions) == 0

    def test_checkbox_generates_check(self) -> None:
        elem = _make_elem(
            element_type=ElementType.INPUT_CHECKBOX,
            tag="input",
            input_type="checkbox",
        )
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CHECK

    def test_action_metadata_includes_dom_id_when_present(self) -> None:
        elem = _make_elem(
            element_type=ElementType.INPUT_CHECKBOX,
            tag="input",
            input_type="checkbox",
            dom_id="toggle-track-desktop",
            selector="#toggle-track-desktop",
        )
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].metadata["dom_id"] == "toggle-track-desktop"
        assert actions[0].metadata["selector"] == "#toggle-track-desktop"

    def test_tab_generates_click(self) -> None:
        elem = _make_elem(element_type=ElementType.TAB)
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CLICK

    def test_low_signal_icon_button_is_skipped(self) -> None:
        elem = _make_elem(
            label="",
            aria_label=None,
            name=None,
            selector="#container > div:nth-of-type(3) > button",
        )
        actions = generate_actions([elem])
        assert actions == []

    def test_sorted_by_priority(self) -> None:
        link = _make_elem(
            element_id="link1",
            element_type=ElementType.LINK,
            selector="a#link",
            tag="a",
            href="/page",
            priority=10,
        )
        button = _make_elem(
            element_id="btn1",
            selector="button#btn",
            priority=30,
        )
        actions = generate_actions([button, link])
        assert actions[0].target_selector == "a#link"


class TestBuildActionId:
    def test_deterministic(self) -> None:
        id1 = build_action_id("button#x", "click")
        id2 = build_action_id("button#x", "click")
        assert id1 == id2

    def test_different_inputs(self) -> None:
        id1 = build_action_id("button#x", "click")
        id2 = build_action_id("button#y", "click")
        assert id1 != id2


class TestEdgeCases:
    def test_empty_element_list(self) -> None:
        actions = generate_actions([])
        assert actions == []

    def test_all_disabled_elements(self) -> None:
        elems = [
            _make_elem(element_id="d1", is_disabled=True),
            _make_elem(element_id="d2", is_disabled=True),
        ]
        actions = generate_actions(elems)
        assert actions == []

    def test_all_invisible_elements(self) -> None:
        elems = [
            _make_elem(element_id="h1", is_visible=False),
            _make_elem(element_id="h2", is_visible=False),
        ]
        actions = generate_actions(elems)
        assert actions == []

    def test_intent_attached_to_actions(self) -> None:
        elem = _make_elem(
            element_type=ElementType.LINK,
            tag="a",
            href="/page",
        )
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].intent is not None
        assert actions[0].intent.intent_class == "navigate"
        assert "navigate" in actions[0].intent.expected_effect.lower()


class TestGenerateFormSubmitActions:
    def test_groups_elements_by_form(self) -> None:
        email = _make_elem(
            element_id="e1",
            element_type=ElementType.INPUT_EMAIL,
            tag="input",
            input_type="email",
            name="email",
            selector='#form input[name="email"]',
            parent_form_selector="#form",
        )
        submit = _make_elem(
            element_id="s1",
            selector="#form button",
            label="Submit",
            parent_form_selector="#form",
        )
        actions = generate_form_submit_actions([email, submit])
        assert len(actions) == 1
        assert all(a.action_type == ActionType.SUBMIT_FORM for a in actions)

    def test_field_values_contain_input_data(self) -> None:
        email = _make_elem(
            element_id="e1",
            element_type=ElementType.INPUT_EMAIL,
            tag="input",
            input_type="email",
            name="email",
            selector='#f input[name="email"]',
            parent_form_selector="#f",
        )
        submit = _make_elem(
            element_id="s1",
            selector="#f button",
            label="Submit",
            parent_form_selector="#f",
        )
        actions = generate_form_submit_actions([email, submit])
        fields = json.loads(actions[0].metadata["field_values_json"])
        assert '#f input[name="email"]' in fields
        assert "@" in fields['#f input[name="email"]']

    def test_invalid_submission_empties_required_in_negative_profile(self) -> None:
        email = _make_elem(
            element_id="e1",
            element_type=ElementType.INPUT_EMAIL,
            tag="input",
            input_type="email",
            name="email",
            selector='#f input[name="email"]',
            parent_form_selector="#f",
            is_required=True,
        )
        submit = _make_elem(
            element_id="s1",
            selector="#f button",
            label="Submit",
            parent_form_selector="#f",
        )
        actions = generate_form_submit_actions(
            [email, submit], input_profile="negative"
        )
        invalid = [a for a in actions if a.metadata.get("scenario") == "invalid"]
        assert len(invalid) == 1
        fields = json.loads(invalid[0].metadata["field_values_json"])
        assert fields['#f input[name="email"]'] == ""

    def test_safe_profile_skips_invalid_submission(self) -> None:
        email = _make_elem(
            element_id="e1",
            element_type=ElementType.INPUT_EMAIL,
            tag="input",
            input_type="email",
            name="email",
            selector='#f input[name="email"]',
            parent_form_selector="#f",
            is_required=True,
        )
        submit = _make_elem(
            element_id="s1",
            selector="#f button",
            label="Submit",
            parent_form_selector="#f",
        )
        actions = generate_form_submit_actions([email, submit], input_profile="safe")
        invalid = [a for a in actions if a.metadata.get("scenario") == "invalid"]
        assert invalid == []

    def test_no_elements_returns_empty(self) -> None:
        assert generate_form_submit_actions([]) == []

    def test_form_without_explicit_submit(self) -> None:
        email = _make_elem(
            element_id="e1",
            element_type=ElementType.INPUT_EMAIL,
            tag="input",
            input_type="email",
            name="email",
            selector='#f input[name="email"]',
            parent_form_selector="#f",
        )
        btn = _make_elem(
            element_id="b1",
            selector="#f button",
            label="Go",
            parent_form_selector="#f",
        )
        actions = generate_form_submit_actions([email, btn])
        assert len(actions) >= 1

    def test_intent_is_submit(self) -> None:
        email = _make_elem(
            element_id="e1",
            element_type=ElementType.INPUT_EMAIL,
            tag="input",
            input_type="email",
            name="email",
            selector='#f input[name="email"]',
            parent_form_selector="#f",
        )
        submit = _make_elem(
            element_id="s1",
            selector="#f button",
            label="Submit",
            parent_form_selector="#f",
        )
        actions = generate_form_submit_actions([email, submit])
        for action in actions:
            assert action.intent is not None
            assert action.intent.intent_class == "submit"

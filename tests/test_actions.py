"""Tests for action generation."""

from flowscout.discovery.actions import (
    ActionType,
    build_action_id,
    generate_actions,
)
from flowscout.discovery.elements import ElementType, InteractiveElement


def _make_elem(**kwargs) -> InteractiveElement:
    defaults = {
        "element_id": "test",
        "element_type": ElementType.BUTTON,
        "selector": "button#test",
        "label": "Test",
        "tag": "button",
        "is_visible": True,
        "is_disabled": False,
    }
    defaults.update(kwargs)
    return InteractiveElement(**defaults)


class TestGenerateActions:
    def test_button_generates_click(self):
        elem = _make_elem()
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CLICK

    def test_link_generates_click(self):
        elem = _make_elem(
            element_type=ElementType.LINK,
            tag="a",
            href="/page",
        )
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CLICK

    def test_external_link_filtered(self):
        elem = _make_elem(
            element_type=ElementType.LINK,
            tag="a",
            href="https://external.com/page",
        )
        actions = generate_actions([elem], base_url="https://mysite.com")
        assert len(actions) == 0

    def test_input_generates_fill(self):
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

    def test_select_generates_option_actions(self):
        elem = _make_elem(
            element_type=ElementType.SELECT,
            tag="select",
            options=["a", "b", "c"],
        )
        actions = generate_actions([elem])
        assert len(actions) == 3
        assert all(a.action_type == ActionType.SELECT_OPTION for a in actions)

    def test_disabled_element_skipped(self):
        elem = _make_elem(is_disabled=True)
        actions = generate_actions([elem])
        assert len(actions) == 0

    def test_invisible_element_skipped(self):
        elem = _make_elem(is_visible=False)
        actions = generate_actions([elem])
        assert len(actions) == 0

    def test_checkbox_generates_check(self):
        elem = _make_elem(
            element_type=ElementType.INPUT_CHECKBOX,
            tag="input",
            input_type="checkbox",
        )
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CHECK

    def test_tab_generates_click(self):
        elem = _make_elem(element_type=ElementType.TAB)
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CLICK

    def test_sorted_by_priority(self):
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
    def test_deterministic(self):
        id1 = build_action_id("button#x", "click")
        id2 = build_action_id("button#x", "click")
        assert id1 == id2

    def test_different_inputs(self):
        id1 = build_action_id("button#x", "click")
        id2 = build_action_id("button#y", "click")
        assert id1 != id2


class TestEdgeCases:
    def test_empty_element_list(self):
        actions = generate_actions([])
        assert actions == []

    def test_all_disabled_elements(self):
        elems = [
            _make_elem(element_id="d1", is_disabled=True),
            _make_elem(element_id="d2", is_disabled=True),
        ]
        actions = generate_actions(elems)
        assert actions == []

    def test_all_invisible_elements(self):
        elems = [
            _make_elem(element_id="h1", is_visible=False),
            _make_elem(element_id="h2", is_visible=False),
        ]
        actions = generate_actions(elems)
        assert actions == []

    def test_intent_attached_to_actions(self):
        elem = _make_elem(
            element_type=ElementType.LINK,
            tag="a",
            href="/page",
        )
        actions = generate_actions([elem])
        assert len(actions) == 1
        assert actions[0].intent is not None
        assert actions[0].intent.intent_class is not None

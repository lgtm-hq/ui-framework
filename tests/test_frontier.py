"""Tests for FrontierManager — priority, diversity, and group deprioritization."""

from __future__ import annotations

import pytest

from flowscout.core.frontier import FrontierManager, is_diverse_action
from flowscout.discovery.actions import Action, ActionType, OutcomeType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _action(
    action_id: str = "a1",
    action_type: ActionType = ActionType.CLICK,
    label: str = "Click: button",
    priority: int = 50,
    metadata: dict[str, str] | None = None,
) -> Action:
    return Action(
        action_id=action_id,
        action_type=action_type,
        target_selector=f"#{action_id}",
        label=label,
        metadata=metadata or {},
        priority=priority,
    )


# ---------------------------------------------------------------------------
# Basic push / pop
# ---------------------------------------------------------------------------

class TestBasicOperations:

    def test_push_and_pop_single(self):
        fm = FrontierManager()
        a = _action("a1")
        fm.push(a, "s1", 10)
        assert fm.size == 1
        item = fm.pop()
        assert item.action.action_id == "a1"
        assert fm.is_empty

    def test_pop_priority_order(self):
        fm = FrontierManager()
        fm.push(_action("low"), "s1", 50)
        fm.push(_action("high"), "s1", 10)
        fm.push(_action("mid"), "s1", 30)

        assert fm.pop().action.action_id == "high"
        assert fm.pop().action.action_id == "mid"
        assert fm.pop().action.action_id == "low"

    def test_is_empty_initially(self):
        fm = FrontierManager()
        assert fm.is_empty
        assert fm.size == 0


# ---------------------------------------------------------------------------
# Visited tracking
# ---------------------------------------------------------------------------

class TestVisitedTracking:

    def test_mark_and_check_visited(self):
        fm = FrontierManager()
        assert not fm.is_visited("s1", "a1")
        fm.mark_visited("s1", "a1")
        assert fm.is_visited("s1", "a1")

    def test_different_state_not_visited(self):
        fm = FrontierManager()
        fm.mark_visited("s1", "a1")
        assert not fm.is_visited("s2", "a1")

    def test_different_action_not_visited(self):
        fm = FrontierManager()
        fm.mark_visited("s1", "a1")
        assert not fm.is_visited("s1", "a2")


# ---------------------------------------------------------------------------
# Diversity rotation
# ---------------------------------------------------------------------------

class TestDiversityRotation:

    def test_diversity_kicks_in_after_interval(self):
        """After N consecutive clicks, a diverse action is preferred."""
        fm = FrontierManager(diversity_interval=3)

        # Pop 3 click actions to trigger diversity
        for i in range(3):
            fm.push(_action(f"click-{i}", ActionType.CLICK), "s1", 10)
        for _ in range(3):
            fm.pop()

        # Now push a click at priority 5 and a fill at priority 50
        fm.push(_action("click-next", ActionType.CLICK, priority=5), "s1", 5)
        fm.push(
            _action("fill-1", ActionType.FILL, label="Fill: email", priority=50),
            "s1",
            50,
        )

        # Diversity should prefer the fill even though click has lower priority
        item = fm.pop()
        assert item.action.action_type == ActionType.FILL

    def test_no_diversity_when_only_clicks_available(self):
        """If no diverse actions exist, clicks still pop normally."""
        fm = FrontierManager(diversity_interval=2)

        for i in range(3):
            fm.push(_action(f"click-{i}", ActionType.CLICK), "s1", 10 + i)
        for _ in range(2):
            fm.pop()

        # Only clicks left — should still pop
        item = fm.pop()
        assert item.action.action_type == ActionType.CLICK

    def test_category_rotation(self):
        """Diversity rotates between categories (search, dropdown, input, form)."""
        fm = FrontierManager(diversity_interval=1)

        # One click to trigger diversity
        fm.push(_action("click-0", ActionType.CLICK), "s1", 10)
        fm.pop()

        # Push search and input with same priority
        fm.push(
            _action("search", ActionType.CLICK, metadata={"is_search": "true"}),
            "s1",
            20,
        )
        fm.push(
            _action("fill", ActionType.FILL, label="Fill: name"),
            "s1",
            20,
        )

        # First diverse pick
        first = fm.pop()
        first_category = first.action.action_id

        # Push another click to re-trigger diversity
        fm.push(_action("click-1", ActionType.CLICK), "s1", 10)
        fm.pop()  # pops click

        # Push both categories again
        fm.push(
            _action("search-2", ActionType.CLICK, metadata={"is_search": "true"}),
            "s1",
            20,
        )
        fm.push(
            _action("fill-2", ActionType.FILL, label="Fill: email"),
            "s1",
            20,
        )

        # Should rotate to the other category
        second = fm.pop()
        assert second.action.action_id != first_category


# ---------------------------------------------------------------------------
# Group deprioritization
# ---------------------------------------------------------------------------

class TestGroupDeprioritization:

    def test_no_deprioritization_initially(self):
        fm = FrontierManager()
        a = _action(label="Theme: dark", priority=30)
        assert fm.adjusted_priority(a) == 30

    def test_deprioritizes_after_three_dom_changes(self):
        fm = FrontierManager()
        a = _action(label="Theme: dark", priority=30)

        # Simulate 3 DOM_CHANGE outcomes in same group
        for _ in range(3):
            fm.track_outcome(
                _action(label="Theme: light", priority=30),
                OutcomeType.DOM_CHANGE,
            )

        assert fm.adjusted_priority(a) == 80

    def test_no_deprioritization_if_navigation_exists(self):
        fm = FrontierManager()
        a = _action(label="Theme: dark", priority=30)

        fm.track_outcome(
            _action(label="Theme: light", priority=30),
            OutcomeType.DOM_CHANGE,
        )
        fm.track_outcome(
            _action(label="Theme: solarized", priority=30),
            OutcomeType.DOM_CHANGE,
        )
        fm.track_outcome(
            _action(label="Theme: nord", priority=30),
            OutcomeType.DOM_CHANGE,
        )
        fm.track_outcome(
            _action(label="Theme: gruvbox", priority=30),
            OutcomeType.NAVIGATION,
        )

        # Navigation exists, so no deprioritization
        assert fm.adjusted_priority(a) == 30

    def test_no_deprioritization_without_label_prefix(self):
        fm = FrontierManager()
        a = _action(label="Submit", priority=30)
        # No colon in label → no group → no deprioritization
        assert fm.adjusted_priority(a) == 30


# ---------------------------------------------------------------------------
# Priority overrides
# ---------------------------------------------------------------------------

class TestPriorityOverrides:

    def test_search_priority_override(self):
        fm = FrontierManager()
        fm.push(
            _action("search", ActionType.CLICK, metadata={"is_search": "true"}),
            "s1",
            50,
        )
        fm.push(_action("nav", ActionType.CLICK), "s1", 10)

        fm.apply_priority_overrides("s1", {"__search_action__": 1}, is_saturated=False)

        # Search should now be highest priority
        item = fm.pop()
        assert item.action.action_id == "search"

    def test_content_priority_override(self):
        fm = FrontierManager()
        fm.push(_action("content-click", ActionType.CLICK), "s1", 40)
        fm.push(_action("nav-link", ActionType.CLICK), "s1", 10)

        fm.apply_priority_overrides("s1", {"__content_items__": 5}, is_saturated=False)

        item = fm.pop()
        assert item.action.action_id == "content-click"

    def test_saturated_priority_override(self):
        fm = FrontierManager()
        fm.push(_action("a1", ActionType.CLICK), "s1", 10)

        fm.apply_priority_overrides("s1", {"__saturated__": 90}, is_saturated=True)

        item = fm.pop()
        assert item.priority == 90

    def test_override_only_affects_target_state(self):
        fm = FrontierManager()
        fm.push(_action("a1", ActionType.CLICK), "s1", 10)
        fm.push(_action("a2", ActionType.CLICK), "s2", 10)

        fm.apply_priority_overrides("s1", {"__saturated__": 90}, is_saturated=True)

        # s2 item should be unaffected
        item = fm.pop()
        assert item.source_state_id == "s2"
        assert item.priority == 10


# ---------------------------------------------------------------------------
# State action count
# ---------------------------------------------------------------------------

class TestStateActionCount:

    def test_count_increments_on_push(self):
        fm = FrontierManager()
        assert fm.state_action_count("s1") == 0
        fm.push(_action("a1"), "s1", 10)
        assert fm.state_action_count("s1") == 1
        fm.push(_action("a2"), "s1", 20)
        assert fm.state_action_count("s1") == 2

    def test_count_per_state(self):
        fm = FrontierManager()
        fm.push(_action("a1"), "s1", 10)
        fm.push(_action("a2"), "s2", 10)
        assert fm.state_action_count("s1") == 1
        assert fm.state_action_count("s2") == 1


# ---------------------------------------------------------------------------
# is_diverse_action helper
# ---------------------------------------------------------------------------

class TestIsDiverseAction:

    def test_fill_is_diverse(self):
        assert is_diverse_action(_action(action_type=ActionType.FILL))

    def test_click_is_not_diverse(self):
        assert not is_diverse_action(_action(action_type=ActionType.CLICK))

    def test_search_click_is_diverse(self):
        assert is_diverse_action(
            _action(action_type=ActionType.CLICK, metadata={"is_search": "true"}),
        )

    def test_dropdown_click_is_diverse(self):
        assert is_diverse_action(
            _action(action_type=ActionType.CLICK, metadata={"requires_open": "#menu"}),
        )

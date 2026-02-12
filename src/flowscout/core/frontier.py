"""Priority frontier with diversity-aware popping."""

from __future__ import annotations

import heapq
from collections import defaultdict

from flowscout.discovery.actions import Action, ActionType, OutcomeType

# After this many consecutive click actions, prefer a non-click if available
_DIVERSITY_INTERVAL = 5

# Action types that count as "interactive" (non-navigation) diversity
_DIVERSE_TYPES = frozenset(
    {
        ActionType.FILL,
        ActionType.SELECT_OPTION,
        ActionType.CHECK,
        ActionType.UNCHECK,
        ActionType.SUBMIT_FORM,
    }
)

# Individual input actions preferred over form submits for diversity picks
_INPUT_TYPES = frozenset(
    {
        ActionType.FILL,
        ActionType.SELECT_OPTION,
        ActionType.CHECK,
        ActionType.UNCHECK,
    }
)


class _FrontierItem:
    """Wrapper for priority queue items (needed for heap comparison)."""

    def __init__(self, priority: int, action: Action, source_state_id: str) -> None:
        self.priority = priority
        self.action = action
        self.source_state_id = source_state_id

    def __lt__(self, other: _FrontierItem) -> bool:
        return self.priority < other.priority


class FrontierManager:
    """Priority-based frontier with diversity rotation and group deprioritization."""

    def __init__(self, *, diversity_interval: int = _DIVERSITY_INTERVAL) -> None:
        self._frontier: list[_FrontierItem] = []
        self._visited: set[tuple[str, str]] = set()
        self._state_action_count: dict[str, int] = defaultdict(int)
        self._group_outcome_count: dict[str, dict[str, int]] = defaultdict(
            lambda: defaultdict(int),
        )
        self._click_streak = 0
        self._last_diverse_category: str | None = None
        self._diversity_interval = diversity_interval

    # ── Public API ──

    @property
    def is_empty(self) -> bool:
        return len(self._frontier) == 0

    @property
    def size(self) -> int:
        return len(self._frontier)

    def push(self, action: Action, source_state_id: str, priority: int) -> None:
        """Add an action to the frontier."""
        heapq.heappush(
            self._frontier,
            _FrontierItem(priority, action, source_state_id),
        )
        self._state_action_count[source_state_id] += 1

    def pop(self) -> _FrontierItem:
        """Pop the next item with diversity awareness.

        After ``diversity_interval`` consecutive click actions, prefer a
        non-click action if one exists.  Rotates between diverse categories
        (search, dropdown, input, form) to prevent one type from monopolizing.
        """
        if self._click_streak >= self._diversity_interval:
            item = self._find_diverse_candidate()
            if item is not None:
                return item

        item = heapq.heappop(self._frontier)
        if item.action.action_type == ActionType.CLICK and not _is_diverse_item(item):
            self._click_streak += 1
        else:
            self._click_streak = 0
        return item

    def mark_visited(self, state_id: str, action_id: str) -> None:
        self._visited.add((state_id, action_id))

    def is_visited(self, state_id: str, action_id: str) -> bool:
        return (state_id, action_id) in self._visited

    def state_action_count(self, state_id: str) -> int:
        return self._state_action_count[state_id]

    def track_outcome(self, action: Action, result_outcome: OutcomeType) -> None:
        """Track outcomes by action group for smart deprioritization."""
        label_prefix = action.label.split(":")[0] if ":" in action.label else ""
        if label_prefix:
            self._group_outcome_count[label_prefix][result_outcome.value] += 1

    def adjusted_priority(self, action: Action) -> int:
        """Adjust priority based on group outcome history.

        If we've seen 3+ actions in a group all produce DOM_CHANGE (not
        NAVIGATION), deprioritize remaining actions in that group.
        """
        label_prefix = action.label.split(":")[0] if ":" in action.label else ""
        if not label_prefix:
            return int(action.priority)

        group_outcomes = self._group_outcome_count.get(label_prefix)
        if not group_outcomes:
            return int(action.priority)

        dom_changes = group_outcomes.get(OutcomeType.DOM_CHANGE.value, 0)
        navigations = group_outcomes.get(OutcomeType.NAVIGATION.value, 0)

        if dom_changes >= 3 and navigations == 0:
            return max(int(action.priority), 80)

        return int(action.priority)

    def apply_priority_overrides(
        self,
        state_id: str,
        overrides: dict[str, int],
        is_saturated: bool,
    ) -> None:
        """Apply smart-mode priority overrides to frontier items for a state."""
        saturated_priority = overrides.get("__saturated__")
        search_priority = overrides.get("__search_action__")
        content_priority = overrides.get("__content_items__")

        modified = False
        for item in self._frontier:
            if item.source_state_id != state_id:
                continue

            if search_priority is not None:
                if item.action.meta.is_search:
                    item.priority = search_priority
                    modified = True
                elif item.action.meta.element_type == "input_search":
                    item.priority = search_priority
                    modified = True

            if content_priority is not None:
                if (
                    item.action.action_type == ActionType.CLICK
                    and not item.action.meta.is_search
                    and item.action.meta.element_type != "input_search"
                ):
                    item.priority = min(item.priority, content_priority)
                    modified = True

            if saturated_priority is not None and is_saturated:
                item.priority = max(item.priority, saturated_priority)
                modified = True

        if modified:
            heapq.heapify(self._frontier)

    # ── Internal ──

    def _find_diverse_candidate(self) -> _FrontierItem | None:
        """Find the best diverse candidate across three passes."""
        best_idx: int | None = None
        best_priority = float("inf")

        # Pass 1: prefer a DIFFERENT category than the last pick
        for i, candidate in enumerate(self._frontier):
            cat = _diverse_category(candidate)
            if cat is None:
                continue
            if cat == self._last_diverse_category:
                continue
            if candidate.priority < best_priority:
                best_idx = i
                best_priority = candidate.priority

        # Pass 2: any diverse candidate (no category restriction)
        if best_idx is None:
            for i, candidate in enumerate(self._frontier):
                cat = _diverse_category(candidate)
                if cat is None:
                    continue
                if candidate.priority < best_priority:
                    best_idx = i
                    best_priority = candidate.priority

        # Pass 3: any diverse type (including SUBMIT_FORM)
        if best_idx is None:
            for i, candidate in enumerate(self._frontier):
                if _is_diverse_item(candidate) and candidate.priority < best_priority:
                    best_idx = i
                    best_priority = candidate.priority

        if best_idx is None:
            return None

        item = self._frontier[best_idx]
        self._last_diverse_category = _diverse_category(item)
        # Remove from heap: swap with last, pop, re-heapify
        self._frontier[best_idx] = self._frontier[-1]
        self._frontier.pop()
        if self._frontier:
            heapq.heapify(self._frontier)
        self._click_streak = 0
        return item


def _is_diverse_item(item: _FrontierItem) -> bool:
    """Check if a frontier item is a diverse (non-navigation) action."""
    if item.action.action_type in _DIVERSE_TYPES:
        return True
    if item.action.meta.is_search:
        return True
    if item.action.meta.is_dropdown_option:
        return True
    return False


def _diverse_category(item: _FrontierItem) -> str | None:
    """Classify a frontier item's diverse category for rotation."""
    if item.action.meta.is_search:
        return "search"
    if item.action.meta.is_dropdown_option:
        return "dropdown"
    if item.action.action_type in _INPUT_TYPES:
        return "input"
    if item.action.action_type in _DIVERSE_TYPES:
        return "form"
    return None


def is_diverse_action(action: Action) -> bool:
    """Check whether an action should count as diverse for budgeting."""
    if action.action_type in _DIVERSE_TYPES:
        return True
    if action.meta.is_search:
        return True
    if action.meta.is_dropdown_option:
        return True
    return False

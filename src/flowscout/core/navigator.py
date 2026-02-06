"""Priority-BFS exploration engine."""

from __future__ import annotations

import heapq
import time
from collections import defaultdict
from datetime import datetime, timezone

from flowscout.analysis.graph import ExplorationGraph, ExplorationResult, Flow
from flowscout.analysis.narrative import NarrativeGenerator
from flowscout.analysis.verdict import VerdictComputer
from flowscout.core.browser import BrowserManager
from flowscout.core.state import ExplorerConfig, PageState
from flowscout.discovery.actions import (
    Action,
    ActionResult,
    ActionType,
    OutcomeType,
    generate_actions,
    generate_form_submit_actions,
)
from flowscout.discovery.elements import discover_elements
from flowscout.reporting.terminal import TerminalReporter


# After this many consecutive click actions, prefer a non-click if available
_DIVERSITY_INTERVAL = 5

# Action types that count as "interactive" (non-navigation) diversity
_DIVERSE_TYPES = frozenset({
    ActionType.FILL,
    ActionType.SELECT_OPTION,
    ActionType.CHECK,
    ActionType.UNCHECK,
    ActionType.SUBMIT_FORM,
})

# Individual input actions preferred over form submits for diversity picks
# (filling a search box or selecting an option is more interesting than
# a composite submit which may timeout on forms without clear submit buttons)
_INPUT_TYPES = frozenset({
    ActionType.FILL,
    ActionType.SELECT_OPTION,
    ActionType.CHECK,
    ActionType.UNCHECK,
})


class _FrontierItem:
    """Wrapper for priority queue items (needed for heap comparison)."""

    def __init__(self, priority: int, action: Action, source_state_id: str) -> None:
        self.priority = priority
        self.action = action
        self.source_state_id = source_state_id

    def __lt__(self, other: _FrontierItem) -> bool:
        return self.priority < other.priority


class Navigator:
    """The exploration engine that decides what to do next."""

    def __init__(
        self,
        browser: BrowserManager,
        graph: ExplorationGraph,
        config: ExplorerConfig,
        terminal: TerminalReporter,
    ) -> None:
        self.browser = browser
        self.graph = graph
        self.config = config
        self.terminal = terminal
        self._frontier: list[_FrontierItem] = []
        self._visited: set[tuple[str, str]] = set()  # (state_id, action_id)
        self._state_action_count: dict[str, int] = defaultdict(int)
        self._group_outcome_count: dict[str, dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self._total_actions_executed = 0
        self._click_streak = 0
        self._verdict_computer = VerdictComputer()
        self._narrative_generator = NarrativeGenerator()

    async def explore(self, start_url: str) -> ExplorationResult:
        """Main exploration loop."""
        started_at = datetime.now(timezone.utc).isoformat()
        start_time = time.monotonic()

        self.terminal.print_banner(start_url, self.config)

        # 1. Navigate to start URL
        await self.browser.navigate(start_url)

        # 2. Capture initial state
        initial_state = await self.browser.capture_state(depth=0)
        self.graph.add_state(initial_state)
        self.terminal.log_state_discovered(initial_state, is_new=True)

        # 3. Discover actions from initial state
        await self._discover_and_enqueue(initial_state)

        # 4. Main exploration loop
        while self._frontier:
            if self._should_stop():
                self.terminal.log_info("Stopping: limits reached")
                break

            item = self._pop_diverse()
            action = item.action
            source_state_id = item.source_state_id

            # Skip already-visited (state, action) pairs
            pair = (source_state_id, action.action_id)
            if pair in self._visited:
                continue
            self._visited.add(pair)

            # Navigate back to source state if needed
            navigated_back = await self._navigate_to_state(source_state_id)
            if not navigated_back:
                self.terminal.log_warning(
                    f"Could not return to state {source_state_id[:8]}, skipping action"
                )
                continue

            # Execute the action
            self.terminal.log_action_start(action, source_state_id)
            result = await self.browser.execute_action(action)
            self._total_actions_executed += 1

            # Capture resulting state
            source_state = self.graph.states[source_state_id]
            new_depth = source_state.depth + 1
            target_state = await self.browser.capture_state(depth=new_depth)
            result.source_state_id = source_state_id
            result.target_state_id = target_state.state_id

            # Add to graph
            is_new_state = self.graph.add_state(target_state)
            self.graph.add_result(result)

            # Compute step verdict
            is_invalid = action.metadata.get("scenario") == "invalid"
            step_verdict = self._verdict_computer.compute_step_verdict(
                result.outcome,
                action.intent,
                is_invalid_scenario=is_invalid,
            )
            result.verdict = step_verdict.verdict.value
            result.verdict_reason = step_verdict.reason
            result.expected = step_verdict.expected
            result.actual = step_verdict.actual

            self.terminal.log_action_result(action, result, is_new_state)

            # Track group outcomes for smart deprioritization
            self._track_group_outcome(action, result)

            # If new state at acceptable depth, discover its actions
            if is_new_state and new_depth < self.config.max_depth:
                self.terminal.log_state_discovered(target_state, is_new=True)
                await self._discover_and_enqueue(target_state)
            elif is_new_state:
                self.terminal.log_state_discovered(target_state, is_new=True)
                self.terminal.log_info(
                    f"  Max depth ({self.config.max_depth}) reached, not exploring further"
                )

        # 5. Extract flows and compute verdicts + narratives
        flows = self.graph.extract_flows()
        self._compute_flow_verdicts_and_narratives(flows)
        duration = time.monotonic() - start_time
        stats = self.graph.get_stats()

        result = ExplorationResult(
            config=self.config.model_dump(),
            started_at=started_at,
            finished_at=datetime.now(timezone.utc).isoformat(),
            duration_seconds=round(duration, 2),
            states=self.graph.states,
            actions=self.graph.actions,
            results=self.graph.results,
            flows=flows,
            stats=stats,
        )

        self.terminal.print_summary(result)
        return result

    async def _discover_and_enqueue(self, state: PageState) -> None:
        """Discover interactive elements and add their actions to the frontier."""
        elements = await discover_elements(self.browser.page)
        self.terminal.log_info(f"  Discovered {len(elements)} interactive elements")

        base_url = (
            state.url.split("//", 1)[-1].split("/", 1)[0] if "//" in state.url else ""
        )
        base_url = state.url.rsplit("/", 1)[0] if "/" in state.url else state.url

        # Generate individual element actions
        actions = generate_actions(elements, base_url=base_url)

        # Generate form submit actions
        form_actions = generate_form_submit_actions(elements)
        actions.extend(form_actions)

        # Partition into click vs interactive (fill/select/check/submit/search)
        # to ensure diverse action types get reserved frontier slots.
        # Search-trigger clicks (role="search") are treated as diverse so they
        # don't get drowned out by navigation links.
        def _is_diverse(a: Action) -> bool:
            if a.action_type in _DIVERSE_TYPES:
                return True
            if a.metadata.get("is_search") == "true":
                return True
            return False

        click_actions = [a for a in actions if not _is_diverse(a)]
        diverse_actions = [a for a in actions if _is_diverse(a)]

        budget = self.config.max_actions_per_state
        # Reserve up to 30% of slots for diverse actions (minimum 1 if any exist)
        diverse_reserve = min(len(diverse_actions), max(1, budget * 3 // 10))
        click_budget = budget - diverse_reserve if diverse_actions else budget

        enqueued = 0

        def _enqueue(action: Action) -> None:
            nonlocal enqueued
            priority = self._adjusted_priority(action)
            self.graph.add_action(action)
            heapq.heappush(
                self._frontier, _FrontierItem(priority, action, state.state_id)
            )
            self._state_action_count[state.state_id] += 1
            enqueued += 1

        # Enqueue click actions up to their budget
        for action in click_actions:
            if enqueued >= click_budget:
                break
            _enqueue(action)

        # Enqueue diverse actions (fill, select, check, submit)
        for action in diverse_actions:
            if self._state_action_count[state.state_id] >= budget:
                break
            _enqueue(action)

        self.terminal.log_info(
            f"  Enqueued {enqueued} actions "
            f"({len(diverse_actions)} interactive, frontier size: {len(self._frontier)})"
        )

    async def _navigate_to_state(self, target_state_id: str) -> bool:
        """Navigate back to a previously visited state.

        Returns True if navigation succeeded.
        """
        # Check if already at the target state
        try:
            current_state = await self.browser.capture_state(depth=0)
            if (
                current_state.fingerprint
                == self.graph.states[target_state_id].fingerprint
            ):
                return True
        except Exception:
            pass

        target = self.graph.states[target_state_id]

        # Try direct URL navigation
        try:
            await self.browser.navigate(target.url)
            current_state = await self.browser.capture_state(depth=0)
            if current_state.fingerprint == target.fingerprint:
                return True
        except Exception:
            pass

        # If direct navigation didn't reproduce the state, try replaying path
        path = self.graph.find_path_from_root(target_state_id)
        if path is not None and len(path) > 0:
            try:
                # Navigate to root first
                root_state = self.graph.states[self.graph.root_state_id]
                await self.browser.navigate(root_state.url)

                # Replay each action
                for step in path:
                    action = self.graph.actions.get(step.action_id)
                    if action:
                        await self.browser.execute_action(action)

                return True
            except Exception:
                pass

        # Last resort: just navigate to the URL and hope for the best
        try:
            await self.browser.navigate(target.url)
            return True
        except Exception:
            return False

    def _compute_flow_verdicts_and_narratives(self, flows: list[Flow]) -> None:
        """Compute journey verdicts and narratives for each flow."""
        from flowscout.analysis.verdict import StepVerdict, Verdict

        for flow in flows:
            # Gather step verdicts from results for this flow
            step_verdicts: list[StepVerdict] = []
            flow_actions: list[Action] = []
            flow_results: list[ActionResult] = []
            flow_states: list[PageState | None] = []
            flow_intents = []

            for i, action_id in enumerate(flow.action_ids):
                action = self.graph.actions.get(action_id)
                source_sid = flow.state_ids[i] if i < len(flow.state_ids) else ""
                # Find matching result
                matching_result = None
                for r in self.graph.results:
                    if r.action_id == action_id and r.source_state_id == source_sid:
                        matching_result = r
                        break
                if not matching_result:
                    for r in self.graph.results:
                        if r.action_id == action_id:
                            matching_result = r
                            break

                if action:
                    flow_actions.append(action)
                    flow_intents.append(action.intent)
                if matching_result:
                    flow_results.append(matching_result)
                    sv = StepVerdict(
                        verdict=(
                            Verdict(matching_result.verdict)
                            if matching_result.verdict
                            else Verdict.INCONCLUSIVE
                        ),
                        reason=matching_result.verdict_reason or "",
                        expected=matching_result.expected or "",
                        actual=matching_result.actual or "",
                    )
                    step_verdicts.append(sv)

            # Journey verdict
            journey_verdict = self._verdict_computer.compute_journey_verdict(
                step_verdicts
            )
            flow.verdict = journey_verdict

            # Narrative
            flow_states = [self.graph.states.get(sid) for sid in flow.state_ids]
            narrative = self._narrative_generator.narrate_flow(
                flow.name,
                flow_actions,
                flow_results,
                flow_states,
                intents=flow_intents,
                step_verdicts=step_verdicts,
            )
            flow.narrative = narrative

    @staticmethod
    def _is_diverse_item(item: _FrontierItem) -> bool:
        """Check if a frontier item is a diverse (non-navigation) action."""
        if item.action.action_type in _DIVERSE_TYPES:
            return True
        if item.action.metadata.get("is_search") == "true":
            return True
        return False

    def _pop_diverse(self) -> _FrontierItem:
        """Pop from frontier with diversity awareness.

        After ``_DIVERSITY_INTERVAL`` consecutive click actions, prefer a
        non-click action if one exists.  Prefers individual input actions
        and search triggers over composite SUBMIT_FORM.
        """
        if self._click_streak >= _DIVERSITY_INTERVAL:
            best_idx: int | None = None
            best_priority = float("inf")

            # First pass: prefer input actions + search triggers
            for i, candidate in enumerate(self._frontier):
                if candidate.priority < best_priority and (
                    candidate.action.action_type in _INPUT_TYPES
                    or candidate.action.metadata.get("is_search") == "true"
                ):
                    best_idx = i
                    best_priority = candidate.priority

            # Fallback: any diverse type (including SUBMIT_FORM)
            if best_idx is None:
                for i, candidate in enumerate(self._frontier):
                    if (
                        self._is_diverse_item(candidate)
                        and candidate.priority < best_priority
                    ):
                        best_idx = i
                        best_priority = candidate.priority

            if best_idx is not None:
                item = self._frontier[best_idx]
                # Remove from heap: swap with last, pop, re-heapify
                self._frontier[best_idx] = self._frontier[-1]
                self._frontier.pop()
                if self._frontier:
                    heapq.heapify(self._frontier)
                self._click_streak = 0
                return item

        item = heapq.heappop(self._frontier)
        if item.action.action_type == ActionType.CLICK and not self._is_diverse_item(item):
            self._click_streak += 1
        else:
            self._click_streak = 0
        return item

    def _should_stop(self) -> bool:
        """Check termination conditions."""
        if len(self.graph.states) >= self.config.max_states:
            return True
        if (
            self._total_actions_executed
            >= self.config.max_states * self.config.max_actions_per_state
        ):
            return True
        return False

    def _track_group_outcome(self, action: Action, result: ActionResult) -> None:
        """Track outcomes by action group for smart deprioritization.

        Groups are defined by the element's data attributes (e.g., all theme
        buttons share similar data attributes).
        """
        # Group by action label prefix (e.g., "Select option:" actions)
        label_prefix = action.label.split(":")[0] if ":" in action.label else ""
        if label_prefix:
            self._group_outcome_count[label_prefix][result.outcome.value] += 1

    def _adjusted_priority(self, action: Action) -> int:
        """Adjust priority based on group outcome history.

        If we've seen 3+ actions in a group all produce DOM_CHANGE (not
        NAVIGATION), deprioritize remaining actions in that group.
        """
        label_prefix = action.label.split(":")[0] if ":" in action.label else ""
        if not label_prefix:
            return action.priority

        group_outcomes = self._group_outcome_count.get(label_prefix)
        if not group_outcomes:
            return action.priority

        dom_changes = group_outcomes.get(OutcomeType.DOM_CHANGE.value, 0)
        navigations = group_outcomes.get(OutcomeType.NAVIGATION.value, 0)

        # If 3+ DOM_CHANGE and 0 NAVIGATION, deprioritize
        if dom_changes >= 3 and navigations == 0:
            return max(action.priority, 80)

        return action.priority

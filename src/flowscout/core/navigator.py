"""Priority-BFS exploration engine."""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from flowscout.analysis.element_inventory import summarize_element_inventory
from flowscout.analysis.graph import ExplorationGraph, ExplorationResult, Flow
from flowscout.analysis.narrative import NarrativeGenerator
from flowscout.analysis.verdict import VerdictComputer
from flowscout.core.browser import BrowserManager
from flowscout.core.errors import BrowserError
from flowscout.core.frontier import FrontierManager, is_diverse_action
from flowscout.core.policy import get_action_policy_block_reason
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

if TYPE_CHECKING:
    from flowscout.smart.planner import SmartPlanner as _SmartPlannerType

logger = logging.getLogger(__name__)

SmartPlanner: type[_SmartPlannerType] | None = None


class Navigator:
    """The exploration engine that decides what to do next."""

    def __init__(
        self,
        browser: BrowserManager,
        graph: ExplorationGraph,
        config: ExplorerConfig,
        terminal: TerminalReporter,
        *,
        frontier: FrontierManager | None = None,
    ) -> None:
        self.browser = browser
        self.graph = graph
        self.config = config
        self.terminal = terminal
        self._frontier = frontier or FrontierManager()
        self._total_actions_executed = 0
        self._verdict_computer = VerdictComputer()
        self._narrative_generator = NarrativeGenerator()

        # Smart planner (only active in smart mode)
        self._smart_planner = None
        if config.smart_mode:
            from flowscout.smart.planner import SmartPlanner as _SmartPlanner

            self._smart_planner = _SmartPlanner(
                archetype_instance_limit=config.smart_archetype_instance_limit,
                min_features_before_stop=config.smart_min_features_before_stop,
                min_archetypes_before_stop=config.smart_min_archetypes_before_stop,
                stop_on_saturation=config.smart_stop_on_saturation,
            )

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
        await self._apply_smart_advice(initial_state)

        # 4. Main exploration loop
        while not self._frontier.is_empty:
            if self._should_stop():
                self.terminal.log_info("Stopping: limits reached")
                break

            item = self._frontier.pop()
            action = item.action
            source_state_id = item.source_state_id

            # Skip already-visited (state, action) pairs
            if self._frontier.is_visited(source_state_id, action.action_id):
                continue
            self._frontier.mark_visited(source_state_id, action.action_id)

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

            # Capture resulting state — only increment depth on page navigation
            source_state = self.graph.states[source_state_id]
            url_changed = result.url_before != result.url_after
            new_depth = source_state.depth + (1 if url_changed else 0)
            target_state = await self.browser.capture_state(depth=new_depth)
            result.source_state_id = source_state_id
            result.target_state_id = target_state.state_id

            # Add to graph
            is_new_state = self.graph.add_state(target_state)
            self.graph.add_result(result)

            # Compute step verdict
            is_invalid = action.metadata.get("scenario") == "invalid"
            observed_detail = self._result_detail(result)
            step_verdict = self._verdict_computer.compute_step_verdict(
                result.outcome,
                action.intent,
                is_invalid_scenario=is_invalid,
                observed_detail=observed_detail,
            )
            result.verdict = step_verdict.verdict.value
            result.verdict_reason = step_verdict.reason
            result.expected = step_verdict.expected
            result.actual = step_verdict.actual
            result.confidence, result.confidence_reason = (
                self._compute_transition_confidence(result.outcome)
            )

            self.terminal.log_action_result(action, result, is_new_state)

            # Track group outcomes for smart deprioritization
            self._frontier.track_outcome(action, result.outcome)

            # If new state at acceptable depth, discover its actions
            if is_new_state and new_depth < self.config.max_depth:
                self.terminal.log_state_discovered(target_state, is_new=True)
                await self._discover_and_enqueue(target_state)
                await self._apply_smart_advice(target_state)
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

        # Attach smart mode data
        if self._smart_planner:
            result.page_catalogs = self._smart_planner.get_all_catalogs()
            result.coverage = self._smart_planner.coverage.summary()
            result.archetypes = self._smart_planner.registry.archetype_distribution()
            result.smart_analyses = self._smart_planner.get_all_analyses()
            result.element_inventory = summarize_element_inventory(
                analyses=result.smart_analyses,
                states_by_id=result.states,
            )
            result.stats["interactive_elements"] = int(
                result.element_inventory.get("interactive_elements", 0)
            )
            result.stats["non_interactive_elements"] = int(
                result.element_inventory.get("non_interactive_elements", 0)
            )
            result.stats["total_catalog_elements"] = int(
                result.element_inventory.get("total_elements", 0)
            )

        self.terminal.print_summary(result)
        return result

    async def _apply_smart_advice(self, state: PageState) -> None:
        """Run the smart planner and apply its advice to the frontier."""
        if not self._smart_planner:
            return
        try:
            advice = await self._smart_planner.on_state_discovered(
                state, self.browser, self.graph
            )
        except (BrowserError, RuntimeError):
            logger.debug("Smart planner failed for %s", state.state_id, exc_info=True)
            return

        # Log archetype discovery
        analysis = self._smart_planner.get_analysis(state.state_id)
        if analysis:
            is_novel = (
                self._smart_planner.registry.instance_count(
                    analysis.structural_signature
                )
                == 1
            )
            self.terminal.log_archetype(
                state.state_id,
                analysis.archetype.value,
                analysis.archetype_confidence,
                is_novel,
            )

            if advice.content_expectations:
                self.terminal.log_expectation_result(advice.content_expectations)

        # Apply priority overrides to frontier
        if advice.priority_overrides:
            self._frontier.apply_priority_overrides(
                state.state_id,
                advice.priority_overrides,
                advice.is_archetype_saturated,
            )

    async def _discover_and_enqueue(self, state: PageState) -> None:
        """Discover interactive elements and add their actions to the frontier."""
        elements = await discover_elements(self.browser.page)
        self.terminal.log_info(f"  Discovered {len(elements)} interactive elements")

        base_url = (
            state.url.split("//", 1)[-1].split("/", 1)[0] if "//" in state.url else ""
        )
        base_url = state.url.rsplit("/", 1)[0] if "/" in state.url else state.url

        # Generate individual element actions
        actions = generate_actions(
            elements,
            base_url=base_url,
            input_profile=self.config.input_profile.value,
        )

        # Generate form submit actions
        form_actions = generate_form_submit_actions(
            elements,
            input_profile=self.config.input_profile.value,
        )
        actions.extend(form_actions)
        actions, blocked_count = self._apply_action_policy(actions)

        # Partition into click vs interactive for budget allocation
        click_actions = [a for a in actions if not is_diverse_action(a)]
        diverse_actions = [a for a in actions if is_diverse_action(a)]

        budget = self.config.max_actions_per_state
        diverse_reserve = min(len(diverse_actions), max(1, budget * 3 // 10))
        click_budget = budget - diverse_reserve if diverse_actions else budget

        enqueued = 0

        def _enqueue(action: Action) -> None:
            nonlocal enqueued
            priority = self._frontier.adjusted_priority(action)
            self.graph.add_action(action)
            self._frontier.push(action, state.state_id, priority)
            enqueued += 1

        for action in click_actions:
            if enqueued >= click_budget:
                break
            _enqueue(action)

        for action in diverse_actions:
            if self._frontier.state_action_count(state.state_id) >= budget:
                break
            _enqueue(action)

        self.terminal.log_info(
            f"  Enqueued {enqueued} actions "
            f"({len(diverse_actions)} interactive, frontier size: {self._frontier.size})"
        )
        if blocked_count:
            self.terminal.log_info(
                f"  Policy skipped {blocked_count} high-impact actions"
            )

    def _apply_action_policy(self, actions: list[Action]) -> tuple[list[Action], int]:
        """Filter actions according to non-destructive policy settings."""
        allowed_actions: list[Action] = []
        blocked_count = 0
        for action in actions:
            reason = get_action_policy_block_reason(
                action=action,
                policy=self.config.action_policy,
            )
            if reason is None:
                allowed_actions.append(action)
                continue

            blocked_count += 1
            if self.config.verbose:
                self.terminal.log_info(f"  Policy blocked '{action.label}' ({reason})")

        return allowed_actions, blocked_count

    async def _navigate_to_state(self, target_state_id: str) -> bool:
        """Navigate back to a previously visited state."""
        try:
            current_state = await self.browser.capture_state(depth=0)
            if (
                current_state.fingerprint
                == self.graph.states[target_state_id].fingerprint
            ):
                return True
        except BrowserError:
            logger.debug(
                "Could not capture current state for comparison", exc_info=True
            )

        target = self.graph.states[target_state_id]

        try:
            await self.browser.navigate(target.url)
            current_state = await self.browser.capture_state(depth=0)
            if current_state.fingerprint == target.fingerprint:
                return True
        except BrowserError:
            logger.debug("Direct navigation to %s failed", target.url, exc_info=True)

        path = self.graph.find_path_from_root(target_state_id)
        if path is not None and len(path) > 0:
            try:
                root_state = self.graph.states[self.graph.root_state_id]
                await self.browser.navigate(root_state.url)
                for step in path:
                    action = self.graph.actions.get(step.action_id)
                    if action:
                        await self.browser.execute_action(action)
                return True
            except BrowserError:
                logger.debug(
                    "Path replay to %s failed",
                    target_state_id,
                    exc_info=True,
                )

        try:
            await self.browser.navigate(target.url)
            return True
        except BrowserError:
            logger.debug(
                "Last-resort navigation to %s failed", target.url, exc_info=True
            )
            return False

    def _compute_flow_verdicts_and_narratives(self, flows: list[Flow]) -> None:
        """Compute journey verdicts and narratives for each flow."""
        from flowscout.analysis.verdict import StepVerdict, Verdict

        for flow in flows:
            step_verdicts: list[StepVerdict] = []
            flow_actions: list[Action] = []
            flow_results: list[ActionResult] = []
            flow_intents = []

            for i, action_id in enumerate(flow.action_ids):
                action = self.graph.actions.get(action_id)
                source_sid = flow.state_ids[i] if i < len(flow.state_ids) else ""
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

            journey_verdict = self._verdict_computer.compute_journey_verdict(
                step_verdicts
            )
            flow.verdict = journey_verdict

            flow_states: list[PageState | None] = [
                self.graph.states.get(sid) for sid in flow.state_ids
            ]
            narrative = self._narrative_generator.narrate_flow(
                flow.name,
                flow_actions,
                flow_results,
                flow_states,
                intents=flow_intents,
                step_verdicts=step_verdicts,
            )
            flow.narrative = narrative

    def _should_stop(self) -> bool:
        """Check termination conditions."""
        if len(self.graph.states) >= self.config.max_states:
            return True
        if (
            self._total_actions_executed
            >= self.config.max_states * self.config.max_actions_per_state
        ):
            return True
        if self._smart_planner and self._smart_planner.coverage.is_saturated():
            return True
        return False

    @staticmethod
    def _result_detail(result: ActionResult) -> str:
        """Return the best available human-readable detail for a result."""
        if result.error_messages:
            return result.error_messages[0]
        if result.console_errors:
            return result.console_errors[0]
        return (result.message or "").strip()

    @staticmethod
    def _compute_transition_confidence(outcome: OutcomeType) -> tuple[float, str]:
        """Map an observed outcome to a confidence score and reason."""
        mapping: dict[OutcomeType, tuple[float, str]] = {
            OutcomeType.NAVIGATION: (0.95, "URL changed and navigation completed"),
            OutcomeType.DOM_CHANGE: (0.85, "DOM changed after interaction"),
            OutcomeType.VALIDATION_ERROR: (0.8, "Validation feedback detected"),
            OutcomeType.VISUAL_CHANGE: (0.7, "Visual state changed"),
            OutcomeType.NO_CHANGE: (0.55, "No visible transition detected"),
            OutcomeType.TIMEOUT: (0.3, "Action timed out"),
            OutcomeType.NETWORK_ERROR: (0.25, "HTTP/network errors detected"),
            OutcomeType.CONSOLE_ERROR: (0.25, "Console errors detected"),
            OutcomeType.EXCEPTION: (0.2, "Action raised an exception"),
        }
        return mapping.get(outcome, (0.5, "Unknown outcome"))


# Backward-compatible alias
ExplorationEngine = Navigator

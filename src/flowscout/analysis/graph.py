"""NetworkX-backed exploration graph with flow extraction."""

from __future__ import annotations

from itertools import islice
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, Field

import networkx as nx

from flowscout.analysis.narrative import FlowNarrative
from flowscout.core.inventory import PageInventory
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType

_MAX_PATHS_PER_LEAF = 25
_MAX_TOTAL_LINEAR_FLOWS = 500
_MAX_CYCLE_FLOWS = 200
EXPLORATION_RESULT_SCHEMA_VERSION = "2.0.0"


class Flow(BaseModel):
    """A named sequence of states connected by actions."""

    flow_id: str
    name: str
    description: str
    state_ids: list[str] = Field(default_factory=list)
    action_ids: list[str] = Field(default_factory=list)
    outcomes: list[OutcomeType] = Field(default_factory=list)
    is_cycle: bool = False
    depth: int = 0
    stability_score: float = 0.0
    is_stable: bool = False
    narrative: FlowNarrative | None = None
    category: str = ""
    tags: list[str] = Field(default_factory=list)
    flow_template: str = ""
    archetype_sequence: list[str] = Field(default_factory=list)


class ExplorationResult(BaseModel):
    """Complete exploration output."""

    schema_version: str = EXPLORATION_RESULT_SCHEMA_VERSION
    version: str = EXPLORATION_RESULT_SCHEMA_VERSION
    config: dict[str, Any] = Field(default_factory=dict)
    started_at: str = ""
    finished_at: str = ""
    duration_seconds: float = 0.0
    states: dict[str, PageState] = Field(default_factory=dict)
    actions: dict[str, Action] = Field(default_factory=dict)
    results: list[ActionResult] = Field(default_factory=list)
    flows: list[Flow] = Field(default_factory=list)
    stats: dict[str, int] = Field(default_factory=dict)
    page_catalogs: dict[str, Any] = Field(default_factory=dict)
    coverage: dict[str, Any] = Field(default_factory=dict)
    page_inventories: dict[str, PageInventory] = Field(default_factory=dict)
    element_inventory: dict[str, Any] = Field(default_factory=dict)
    archetypes: dict[str, Any] = Field(default_factory=dict)
    smart_analyses: dict[str, Any] = Field(default_factory=dict)


class ExplorationGraph:
    """Directed graph of page states connected by actions."""

    def __init__(self) -> None:
        self._graph: nx.DiGraph = nx.DiGraph()
        self.states: dict[str, PageState] = {}
        self.actions: dict[str, Action] = {}
        self.results: list[ActionResult] = []
        self._root_state_id: str | None = None

    @property
    def root_state_id(self) -> str | None:
        return self._root_state_id

    def add_state(self, state: PageState) -> bool:
        """Add a state node. Returns True if it was new."""
        if state.state_id in self.states:
            return False
        self.states[state.state_id] = state
        self._graph.add_node(state.state_id)
        if self._root_state_id is None:
            self._root_state_id = state.state_id
        return True

    def add_action(self, action: Action) -> None:
        """Register an action (without connecting it to states yet)."""
        self.actions[action.action_id] = action

    def add_result(self, result: ActionResult) -> None:
        """Add an action result as a directed edge between states."""
        self.results.append(result)
        self._graph.add_edge(
            result.source_state_id,
            result.target_state_id,
            action_id=result.action_id,
            outcome=result.outcome.value,
        )

    def find_path_from_root(self, target_state_id: str) -> list[ActionResult] | None:
        """Find the shortest action path from root to target state."""
        if not self._root_state_id or target_state_id == self._root_state_id:
            return []
        if target_state_id not in self._graph:
            return None
        try:
            node_path = nx.shortest_path(
                self._graph, self._root_state_id, target_state_id
            )
        except nx.NetworkXNoPath:
            return None

        action_path: list[ActionResult] = []
        for i in range(len(node_path) - 1):
            src, dst = node_path[i], node_path[i + 1]
            edge_data = self._graph.edges[src, dst]
            action_id = edge_data["action_id"]
            for result in self.results:
                if result.action_id == action_id and result.source_state_id == src:
                    action_path.append(result)
                    break
        return action_path

    def extract_flows(self) -> list[Flow]:
        """Extract named flows from the graph.

        Finds all simple paths from root to leaf nodes, plus cycles.
        """
        flows: list[Flow] = []
        if not self._root_state_id:
            return flows

        # Leaf nodes (no outgoing edges)
        leaf_nodes = [
            n
            for n in self._graph.nodes
            if self._graph.out_degree(n) == 0 and n != self._root_state_id
        ]

        flow_counter = 0
        total_linear_flows = 0
        linear_flow_limit_hit = False
        for leaf in leaf_nodes:
            try:
                per_leaf_count = 0
                for path in nx.all_simple_paths(self._graph, self._root_state_id, leaf):
                    if (
                        per_leaf_count >= _MAX_PATHS_PER_LEAF
                        or total_linear_flows >= _MAX_TOTAL_LINEAR_FLOWS
                    ):
                        linear_flow_limit_hit = True
                        break

                    flow_counter += 1
                    per_leaf_count += 1
                    total_linear_flows += 1
                    flow = self._path_to_flow(path, flow_counter)
                    flows.append(flow)

                if total_linear_flows >= _MAX_TOTAL_LINEAR_FLOWS:
                    linear_flow_limit_hit = True
                    break
            except nx.NetworkXError:
                continue

        # Detect cycles
        try:
            for cycle in islice(nx.simple_cycles(self._graph), _MAX_CYCLE_FLOWS):
                if len(cycle) > 1:
                    flow_counter += 1
                    flow = self._cycle_to_flow(cycle, flow_counter)
                    flows.append(flow)
        except nx.NetworkXError:
            pass

        if linear_flow_limit_hit and self.results:
            flows.extend(self._result_fallback_flows(start_index=flow_counter + 1))

        # Fallback for interaction-heavy runs with no root->leaf paths
        # (for example single-page apps or auth screens with self-loops).
        if not flows and self.results:
            flows.extend(self._result_fallback_flows(start_index=flow_counter + 1))

        # Assign categories and tags
        for flow in flows:
            flow.category, flow.tags = self._categorize_flow(flow)

        return flows

    def _path_to_flow(self, node_path: list[str], index: int) -> Flow:
        """Convert a node path to a Flow."""
        action_ids: list[str] = []
        outcomes: list[OutcomeType] = []

        for i in range(len(node_path) - 1):
            src, dst = node_path[i], node_path[i + 1]
            if self._graph.has_edge(src, dst):
                edge = self._graph.edges[src, dst]
                action_ids.append(edge.get("action_id", ""))
                outcomes.append(OutcomeType(edge.get("outcome", "no_change")))

        # Build a descriptive name from page titles
        action_labels = []
        for aid in action_ids:
            if aid in self.actions:
                action_labels.append(self.actions[aid].label)
        description = " → ".join(action_labels) if action_labels else "Unknown flow"

        start_state = self.states.get(node_path[0])
        end_state = self.states.get(node_path[-1])
        start_title = start_state.title if start_state and start_state.title else ""
        end_title = end_state.title if end_state and end_state.title else ""
        if start_title and end_title and start_title != end_title:
            name = f"{start_title} \u2192 {end_title}"
        elif end_title:
            name = end_title
        else:
            name = f"Flow {index}"

        return Flow(
            flow_id=f"flow-{index}",
            name=name,
            description=description,
            state_ids=node_path,
            action_ids=action_ids,
            outcomes=outcomes,
            is_cycle=False,
            depth=len(node_path) - 1,
        )

    def _cycle_to_flow(self, cycle_nodes: list[str], index: int) -> Flow:
        """Convert a cycle to a Flow."""
        # Close the cycle
        closed = list(cycle_nodes) + [cycle_nodes[0]]
        action_ids: list[str] = []
        outcomes: list[OutcomeType] = []

        for i in range(len(closed) - 1):
            src, dst = closed[i], closed[i + 1]
            if self._graph.has_edge(src, dst):
                edge = self._graph.edges[src, dst]
                action_ids.append(edge.get("action_id", ""))
                outcomes.append(OutcomeType(edge.get("outcome", "no_change")))

        action_labels = [
            self.actions[aid].label for aid in action_ids if aid in self.actions
        ]

        # Build cycle name from state titles
        cycle_titles = []
        for sid in cycle_nodes:
            state = self.states.get(sid)
            if state and state.title:
                cycle_titles.append(state.title)
        if cycle_titles:
            unique_titles = list(dict.fromkeys(cycle_titles))
            cycle_name = " \u2194 ".join(unique_titles)
            if len(unique_titles) == 1 and action_labels:
                cycle_name = f"{unique_titles[0]} \u00b7 {action_labels[0]}"
        else:
            cycle_name = f"Cycle {index}"

        return Flow(
            flow_id=f"cycle-{index}",
            name=cycle_name,
            description=(
                " \u2192 ".join(action_labels)
                if action_labels
                else f"Cycle through {len(cycle_nodes)} states"
            ),
            state_ids=closed,
            action_ids=action_ids,
            outcomes=outcomes,
            is_cycle=True,
            depth=len(cycle_nodes),
        )

    @staticmethod
    def _fallback_outcome_label(outcome: OutcomeType) -> str:
        """Return a readable outcome label for fallback flow names."""
        labels = {
            OutcomeType.NAVIGATION: "Navigation",
            OutcomeType.DOM_CHANGE: "DOM Change",
            OutcomeType.VISUAL_CHANGE: "Visual Change",
            OutcomeType.NO_CHANGE: "No Visible Change",
            OutcomeType.VALIDATION_ERROR: "Validation Feedback",
            OutcomeType.NETWORK_ERROR: "Network Error",
            OutcomeType.CONSOLE_ERROR: "Console Error",
            OutcomeType.TIMEOUT: "Timeout",
            OutcomeType.EXCEPTION: "Exception",
        }
        return labels.get(outcome, str(outcome.value).replace("_", " ").title())

    @staticmethod
    def _fallback_action_summary(action: Action | None, action_id: str) -> str:
        """Return a concise, human-readable action summary."""
        if not action:
            return action_id

        label = action.label.strip()
        for prefix in (
            "Click: ",
            "Fill: ",
            "Check: ",
            "Uncheck: ",
            "Select option: ",
            "Select radio: ",
            "Toggle: ",
            "Open dropdown: ",
            "Tab: ",
        ):
            if label.startswith(prefix):
                label = label[len(prefix) :].strip()
                break

        if action.action_type == ActionType.FILL and " = '" in label:
            label = label.split(" = '", 1)[0].strip()

        verb_by_type = {
            ActionType.CLICK: "Click",
            ActionType.FILL: "Enter",
            ActionType.SELECT_OPTION: "Select",
            ActionType.CHECK: "Check",
            ActionType.UNCHECK: "Uncheck",
            ActionType.SUBMIT_FORM: "Submit",
            ActionType.PRESS_KEY: "Press",
            ActionType.HOVER: "Hover",
            ActionType.NAVIGATE: "Navigate",
        }
        verb = verb_by_type.get(action.action_type, "Use")
        return f"{verb} {label}".strip()

    def _result_fallback_flows(self, start_index: int) -> list[Flow]:
        """Build one-step flows directly from recorded results.

        This keeps reporting actionable when path-based extraction yields
        zero flows (typically due to self-loops/no leaf nodes).
        """
        flows: list[Flow] = []
        seen: set[tuple[str, str]] = set()
        index = start_index

        for result in self.results:
            dedupe_key = (
                result.action_id,
                result.outcome.value,
            )
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)

            source_state = self.states.get(result.source_state_id)
            target_state = self.states.get(result.target_state_id)
            action = self.actions.get(result.action_id)

            source_name = (
                source_state.title if source_state and source_state.title else "State"
            )
            target_name = (
                target_state.title if target_state and target_state.title else "State"
            )
            action_summary = self._fallback_action_summary(action, result.action_id)
            outcome_summary = self._fallback_outcome_label(result.outcome)

            if source_name == target_name:
                name = f"{source_name} · {action_summary} · {outcome_summary}"
            else:
                name = f"{source_name} \u2192 {target_name} · {action_summary}"
                if result.outcome != OutcomeType.NAVIGATION:
                    name = f"{name} · {outcome_summary}"

            description = action_summary
            if result.observation_notes:
                description = f"{description} \u2192 {result.observation_notes}"
            elif result.message:
                description = f"{description} \u2192 {result.message}"

            flow = Flow(
                flow_id=f"flow-{index}",
                name=name,
                description=description,
                state_ids=[result.source_state_id, result.target_state_id],
                action_ids=[result.action_id],
                outcomes=[result.outcome],
                is_cycle=False,
                depth=1,
            )
            flows.append(flow)
            index += 1

        return flows

    def _categorize_flow(self, flow: Flow) -> tuple[str, list[str]]:
        """Assign a category and interaction tags to a flow."""
        # Category from starting state's title (generic — works on any site)
        start_state = self.states.get(flow.state_ids[0]) if flow.state_ids else None
        category = "Other"
        if start_state:
            title = start_state.title or ""
            if title:
                category = title
            else:
                # Fallback: last path segment from URL
                parsed = urlparse(start_state.url)
                path = parsed.path.rstrip("/")
                category = path.split("/")[-1] if path else "Home"

        # Tags from action types used
        tags: set[str] = set()
        for aid in flow.action_ids:
            action = self.actions.get(aid)
            if not action:
                continue
            if action.meta.is_search:
                tags.add("search")
            elif action.meta.is_dropdown_option:
                tags.add("dropdown")
            elif action.action_type == ActionType.CLICK:
                tags.add("navigation")
            elif action.action_type == ActionType.FILL:
                tags.add("form")
            elif action.action_type == ActionType.SELECT_OPTION:
                tags.add("dropdown")
            elif action.action_type in (ActionType.CHECK, ActionType.UNCHECK):
                tags.add("form")
            elif action.action_type == ActionType.SUBMIT_FORM:
                tags.add("form")

        return category, sorted(tags)

    def to_serializable(self) -> dict[str, Any]:
        """Export graph as a JSON-serializable dict for reporting."""
        nodes = []
        for sid, state in self.states.items():
            nodes.append(
                {
                    "id": sid,
                    "label": state.title or state.url,
                    "url": state.url,
                    "depth": state.depth,
                    "signals": state.signals,
                }
            )

        edges = []
        for result in self.results:
            action = self.actions.get(result.action_id)
            edges.append(
                {
                    "source": result.source_state_id,
                    "target": result.target_state_id,
                    "action_id": result.action_id,
                    "label": action.label if action else result.action_id,
                    "outcome": result.outcome.value,
                }
            )

        return {"nodes": nodes, "edges": edges}

    def get_stats(self) -> dict[str, int]:
        """Compute summary statistics."""
        outcome_counts: dict[str, int] = {}
        for result in self.results:
            key = result.outcome.value
            outcome_counts[key] = outcome_counts.get(key, 0) + 1

        return {
            "total_states": len(self.states),
            "total_actions_executed": len(self.results),
            "total_unique_actions": len(self.actions),
            "total_edges": self._graph.number_of_edges(),
            **{f"outcome_{k}": v for k, v in outcome_counts.items()},
        }

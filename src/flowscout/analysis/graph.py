"""NetworkX-backed exploration graph with flow extraction."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

import networkx as nx

from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, OutcomeType

if TYPE_CHECKING:
    pass


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
    verdict: Any = None  # JourneyVerdict | None
    narrative: Any = None  # FlowNarrative | None


class ExplorationResult(BaseModel):
    """Complete exploration output."""

    config: dict = Field(default_factory=dict)
    started_at: str = ""
    finished_at: str = ""
    duration_seconds: float = 0.0
    states: dict[str, PageState] = Field(default_factory=dict)
    actions: dict[str, Action] = Field(default_factory=dict)
    results: list[ActionResult] = Field(default_factory=list)
    flows: list[Flow] = Field(default_factory=list)
    stats: dict[str, int] = Field(default_factory=dict)


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
        for leaf in leaf_nodes:
            try:
                paths = list(
                    nx.all_simple_paths(self._graph, self._root_state_id, leaf)
                )
            except nx.NetworkXError:
                continue

            for path in paths:
                flow_counter += 1
                flow = self._path_to_flow(path, flow_counter)
                flows.append(flow)

        # Detect cycles
        try:
            for cycle in nx.simple_cycles(self._graph):
                if len(cycle) > 1:
                    flow_counter += 1
                    flow = self._cycle_to_flow(cycle, flow_counter)
                    flows.append(flow)
        except nx.NetworkXError:
            pass

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

        # Build cycle name from state titles
        cycle_titles = []
        for sid in cycle_nodes:
            state = self.states.get(sid)
            if state and state.title:
                cycle_titles.append(state.title)
        if cycle_titles:
            cycle_name = " \u2194 ".join(dict.fromkeys(cycle_titles))
        else:
            cycle_name = f"Cycle {index}"

        return Flow(
            flow_id=f"cycle-{index}",
            name=cycle_name,
            description=f"Cycle through {len(cycle_nodes)} states",
            state_ids=closed,
            action_ids=action_ids,
            outcomes=outcomes,
            is_cycle=True,
            depth=len(cycle_nodes),
        )

    def to_serializable(self) -> dict:
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

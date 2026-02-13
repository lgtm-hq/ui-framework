"""Model-based graph walking strategies over a SiteModel."""

from __future__ import annotations

import random
from collections.abc import Sequence

import networkx as nx

from flowscout.core.action_types import ActionType
from flowscout.modeling.scenarios import FlowScenario, ScenarioStep
from flowscout.modeling.site_model import NavigationEdge, SiteModel


class ModelWalker:
    """Traverse a SiteModel state machine using MBT strategies."""

    def __init__(self) -> None:
        """Initialize the walker."""
        self._rng = random.SystemRandom()

    def walk_edge_coverage(
        self,
        model: SiteModel,
    ) -> list[FlowScenario]:
        """Generate scenarios that collectively touch every navigation edge.

        Args:
            model: Site model to traverse.

        Returns:
            Scenarios that together cover all model transitions.
        """
        graph = _build_graph(model=model)
        if graph.number_of_edges() == 0:
            return []

        edge_index, outgoing_edges, edges_by_pair = _index_navigation_edges(model=model)
        component_walks = _build_edge_coverage_walks(
            graph=graph,
            edge_index=edge_index,
            outgoing_edges=outgoing_edges,
            edges_by_pair=edges_by_pair,
        )

        scenarios: list[FlowScenario] = []
        page_type_names = _page_type_name_map(model=model)
        page_type_features = _page_type_feature_map(model=model)
        for scenario_index, (path_nodes, path_edge_ids) in enumerate(
            component_walks,
            start=1,
        ):
            scenarios.append(
                _build_scenario(
                    strategy="edge_coverage",
                    scenario_index=scenario_index,
                    node_path=path_nodes,
                    edge_ids=path_edge_ids,
                    edge_index=edge_index,
                    page_type_names=page_type_names,
                    page_type_features=page_type_features,
                ),
            )

        return scenarios

    def walk_state_coverage(
        self,
        model: SiteModel,
    ) -> list[FlowScenario]:
        """Generate scenarios that visit every page type at least once.

        Args:
            model: Site model to traverse.

        Returns:
            Scenarios that together visit all states/page types.
        """
        graph = _build_graph(model=model)
        all_nodes = sorted(graph.nodes)
        if not all_nodes:
            return []

        edge_index, _, edges_by_pair = _index_navigation_edges(model=model)
        page_type_names = _page_type_name_map(model=model)
        page_type_features = _page_type_feature_map(model=model)
        uncovered: set[str] = set(all_nodes)
        scenarios: list[FlowScenario] = []
        scenario_index = 1

        while uncovered:
            start_node = min(uncovered)
            uncovered.remove(start_node)
            path_nodes = [start_node]
            current = start_node

            while uncovered:
                best_path = _shortest_path_to_any(
                    graph=graph,
                    source=current,
                    targets=uncovered,
                )
                if best_path is None:
                    break

                for node_id in best_path[1:]:
                    path_nodes.append(node_id)
                    uncovered.discard(node_id)
                current = path_nodes[-1]

            path_edge_ids = _resolve_path_edge_ids(
                node_path=path_nodes,
                edge_index=edge_index,
                edges_by_pair=edges_by_pair,
            )
            scenarios.append(
                _build_scenario(
                    strategy="state_coverage",
                    scenario_index=scenario_index,
                    node_path=path_nodes,
                    edge_ids=path_edge_ids,
                    edge_index=edge_index,
                    page_type_names=page_type_names,
                    page_type_features=page_type_features,
                ),
            )
            scenario_index += 1

        return scenarios

    def walk_random(
        self,
        model: SiteModel,
        steps: int = 20,
    ) -> FlowScenario:
        """Generate one random exploratory walk through the model.

        Args:
            model: Site model to traverse.
            steps: Maximum number of transition steps to attempt.

        Returns:
            A single random MBT scenario.
        """
        graph = _build_graph(model=model)
        all_nodes = sorted(graph.nodes)
        if not all_nodes:
            return FlowScenario(
                scenario_id="mbt-random-1",
                name="MBT random path 1",
                description="Random MBT walk on an empty model.",
                page_type_sequence=[],
                steps=[],
                priority="nice-to-have",
                template="mbt_random",
                tags=["mbt", "random"],
            )

        edge_index, outgoing_edges, _ = _index_navigation_edges(model=model)
        page_type_names = _page_type_name_map(model=model)
        page_type_features = _page_type_feature_map(model=model)
        start_weights = [
            max(
                sum(
                    max(edge_index[eid].occurrence_count, 1)
                    for eid in outgoing_edges.get(node_id, [])
                ),
                1,
            )
            for node_id in all_nodes
        ]
        start_node = self._rng.choices(
            population=all_nodes,
            weights=start_weights,
            k=1,
        )[0]

        path_nodes = [start_node]
        path_edge_ids: list[int] = []
        current = start_node

        for _ in range(max(steps, 0)):
            choices = outgoing_edges.get(current, [])
            if not choices:
                break

            weights = [max(edge_index[eid].occurrence_count, 1) for eid in choices]
            edge_id = self._rng.choices(
                population=choices,
                weights=weights,
                k=1,
            )[0]
            edge = edge_index[edge_id]
            path_edge_ids.append(edge_id)
            path_nodes.append(edge.to_page_type)
            current = edge.to_page_type

        return _build_scenario(
            strategy="random",
            scenario_index=1,
            node_path=path_nodes,
            edge_ids=path_edge_ids,
            edge_index=edge_index,
            page_type_names=page_type_names,
            page_type_features=page_type_features,
        )

    def walk_all_paths(
        self,
        model: SiteModel,
        max_depth: int = 5,
    ) -> list[FlowScenario]:
        """Enumerate all simple paths up to a maximum depth.

        Args:
            model: Site model to traverse.
            max_depth: Maximum number of edges in each path.

        Returns:
            All unique simple-path scenarios up to ``max_depth``.
        """
        if max_depth < 1:
            return []

        graph = _build_graph(model=model)
        if graph.number_of_edges() == 0:
            return []

        edge_index, _, edges_by_pair = _index_navigation_edges(model=model)
        page_type_names = _page_type_name_map(model=model)
        page_type_features = _page_type_feature_map(model=model)
        all_nodes = sorted(graph.nodes)
        start_nodes = [node for node in all_nodes if graph.in_degree(node) == 0]
        if not start_nodes:
            start_nodes = all_nodes

        seen_paths: set[tuple[str, ...]] = set()
        scenarios: list[FlowScenario] = []
        scenario_index = 1

        for source in start_nodes:
            for target in all_nodes:
                if source == target:
                    continue
                for node_path in nx.all_simple_paths(
                    graph,
                    source=source,
                    target=target,
                    cutoff=max_depth,
                ):
                    if len(node_path) < 2:
                        continue
                    path_key = tuple(node_path)
                    if path_key in seen_paths:
                        continue
                    seen_paths.add(path_key)

                    path_edge_ids = _resolve_path_edge_ids(
                        node_path=node_path,
                        edge_index=edge_index,
                        edges_by_pair=edges_by_pair,
                    )
                    scenarios.append(
                        _build_scenario(
                            strategy="all_paths",
                            scenario_index=scenario_index,
                            node_path=node_path,
                            edge_ids=path_edge_ids,
                            edge_index=edge_index,
                            page_type_names=page_type_names,
                            page_type_features=page_type_features,
                        ),
                    )
                    scenario_index += 1

        return scenarios


def _build_edge_coverage_walks(
    *,
    graph: nx.DiGraph,
    edge_index: dict[int, NavigationEdge],
    outgoing_edges: dict[str, list[int]],
    edges_by_pair: dict[tuple[str, str], list[int]],
) -> list[tuple[list[str], list[int]]]:
    """Build edge-covering walks with CPP-first strategy and deterministic fallback."""
    walks: list[tuple[list[str], list[int]]] = []
    for component_nodes in _edge_connected_components(graph=graph):
        component_edge_ids = _component_edge_ids(
            component_nodes=component_nodes,
            edge_index=edge_index,
        )
        if not component_edge_ids:
            continue

        cpp_walk = _try_directed_cpp_walk(
            component_nodes=component_nodes,
            component_edge_ids=component_edge_ids,
            edge_index=edge_index,
            edges_by_pair=edges_by_pair,
        )
        if cpp_walk is not None:
            walks.append(cpp_walk)
            continue

        walks.extend(
            _fallback_component_edge_walks(
                component_nodes=component_nodes,
                component_edge_ids=component_edge_ids,
                edge_index=edge_index,
                outgoing_edges=outgoing_edges,
                edges_by_pair=edges_by_pair,
            ),
        )

    return walks


def _edge_connected_components(
    *,
    graph: nx.DiGraph,
) -> list[set[str]]:
    """Return weakly connected components that contain at least one edge."""
    edge_nodes = {node for edge in graph.edges for node in edge}
    if not edge_nodes:
        return []

    component_graph = graph.subgraph(edge_nodes).copy()
    components = [
        set(nodes) for nodes in nx.weakly_connected_components(component_graph)
    ]
    return sorted(components, key=lambda nodes: min(nodes))


def _component_edge_ids(
    *,
    component_nodes: set[str],
    edge_index: dict[int, NavigationEdge],
) -> set[int]:
    """Collect edge IDs fully contained inside a node component."""
    return {
        edge_id
        for edge_id, edge in edge_index.items()
        if edge.from_page_type in component_nodes
        and edge.to_page_type in component_nodes
    }


def _component_graph(
    *,
    component_nodes: set[str],
    component_edge_ids: set[int],
    edge_index: dict[int, NavigationEdge],
) -> nx.DiGraph:
    """Build a directed graph from a component edge set."""
    component_graph = nx.DiGraph()
    component_graph.add_nodes_from(component_nodes)
    for edge_id in component_edge_ids:
        edge = edge_index[edge_id]
        component_graph.add_edge(edge.from_page_type, edge.to_page_type)
    return component_graph


def _try_directed_cpp_walk(
    *,
    component_nodes: set[str],
    component_edge_ids: set[int],
    edge_index: dict[int, NavigationEdge],
    edges_by_pair: dict[tuple[str, str], list[int]],
) -> tuple[list[str], list[int]] | None:
    """Attempt a directed-CPP style Eulerian walk for one component.

    The strategy balances node in/out degree with min-cost matching over
    shortest directed paths, then computes an Eulerian traversal.
    """
    component_graph = _component_graph(
        component_nodes=component_nodes,
        component_edge_ids=component_edge_ids,
        edge_index=edge_index,
    )
    active_nodes = [
        node_id
        for node_id in component_graph.nodes
        if component_graph.in_degree(node_id) + component_graph.out_degree(node_id) > 0
    ]
    if not active_nodes:
        return None

    active_subgraph = component_graph.subgraph(active_nodes).copy()
    if not nx.is_strongly_connected(active_subgraph):
        return None

    imbalance = {
        node_id: component_graph.out_degree(node_id)
        - component_graph.in_degree(node_id)
        for node_id in active_nodes
    }
    requires_outgoing = [
        node_id for node_id in active_nodes for _ in range(max(-imbalance[node_id], 0))
    ]
    requires_incoming = [
        node_id for node_id in active_nodes for _ in range(max(imbalance[node_id], 0))
    ]
    if len(requires_outgoing) != len(requires_incoming):
        return None

    extra_edge_ids: list[int] = []
    if requires_outgoing:
        pairings = _min_cost_imbalance_pairings(
            graph=active_subgraph,
            requires_outgoing=requires_outgoing,
            requires_incoming=requires_incoming,
        )
        if pairings is None:
            return None
        for source_node, target_node in pairings:
            shortest_path = nx.shortest_path(
                active_subgraph,
                source=source_node,
                target=target_node,
            )
            path_edge_ids = _resolve_path_edge_ids(
                node_path=shortest_path,
                edge_index=edge_index,
                edges_by_pair=edges_by_pair,
            )
            if not path_edge_ids:
                return None
            extra_edge_ids.extend(path_edge_ids)

    traversal_graph = nx.MultiDiGraph()
    traversal_graph.add_nodes_from(component_nodes)
    for edge_id in sorted(component_edge_ids):
        edge = edge_index[edge_id]
        traversal_graph.add_edge(
            edge.from_page_type,
            edge.to_page_type,
            edge_id=edge_id,
        )
    for edge_id in extra_edge_ids:
        edge = edge_index[edge_id]
        traversal_graph.add_edge(
            edge.from_page_type,
            edge.to_page_type,
            edge_id=edge_id,
        )

    if traversal_graph.number_of_edges() == 0:
        return None

    traversed: list[tuple[str, str, int]]
    if nx.is_eulerian(traversal_graph):
        start_node = min(active_nodes)
        traversed = list(
            nx.eulerian_circuit(
                traversal_graph,
                source=start_node,
                keys=True,
            ),
        )
    elif nx.has_eulerian_path(traversal_graph):
        traversed = list(nx.eulerian_path(traversal_graph, keys=True))
    else:
        return None

    if not traversed:
        return None

    path_nodes = [traversed[0][0], *[to_node for _, to_node, _ in traversed]]
    path_edge_ids = [
        int(traversal_graph[from_node][to_node][key]["edge_id"])
        for from_node, to_node, key in traversed
    ]
    return path_nodes, path_edge_ids


def _min_cost_imbalance_pairings(
    *,
    graph: nx.DiGraph,
    requires_outgoing: Sequence[str],
    requires_incoming: Sequence[str],
) -> list[tuple[str, str]] | None:
    """Solve minimum-cost pairings between imbalance copies."""
    total = len(requires_outgoing)
    if total == 0:
        return []
    if total != len(requires_incoming):
        return None

    flow_graph = nx.DiGraph()
    source = "__source__"
    sink = "__sink__"
    flow_graph.add_node(source, demand=-total)
    flow_graph.add_node(sink, demand=total)

    for out_idx, _ in enumerate(requires_outgoing):
        out_node = f"out:{out_idx}"
        flow_graph.add_node(out_node, demand=0)
        flow_graph.add_edge(source, out_node, capacity=1, weight=0)
    for in_idx, _ in enumerate(requires_incoming):
        in_node = f"in:{in_idx}"
        flow_graph.add_node(in_node, demand=0)
        flow_graph.add_edge(in_node, sink, capacity=1, weight=0)

    for out_idx, source_node in enumerate(requires_outgoing):
        for in_idx, target_node in enumerate(requires_incoming):
            try:
                distance = nx.shortest_path_length(
                    graph,
                    source=source_node,
                    target=target_node,
                )
            except nx.NetworkXNoPath:
                continue
            flow_graph.add_edge(
                f"out:{out_idx}",
                f"in:{in_idx}",
                capacity=1,
                weight=int(distance),
            )

    try:
        flow_dict = nx.min_cost_flow(flow_graph)
    except nx.NetworkXException:
        return None

    pairings: list[tuple[str, str]] = []
    for out_idx, source_node in enumerate(requires_outgoing):
        out_node = f"out:{out_idx}"
        matches = [
            in_node
            for in_node, flow in flow_dict.get(out_node, {}).items()
            if in_node.startswith("in:") and flow == 1
        ]
        if len(matches) != 1:
            return None
        in_idx = int(matches[0].split(":", maxsplit=1)[1])
        pairings.append((source_node, requires_incoming[in_idx]))

    return pairings


def _fallback_component_edge_walks(
    *,
    component_nodes: set[str],
    component_edge_ids: set[int],
    edge_index: dict[int, NavigationEdge],
    outgoing_edges: dict[str, list[int]],
    edges_by_pair: dict[tuple[str, str], list[int]],
) -> list[tuple[list[str], list[int]]]:
    """Fallback edge coverage for non-CPP components.

    Uses greedy uncovered-edge traversal and shortest-path stitching to
    reduce path fragmentation while guaranteeing full edge coverage.
    """
    component_graph = _component_graph(
        component_nodes=component_nodes,
        component_edge_ids=component_edge_ids,
        edge_index=edge_index,
    )
    uncovered = set(component_edge_ids)
    walks: list[tuple[list[str], list[int]]] = []

    while uncovered:
        seed_edge_id = min(
            uncovered,
            key=lambda edge_id: _edge_sort_key(
                edge=edge_index[edge_id], edge_id=edge_id
            ),
        )
        current = edge_index[seed_edge_id].from_page_type
        path_nodes = [current]
        path_edge_ids: list[int] = []

        while uncovered:
            next_edge_id = _next_uncovered_edge_from_node(
                node_id=current,
                uncovered=uncovered,
                outgoing_edges=outgoing_edges,
            )
            if next_edge_id is not None:
                edge = edge_index[next_edge_id]
                path_edge_ids.append(next_edge_id)
                path_nodes.append(edge.to_page_type)
                current = edge.to_page_type
                uncovered.discard(next_edge_id)
                continue

            next_sources = {edge_index[edge_id].from_page_type for edge_id in uncovered}
            shortest_path = _shortest_path_to_any(
                graph=component_graph,
                source=current,
                targets=next_sources,
            )
            if shortest_path is None or len(shortest_path) < 2:
                break

            bridge_edge_ids = _resolve_path_edge_ids(
                node_path=shortest_path,
                edge_index=edge_index,
                edges_by_pair=edges_by_pair,
            )
            if not bridge_edge_ids:
                break

            for bridge_edge_id in bridge_edge_ids:
                bridge_edge = edge_index[bridge_edge_id]
                path_edge_ids.append(bridge_edge_id)
                path_nodes.append(bridge_edge.to_page_type)
                uncovered.discard(bridge_edge_id)
            current = path_nodes[-1]

        if path_edge_ids:
            walks.append((path_nodes, path_edge_ids))
            continue

        # Absolute fallback to avoid infinite loops on malformed graphs.
        edge = edge_index[seed_edge_id]
        uncovered.discard(seed_edge_id)
        walks.append(([edge.from_page_type, edge.to_page_type], [seed_edge_id]))

    return walks


def _next_uncovered_edge_from_node(
    *,
    node_id: str,
    uncovered: set[int],
    outgoing_edges: dict[str, list[int]],
) -> int | None:
    """Select the best uncovered outgoing edge from a node."""
    candidates = [
        edge_id for edge_id in outgoing_edges.get(node_id, []) if edge_id in uncovered
    ]
    if not candidates:
        return None
    return candidates[0]


def _build_graph(
    *,
    model: SiteModel,
) -> nx.DiGraph:
    """Build a directed graph from SiteModel page types and navigation edges."""
    graph = nx.DiGraph()
    for page_type in model.page_types:
        graph.add_node(page_type.page_type_id)
    for edge in model.navigation_edges:
        graph.add_edge(edge.from_page_type, edge.to_page_type)
    return graph


def _page_type_name_map(
    *,
    model: SiteModel,
) -> dict[str, str]:
    """Build page type ID -> display name mapping with sane fallbacks."""
    names: dict[str, str] = {}
    for page_type in model.page_types:
        names[page_type.page_type_id] = page_type.name or page_type.page_type_id
    return names


def _page_type_feature_map(
    *,
    model: SiteModel,
) -> dict[str, set[str]]:
    """Build page type ID -> feature set lookup."""
    return {
        page_type.page_type_id: set(page_type.features)
        for page_type in model.page_types
    }


def _index_navigation_edges(
    *,
    model: SiteModel,
) -> tuple[
    dict[int, NavigationEdge], dict[str, list[int]], dict[tuple[str, str], list[int]]
]:
    """Index edges for fast lookup by id, source node, and node-pair."""
    edge_index: dict[int, NavigationEdge] = {}
    outgoing_edges: dict[str, list[int]] = {}
    edges_by_pair: dict[tuple[str, str], list[int]] = {}

    for edge_id, edge in enumerate(model.navigation_edges):
        edge_index[edge_id] = edge
        outgoing_edges.setdefault(edge.from_page_type, []).append(edge_id)
        edges_by_pair.setdefault((edge.from_page_type, edge.to_page_type), []).append(
            edge_id,
        )

    for edge_ids in outgoing_edges.values():
        edge_ids.sort(key=lambda eid: _edge_sort_key(edge=edge_index[eid], edge_id=eid))
    for edge_ids in edges_by_pair.values():
        edge_ids.sort(key=lambda eid: _edge_sort_key(edge=edge_index[eid], edge_id=eid))

    return edge_index, outgoing_edges, edges_by_pair


def _edge_sort_key(
    *,
    edge: NavigationEdge,
    edge_id: int,
) -> tuple[int, str, str, str, int]:
    """Stable sort key prioritizing high-frequency edges first."""
    return (
        -max(edge.occurrence_count, 1),
        edge.to_page_type,
        edge.action_type.value,
        edge.trigger,
        edge_id,
    )


def _resolve_path_edge_ids(
    *,
    node_path: Sequence[str],
    edge_index: dict[int, NavigationEdge],
    edges_by_pair: dict[tuple[str, str], list[int]],
) -> list[int]:
    """Resolve one concrete edge id for each consecutive node transition."""
    if len(node_path) < 2:
        return []

    edge_ids: list[int] = []
    for from_node, to_node in zip(node_path, node_path[1:], strict=False):
        pair_ids = edges_by_pair.get((from_node, to_node), [])
        if not pair_ids:
            continue
        edge_ids.append(pair_ids[0])

    return edge_ids


def _shortest_path_to_any(
    *,
    graph: nx.DiGraph,
    source: str,
    targets: set[str],
) -> list[str] | None:
    """Find the shortest directed path from ``source`` to any target node."""
    best_path: list[str] | None = None
    for target in sorted(targets):
        try:
            candidate = nx.shortest_path(graph, source=source, target=target)
        except nx.NetworkXNoPath:
            continue
        if best_path is None:
            best_path = candidate
            continue
        if len(candidate) < len(best_path):
            best_path = candidate
            continue
        if len(candidate) == len(best_path) and tuple(candidate) < tuple(best_path):
            best_path = candidate
    return best_path


def _build_scenario(
    *,
    strategy: str,
    scenario_index: int,
    node_path: Sequence[str],
    edge_ids: Sequence[int],
    edge_index: dict[int, NavigationEdge],
    page_type_names: dict[str, str],
    page_type_features: dict[str, set[str]],
) -> FlowScenario:
    """Create a FlowScenario for a concrete node/edge traversal path."""
    node_sequence = list(node_path)
    if not node_sequence:
        return FlowScenario(
            scenario_id=f"mbt-{strategy}-{scenario_index}",
            name=f"MBT {strategy.replace('_', ' ')} path {scenario_index}",
            description=f"Model-based walk generated by {strategy} strategy.",
            page_type_sequence=[],
            steps=[],
            priority="important",
            template=f"mbt_{strategy}",
            tags=["mbt", strategy],
        )

    first_node = node_sequence[0]
    final_node = node_sequence[-1]
    first_name = page_type_names.get(first_node, first_node)
    final_name = page_type_names.get(final_node, final_node)

    steps: list[ScenarioStep] = [
        ScenarioStep(
            page_type=first_node,
            action_description=f"Navigate to {first_name}",
            action_type=ActionType.NAVIGATE,
            expected_outcome=f"{first_name} is reachable",
        ),
    ]
    guard_context = {
        "has_input": False,
        "has_form_submission": False,
    }

    for edge_id in edge_ids:
        edge = edge_index[edge_id]
        setup_steps = _guard_setup_steps(
            edge=edge,
            page_type_names=page_type_names,
            page_type_features=page_type_features,
            guard_context=guard_context,
        )
        steps.extend(setup_steps)

        target_name = page_type_names.get(edge.to_page_type, edge.to_page_type)
        trigger = edge.trigger.strip() or edge.action_type.value
        expected_outcome = f"Transition reaches {target_name}"
        guards = sorted(set(getattr(edge, "guards", [])))
        if guards:
            expected_outcome = (
                f"{expected_outcome} with guard preconditions: " + ", ".join(guards)
            )
        steps.append(
            ScenarioStep(
                page_type=edge.from_page_type,
                action_description=f"{edge.action_type.value} via {trigger}",
                action_type=edge.action_type,
                expected_outcome=expected_outcome,
            ),
        )
        if edge.action_type in _INPUT_ACTION_TYPES:
            guard_context["has_input"] = True
        if edge.action_type == ActionType.SUBMIT_FORM:
            guard_context["has_form_submission"] = True

    steps.append(
        ScenarioStep(
            page_type=final_node,
            action_description=f"Verify {final_name} state",
            expected_outcome=f"{final_name} remains stable after traversal",
        ),
    )

    return FlowScenario(
        scenario_id=f"mbt-{strategy}-{scenario_index}",
        name=f"MBT {strategy.replace('_', ' ')} path {scenario_index}",
        description=f"Model-based walk generated by {strategy} strategy.",
        page_type_sequence=node_sequence,
        steps=steps,
        priority="important" if strategy != "random" else "nice-to-have",
        template=f"mbt_{strategy}",
        tags=["mbt", strategy],
    )


_INPUT_ACTION_TYPES = {
    ActionType.FILL,
    ActionType.SELECT_OPTION,
    ActionType.CHECK,
    ActionType.UNCHECK,
    ActionType.PRESS_KEY,
}


def _guard_setup_steps(
    *,
    edge: NavigationEdge,
    page_type_names: dict[str, str],
    page_type_features: dict[str, set[str]],
    guard_context: dict[str, bool],
) -> list[ScenarioStep]:
    """Build precondition steps required by inferred edge guards."""
    guards = sorted(set(getattr(edge, "guards", [])))
    if not guards:
        return []

    source_name = page_type_names.get(edge.from_page_type, edge.from_page_type)
    source_features = page_type_features.get(edge.from_page_type, set())
    steps: list[ScenarioStep] = []

    for guard in guards:
        if guard == "requires_input":
            if guard_context["has_input"]:
                continue
            steps.append(
                ScenarioStep(
                    page_type=edge.from_page_type,
                    action_description="Fill required input (guard precondition)",
                    action_type=ActionType.FILL,
                    expected_outcome=(
                        f"{source_name} satisfies transition input precondition"
                    ),
                ),
            )
            guard_context["has_input"] = True
            continue

        if guard == "requires_form_submission":
            if guard_context["has_form_submission"]:
                continue
            steps.append(
                ScenarioStep(
                    page_type=edge.from_page_type,
                    action_description="Submit form (guard precondition)",
                    action_type=ActionType.SUBMIT_FORM,
                    expected_outcome=(
                        f"{source_name} satisfies form submission precondition"
                    ),
                ),
            )
            guard_context["has_form_submission"] = True
            continue

        if not guard.startswith("requires_"):
            continue
        feature = guard.removeprefix("requires_")
        feature_present = (
            feature in source_features or f"has_{feature}" in source_features
        )
        steps.append(
            ScenarioStep(
                page_type=edge.from_page_type,
                action_description=f"Validate guard precondition: {guard}",
                action_type=None,
                expected_outcome=(
                    f"{source_name} has required feature '{feature}'"
                    if feature_present
                    else f"{source_name} is missing required feature '{feature}'"
                ),
            ),
        )

    return steps

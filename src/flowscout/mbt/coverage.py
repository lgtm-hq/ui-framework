"""Coverage metrics for MBT scenarios against a SiteModel."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import networkx as nx
from pydantic import BaseModel, Field

from flowscout.core.action_types import ActionType
from flowscout.modeling.scenarios import FlowScenario
from flowscout.modeling.site_model import SiteModel


class ModelCoverage(BaseModel):
    """Coverage metrics for a scenario set over a site model."""

    state_coverage: float = 0.0
    edge_coverage: float = 0.0
    path_coverage: float = 0.0
    covered_states: int = 0
    total_states: int = 0
    covered_edges: int = 0
    total_edges: int = 0
    covered_paths: int = 0
    total_paths: int = 0
    uncovered_states: list[str] = Field(default_factory=list)
    uncovered_edges: list[tuple[str, str, str]] = Field(default_factory=list)
    coverage_matrix: dict[str, dict[str, bool]] = Field(default_factory=dict)


def compute_model_coverage(
    *,
    model: SiteModel,
    scenarios: Sequence[FlowScenario | dict[str, Any]] | None = None,
    max_path_depth: int = 5,
) -> ModelCoverage:
    """Compute state/edge/path coverage for a model and scenario set.

    Args:
        model: Site model used as the coverage baseline.
        scenarios: Optional scenarios to evaluate. Defaults to model scenarios.
        max_path_depth: Maximum depth for simple-path coverage denominator.

    Returns:
        Computed model coverage metrics.
    """
    scenario_models = _normalize_scenarios(
        scenarios=scenarios if scenarios is not None else model.test_scenarios,
    )
    all_states = _all_model_states(model=model)
    total_states = len(all_states)

    covered_states = _covered_state_ids(scenarios=scenario_models)
    covered_state_ids = covered_states & all_states
    uncovered_states = sorted(all_states - covered_state_ids)

    edge_keys = _model_edge_keys(model=model)
    covered_edge_keys = _covered_edge_keys(
        model=model,
        scenarios=scenario_models,
    )
    covered_edge_ids = covered_edge_keys & edge_keys
    uncovered_edges = sorted(edge_keys - covered_edge_ids)

    coverage_matrix = _build_coverage_matrix(
        model=model,
        covered_edge_keys=covered_edge_ids,
    )

    covered_paths, total_paths = _path_coverage_counts(
        model=model,
        scenarios=scenario_models,
        max_path_depth=max_path_depth,
    )

    return ModelCoverage(
        state_coverage=_percentage(
            covered=len(covered_state_ids),
            total=total_states,
        ),
        edge_coverage=_percentage(
            covered=len(covered_edge_ids),
            total=len(edge_keys),
        ),
        path_coverage=_percentage(
            covered=covered_paths,
            total=total_paths,
        ),
        covered_states=len(covered_state_ids),
        total_states=total_states,
        covered_edges=len(covered_edge_ids),
        total_edges=len(edge_keys),
        covered_paths=covered_paths,
        total_paths=total_paths,
        uncovered_states=uncovered_states,
        uncovered_edges=uncovered_edges,
        coverage_matrix=coverage_matrix,
    )


def _normalize_scenarios(
    *,
    scenarios: Sequence[FlowScenario | dict[str, Any] | Any],
) -> list[FlowScenario]:
    """Normalize scenario payloads into FlowScenario models."""
    normalized: list[FlowScenario] = []
    for scenario in scenarios:
        if isinstance(scenario, FlowScenario):
            normalized.append(scenario)
            continue
        normalized.append(FlowScenario.model_validate(scenario))
    return normalized


def _all_model_states(*, model: SiteModel) -> set[str]:
    """Collect state/page identifiers from page types and edges."""
    states = {page_type.page_type_id for page_type in model.page_types}
    for edge in model.navigation_edges:
        states.add(edge.from_page_type)
        states.add(edge.to_page_type)
    return states


def _covered_state_ids(*, scenarios: Sequence[FlowScenario]) -> set[str]:
    """Collect all state/page identifiers referenced by scenarios."""
    covered: set[str] = set()
    for scenario in scenarios:
        covered.update(scenario.page_type_sequence)
        covered.update(step.page_type for step in scenario.steps if step.page_type)
    return covered


def _model_edge_keys(*, model: SiteModel) -> set[tuple[str, str, str]]:
    """Build unique edge keys from the model."""
    return {
        (
            edge.from_page_type,
            edge.to_page_type,
            edge.action_type.value,
        )
        for edge in model.navigation_edges
    }


def _covered_edge_keys(
    *,
    model: SiteModel,
    scenarios: Sequence[FlowScenario],
) -> set[tuple[str, str, str]]:
    """Infer covered model edges from scenario traversals."""
    pair_to_edges: dict[tuple[str, str], set[tuple[str, str, str]]] = {}
    for edge in model.navigation_edges:
        key = (edge.from_page_type, edge.to_page_type, edge.action_type.value)
        pair_to_edges.setdefault((edge.from_page_type, edge.to_page_type), set()).add(
            key,
        )

    covered: set[tuple[str, str, str]] = set()
    for scenario in scenarios:
        action_sequence = [
            step.action_type
            for step in scenario.steps
            if step.action_type not in (None, ActionType.NAVIGATE)
        ]
        for idx, (from_state, to_state) in enumerate(
            zip(
                scenario.page_type_sequence,
                scenario.page_type_sequence[1:],
                strict=False,
            ),
        ):
            pair_edges = pair_to_edges.get((from_state, to_state), set())
            if not pair_edges:
                continue

            action_type = action_sequence[idx] if idx < len(action_sequence) else None
            if action_type is None:
                covered.update(pair_edges)
                continue

            exact_key = (from_state, to_state, action_type.value)
            if exact_key in pair_edges:
                covered.add(exact_key)
                continue

            covered.update(pair_edges)

    return covered


def _build_coverage_matrix(
    *,
    model: SiteModel,
    covered_edge_keys: set[tuple[str, str, str]],
) -> dict[str, dict[str, bool]]:
    """Build page-type x action coverage matrix."""
    row_actions: dict[str, set[str]] = {}
    for edge in model.navigation_edges:
        row_actions.setdefault(edge.from_page_type, set()).add(edge.action_type.value)

    matrix: dict[str, dict[str, bool]] = {}
    for page_type_id in sorted(row_actions):
        actions = row_actions[page_type_id]
        matrix[page_type_id] = {
            action_name: any(
                edge_key[0] == page_type_id and edge_key[2] == action_name
                for edge_key in covered_edge_keys
            )
            for action_name in sorted(actions)
        }
    return matrix


def _path_coverage_counts(
    *,
    model: SiteModel,
    scenarios: Sequence[FlowScenario],
    max_path_depth: int,
) -> tuple[int, int]:
    """Compute covered/possible simple path counts up to max depth."""
    if max_path_depth < 1:
        return 0, 0

    graph = nx.DiGraph()
    graph.add_nodes_from(_all_model_states(model=model))
    for edge in model.navigation_edges:
        graph.add_edge(edge.from_page_type, edge.to_page_type)

    possible_paths: set[tuple[str, ...]] = set()
    nodes = sorted(graph.nodes)
    for source in nodes:
        for target in nodes:
            if source == target:
                continue
            for node_path in nx.all_simple_paths(
                graph,
                source=source,
                target=target,
                cutoff=max_path_depth,
            ):
                if len(node_path) > 1:
                    possible_paths.add(tuple(node_path))

    exercised_paths: set[tuple[str, ...]] = set()
    for scenario in scenarios:
        path = tuple(scenario.page_type_sequence)
        if len(path) < 2:
            continue
        if len(path) - 1 > max_path_depth:
            continue
        if len(set(path)) != len(path):
            continue
        if all(
            graph.has_edge(from_state, to_state)
            for from_state, to_state in zip(path, path[1:], strict=False)
        ):
            exercised_paths.add(path)

    covered_paths = len(exercised_paths & possible_paths)
    total_paths = len(possible_paths)
    return covered_paths, total_paths


def _percentage(*, covered: int, total: int) -> float:
    """Return rounded percentage with a safe 0-denominator default."""
    if total == 0:
        return 100.0
    return round((covered / total) * 100.0, 1)

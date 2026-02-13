"""Tests for MBT model coverage metrics."""

from __future__ import annotations

from flowscout.core.action_types import ActionType
from flowscout.mbt.coverage import compute_model_coverage
from flowscout.modeling.scenarios import FlowScenario, ScenarioStep
from flowscout.modeling.site_model import NavigationEdge, PageType, SiteModel


def _page(page_type_id: str, name: str) -> PageType:
    """Create a minimal page type fixture."""
    return PageType(
        page_type_id=page_type_id,
        name=name,
    )


def _edge(
    from_page_type: str,
    to_page_type: str,
    *,
    action_type: ActionType = ActionType.CLICK,
    trigger: str = "",
) -> NavigationEdge:
    """Create a navigation edge fixture."""
    return NavigationEdge(
        from_page_type=from_page_type,
        to_page_type=to_page_type,
        trigger=trigger or f"{from_page_type}->{to_page_type}",
        action_type=action_type,
        occurrence_count=1,
    )


def _scenario(
    scenario_id: str,
    sequence: list[str],
    action_types: list[ActionType],
) -> FlowScenario:
    """Create an MBT-like scenario over a page sequence."""
    steps = [
        ScenarioStep(
            page_type=sequence[0] if sequence else "",
            action_description="Navigate",
            action_type=ActionType.NAVIGATE,
        ),
    ]
    for page_type, action_type in zip(sequence, action_types, strict=False):
        steps.append(
            ScenarioStep(
                page_type=page_type,
                action_description=f"{action_type.value} via step",
                action_type=action_type,
            ),
        )

    return FlowScenario(
        scenario_id=scenario_id,
        name=scenario_id,
        description="coverage test",
        page_type_sequence=sequence,
        steps=steps,
        priority="important",
        template="mbt_edge_coverage",
        tags=["mbt"],
    )


def test_compute_model_coverage_reports_full_state_and_edge_coverage() -> None:
    """Edge-walk scenarios should fully cover the traversed model."""
    model = SiteModel(
        page_types=[
            _page("home", "Home"),
            _page("catalog", "Catalog"),
            _page("detail", "Detail"),
        ],
        navigation_edges=[
            _edge("home", "catalog", trigger="Open catalog"),
            _edge("catalog", "detail", trigger="Open detail"),
        ],
    )
    scenarios = [
        _scenario(
            scenario_id="scenario-1",
            sequence=["home", "catalog", "detail"],
            action_types=[ActionType.CLICK, ActionType.CLICK],
        ),
    ]

    coverage = compute_model_coverage(
        model=model,
        scenarios=scenarios,
    )

    assert coverage.state_coverage == 100.0
    assert coverage.edge_coverage == 100.0
    assert coverage.covered_states == 3
    assert coverage.covered_edges == 2
    assert coverage.uncovered_states == []
    assert coverage.uncovered_edges == []
    assert coverage.coverage_matrix["home"]["click"] is True
    assert coverage.coverage_matrix["catalog"]["click"] is True


def test_compute_model_coverage_lists_uncovered_states_and_edges() -> None:
    """Coverage output should include explicit uncovered state and edge lists."""
    model = SiteModel(
        page_types=[
            _page("home", "Home"),
            _page("search", "Search"),
            _page("detail", "Detail"),
        ],
        navigation_edges=[
            _edge("home", "search", action_type=ActionType.CLICK),
            _edge("search", "detail", action_type=ActionType.SUBMIT_FORM),
        ],
    )
    scenarios = [
        _scenario(
            scenario_id="scenario-1",
            sequence=["home", "search"],
            action_types=[ActionType.CLICK],
        ),
    ]

    coverage = compute_model_coverage(
        model=model,
        scenarios=scenarios,
    )

    assert coverage.state_coverage == 66.7
    assert coverage.edge_coverage == 50.0
    assert coverage.uncovered_states == ["detail"]
    assert coverage.uncovered_edges == [("search", "detail", "submit_form")]
    assert coverage.coverage_matrix["search"]["submit_form"] is False


def test_compute_model_coverage_path_metric_uses_simple_paths() -> None:
    """Path coverage should compare exercised simple paths to model simple paths."""
    model = SiteModel(
        page_types=[
            _page("a", "A"),
            _page("b", "B"),
            _page("c", "C"),
        ],
        navigation_edges=[
            _edge("a", "b"),
            _edge("b", "c"),
            _edge("a", "c"),
        ],
    )
    scenarios = [
        _scenario(
            scenario_id="scenario-1",
            sequence=["a", "b", "c"],
            action_types=[ActionType.CLICK, ActionType.CLICK],
        ),
    ]

    coverage = compute_model_coverage(
        model=model,
        scenarios=scenarios,
        max_path_depth=2,
    )

    assert coverage.total_paths == 4
    assert coverage.covered_paths == 1
    assert coverage.path_coverage == 25.0

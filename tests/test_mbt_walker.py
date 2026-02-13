"""Tests for model-based graph walking strategies."""

from __future__ import annotations

from pathlib import Path

from flowscout.core.action_types import ActionType
from flowscout.mbt import ModelWalker
from flowscout.modeling.scenarios import FlowScenario
from flowscout.modeling.site_model import NavigationEdge, PageType, SiteModel


def _page(
    page_type_id: str,
    name: str,
) -> PageType:
    """Create a minimal page type for MBT tests."""
    return PageType(
        page_type_id=page_type_id,
        name=name,
    )


def _edge(
    from_page_type: str,
    to_page_type: str,
    trigger: str,
    action_type: ActionType = ActionType.CLICK,
    occurrence_count: int = 1,
) -> NavigationEdge:
    """Create a navigation edge with deterministic defaults."""
    return NavigationEdge(
        from_page_type=from_page_type,
        to_page_type=to_page_type,
        trigger=trigger,
        action_type=action_type,
        occurrence_count=occurrence_count,
    )


def _edge_steps(
    scenario: FlowScenario,
) -> list[tuple[str, str, ActionType | None, str]]:
    """Extract traversed edge information from a generated scenario."""
    traversed = [step for step in scenario.steps if " via " in step.action_description]
    return [
        (
            scenario.page_type_sequence[idx],
            scenario.page_type_sequence[idx + 1],
            step.action_type,
            step.action_description,
        )
        for idx, step in enumerate(traversed)
    ]


class TestModelWalker:
    def test_edge_coverage_prefers_single_walk_for_cpp_component(self) -> None:
        """Strongly connected components should use one Eulerian-style walk."""
        model = SiteModel(
            page_types=[
                _page("a", "A"),
                _page("b", "B"),
                _page("c", "C"),
            ],
            navigation_edges=[
                _edge("a", "b", trigger="A to B"),
                _edge("b", "c", trigger="B to C"),
                _edge("c", "a", trigger="C to A"),
                _edge("a", "c", trigger="A to C"),
            ],
        )

        walker = ModelWalker()
        scenarios = walker.walk_edge_coverage(model=model)
        covered_pairs = {
            (from_node, to_node)
            for scenario in scenarios
            for from_node, to_node, _, _ in _edge_steps(scenario=scenario)
        }

        assert len(scenarios) == 1
        assert ("a", "b") in covered_pairs
        assert ("b", "c") in covered_pairs
        assert ("c", "a") in covered_pairs
        assert ("a", "c") in covered_pairs

    def test_edge_coverage_touches_every_navigation_edge(self) -> None:
        """Edge coverage output should include all SiteModel transitions."""
        model = SiteModel(
            page_types=[
                _page("home", "Home"),
                _page("catalog", "Catalog"),
                _page("detail", "Detail"),
            ],
            navigation_edges=[
                _edge("home", "catalog", trigger="Open catalog", occurrence_count=5),
                _edge("catalog", "detail", trigger="View detail", occurrence_count=3),
                _edge("detail", "home", trigger="Back home", occurrence_count=2),
                _edge("home", "detail", trigger="Quick jump", occurrence_count=1),
            ],
        )

        walker = ModelWalker()
        scenarios = walker.walk_edge_coverage(model=model)

        covered_edges = [
            covered
            for scenario in scenarios
            for covered in _edge_steps(scenario=scenario)
        ]

        assert scenarios
        for edge in model.navigation_edges:
            assert any(
                from_node == edge.from_page_type
                and to_node == edge.to_page_type
                and action_type == edge.action_type
                and edge.trigger in description
                for from_node, to_node, action_type, description in covered_edges
            )

    def test_edge_coverage_splits_disconnected_components(self) -> None:
        """Disconnected edge components should produce separate walks."""
        model = SiteModel(
            page_types=[
                _page("a", "A"),
                _page("b", "B"),
                _page("x", "X"),
                _page("y", "Y"),
            ],
            navigation_edges=[
                _edge("a", "b", trigger="A to B"),
                _edge("b", "a", trigger="B to A"),
                _edge("x", "y", trigger="X to Y"),
                _edge("y", "x", trigger="Y to X"),
            ],
        )

        walker = ModelWalker()
        scenarios = walker.walk_edge_coverage(model=model)

        assert len(scenarios) == 2

    def test_state_coverage_visits_every_page_type(self) -> None:
        """State coverage should collectively include all page types."""
        model = SiteModel(
            page_types=[
                _page("home", "Home"),
                _page("catalog", "Catalog"),
                _page("detail", "Detail"),
                _page("profile", "Profile"),
            ],
            navigation_edges=[
                _edge("home", "catalog", trigger="Open catalog"),
                _edge("catalog", "detail", trigger="View detail"),
            ],
        )

        walker = ModelWalker()
        scenarios = walker.walk_state_coverage(model=model)
        visited = {
            page_type_id
            for scenario in scenarios
            for page_type_id in scenario.page_type_sequence
        }

        assert visited == {"home", "catalog", "detail", "profile"}
        assert all(scenario.template == "mbt_state_coverage" for scenario in scenarios)

    def test_all_paths_respects_depth_and_simple_paths(self) -> None:
        """All-path strategy should keep paths simple and depth-bounded."""
        model = SiteModel(
            page_types=[
                _page("home", "Home"),
                _page("catalog", "Catalog"),
                _page("search", "Search"),
                _page("detail", "Detail"),
            ],
            navigation_edges=[
                _edge("home", "catalog", trigger="Browse"),
                _edge("home", "search", trigger="Search"),
                _edge("catalog", "detail", trigger="Pick from catalog"),
                _edge("search", "detail", trigger="Pick from search"),
                _edge("catalog", "search", trigger="Refine query"),
            ],
        )

        walker = ModelWalker()
        scenarios = walker.walk_all_paths(
            model=model,
            max_depth=3,
        )
        paths = {tuple(scenario.page_type_sequence) for scenario in scenarios}

        assert ("home", "catalog", "detail") in paths
        assert ("home", "search", "detail") in paths
        for scenario in scenarios:
            assert len(scenario.page_type_sequence) - 1 <= 3
            assert len(scenario.page_type_sequence) == len(
                set(scenario.page_type_sequence)
            )

    def test_random_walk_returns_valid_scenario(self) -> None:
        """Random walk should emit a valid flow scenario over model edges."""
        model = SiteModel(
            page_types=[
                _page("home", "Home"),
                _page("catalog", "Catalog"),
            ],
            navigation_edges=[
                _edge("home", "catalog", trigger="Open catalog", occurrence_count=5),
                _edge("catalog", "home", trigger="Go home", occurrence_count=1),
            ],
        )

        walker = ModelWalker()
        scenario = walker.walk_random(
            model=model,
            steps=4,
        )
        valid_pairs = {
            (edge.from_page_type, edge.to_page_type) for edge in model.navigation_edges
        }

        assert scenario.template == "mbt_random"
        assert scenario.page_type_sequence
        assert scenario.steps[0].action_type == ActionType.NAVIGATE
        assert len(scenario.page_type_sequence) <= 5
        assert all(
            pair in valid_pairs
            for pair in zip(
                scenario.page_type_sequence,
                scenario.page_type_sequence[1:],
                strict=False,
            )
        )

    def test_walker_does_not_reference_exploration_result(self) -> None:
        """Walker module should stay model-only and avoid ExplorationResult."""
        source = Path("src/flowscout/mbt/walker.py").read_text()
        assert "ExplorationResult" not in source

"""Tests for exploration graph and flow extraction."""

from flowscout.analysis.graph import ExplorationGraph
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType


def _make_state(
    state_id: str, url: str = "https://example.com", depth: int = 0
) -> PageState:
    return PageState(
        state_id=state_id,
        url=url,
        title=f"Page {state_id}",
        fingerprint=state_id * 6,  # Fake 72-char fingerprint
        depth=depth,
        dom_structure_hash="dom",
        visible_text_hash="text",
        form_state_hash="form",
    )


def _make_action(action_id: str, label: str = "test") -> Action:
    return Action(
        action_id=action_id,
        action_type=ActionType.CLICK,
        target_selector="button",
        label=label,
    )


def _make_result(
    action_id: str,
    source: str,
    target: str,
    outcome: OutcomeType = OutcomeType.NAVIGATION,
) -> ActionResult:
    return ActionResult(
        action_id=action_id,
        source_state_id=source,
        target_state_id=target,
        outcome=outcome,
    )


class TestExplorationGraph:
    def test_add_new_state_returns_true(self) -> None:
        graph = ExplorationGraph()
        state = _make_state("s1")
        assert graph.add_state(state) is True

    def test_add_duplicate_state_returns_false(self) -> None:
        graph = ExplorationGraph()
        state = _make_state("s1")
        graph.add_state(state)
        assert graph.add_state(state) is False

    def test_first_state_becomes_root(self) -> None:
        graph = ExplorationGraph()
        state = _make_state("s1")
        graph.add_state(state)
        assert graph.root_state_id == "s1"

    def test_add_result_creates_edge(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_state(_make_state("s2"))
        graph.add_action(_make_action("a1"))
        graph.add_result(_make_result("a1", "s1", "s2"))
        assert len(graph.results) == 1

    def test_find_path_from_root(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_state(_make_state("s2"))
        graph.add_state(_make_state("s3"))
        graph.add_action(_make_action("a1"))
        graph.add_action(_make_action("a2"))
        graph.add_result(_make_result("a1", "s1", "s2"))
        graph.add_result(_make_result("a2", "s2", "s3"))

        path = graph.find_path_from_root("s3")
        assert path is not None
        assert len(path) == 2
        assert path[0].action_id == "a1"
        assert path[1].action_id == "a2"

    def test_find_path_from_root_to_root(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        path = graph.find_path_from_root("s1")
        assert path == []

    def test_find_path_unreachable(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_state(_make_state("s2"))  # No edge connecting
        path = graph.find_path_from_root("s2")
        assert path is None

    def test_extract_flows_linear(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_state(_make_state("s2"))
        graph.add_state(_make_state("s3"))
        graph.add_action(_make_action("a1", "Click Link"))
        graph.add_action(_make_action("a2", "Click Button"))
        graph.add_result(_make_result("a1", "s1", "s2"))
        graph.add_result(_make_result("a2", "s2", "s3"))

        flows = graph.extract_flows()
        linear_flows = [f for f in flows if not f.is_cycle]
        assert len(linear_flows) == 1
        # Should have a flow from s1 to s3
        long_flow = [f for f in linear_flows if len(f.state_ids) == 3]
        assert len(long_flow) == 1

    def test_extract_flows_with_cycle(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_state(_make_state("s2"))
        graph.add_action(_make_action("a1"))
        graph.add_action(_make_action("a2"))
        graph.add_result(_make_result("a1", "s1", "s2"))
        graph.add_result(_make_result("a2", "s2", "s1"))

        flows = graph.extract_flows()
        cycles = [f for f in flows if f.is_cycle]
        assert len(cycles) >= 1

    def test_to_serializable(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_state(_make_state("s2"))
        graph.add_action(_make_action("a1", "Click"))
        graph.add_result(_make_result("a1", "s1", "s2"))

        data = graph.to_serializable()
        assert "nodes" in data
        assert "edges" in data
        assert len(data["nodes"]) == 2
        assert len(data["edges"]) == 1

    def test_get_stats(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_state(_make_state("s2"))
        graph.add_action(_make_action("a1"))
        graph.add_result(_make_result("a1", "s1", "s2"))

        stats = graph.get_stats()
        assert stats["total_states"] == 2
        assert stats["total_actions_executed"] == 1
        assert stats["outcome_navigation"] == 1

    def test_empty_graph_extract_flows(self) -> None:
        graph = ExplorationGraph()
        flows = graph.extract_flows()
        assert flows == []

    def test_single_state_no_flows(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        flows = graph.extract_flows()
        assert flows == []

    def test_all_timeout_dead_ends(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_state(_make_state("s2"))
        graph.add_action(_make_action("a1"))
        graph.add_result(
            _make_result("a1", "s1", "s2", outcome=OutcomeType.TIMEOUT),
        )
        flows = graph.extract_flows()
        # Should still produce at least one flow even with timeout outcomes
        assert len(flows) >= 1

    def test_self_loop_only_still_produces_flows(self) -> None:
        graph = ExplorationGraph()
        graph.add_state(_make_state("s1"))
        graph.add_action(_make_action("a1", "Click Login"))
        graph.add_result(
            _make_result("a1", "s1", "s1", outcome=OutcomeType.NO_CHANGE),
        )

        flows = graph.extract_flows()
        assert len(flows) >= 1
        assert any(flow.action_ids == ["a1"] for flow in flows)

    def test_fallback_flow_name_includes_action_and_outcome(self) -> None:
        graph = ExplorationGraph()
        state = _make_state("s1")
        state.title = "Swag Labs"
        graph.add_state(state)
        graph.add_action(
            Action(
                action_id="a1",
                action_type=ActionType.CLICK,
                target_selector="#login-button",
                label="Click: Login",
            )
        )
        graph.add_result(
            ActionResult(
                action_id="a1",
                source_state_id="s1",
                target_state_id="s1",
                outcome=OutcomeType.VALIDATION_ERROR,
                observation_notes="Validation error was shown",
            )
        )

        flows = graph.extract_flows()
        assert len(flows) == 1
        assert flows[0].name == "Swag Labs · Click Login · Validation Feedback"
        assert flows[0].description == "Click Login \u2192 Validation error was shown"

    def test_fallback_flow_name_strips_fill_value_noise(self) -> None:
        graph = ExplorationGraph()
        state = _make_state("s1")
        state.title = "Swag Labs"
        graph.add_state(state)
        graph.add_action(
            Action(
                action_id="a1",
                action_type=ActionType.FILL,
                target_selector="#user-name",
                label="Fill: Username = 'janedoe42'",
            )
        )
        graph.add_result(
            ActionResult(
                action_id="a1",
                source_state_id="s1",
                target_state_id="s1",
                outcome=OutcomeType.NO_CHANGE,
            )
        )

        flows = graph.extract_flows()
        assert len(flows) == 1
        assert flows[0].name == "Swag Labs · Enter Username · No Visible Change"
        assert flows[0].description == "Enter Username"

    def test_empty_graph_stats(self) -> None:
        graph = ExplorationGraph()
        stats = graph.get_stats()
        assert stats["total_states"] == 0
        assert stats["total_actions_executed"] == 0

    def test_empty_graph_serializable(self) -> None:
        graph = ExplorationGraph()
        data = graph.to_serializable()
        assert data["nodes"] == []
        assert data["edges"] == []

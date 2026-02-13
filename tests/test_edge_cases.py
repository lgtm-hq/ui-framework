"""Edge case tests for core modules."""

from __future__ import annotations

from typing import Any

import pytest

from flowscout.analysis.element_inventory import summarize_element_inventory
from flowscout.analysis.graph import ExplorationGraph, ExplorationResult
from flowscout.core.state import build_fingerprint
from flowscout.discovery.actions import ActionType, OutcomeType
from flowscout.discovery.intent import infer_intent

from conftest import (
    make_action,
    make_action_result,
    make_element,
    make_exploration_result,
    make_state,
)


class TestBuildFingerprint:
    def test_empty_url(self) -> None:
        fp = build_fingerprint(
            url="",
            title="",
            dom_structure_hash="dom",
            visible_text_hash="text",
            form_state_hash="form",
        )
        assert isinstance(fp, str)
        assert len(fp) == 64  # SHA-256 hex

    def test_same_inputs_produce_same_fingerprint(self) -> None:
        fp1 = build_fingerprint(
            url="https://example.com",
            title="Home",
            dom_structure_hash="d1",
            visible_text_hash="t1",
            form_state_hash="f1",
        )
        fp2 = build_fingerprint(
            url="https://example.com",
            title="Home",
            dom_structure_hash="d1",
            visible_text_hash="t1",
            form_state_hash="f1",
        )
        assert fp1 == fp2

    def test_different_urls_produce_different_fingerprints(self) -> None:
        fp1 = build_fingerprint(
            url="https://a.com",
            title="Page",
            dom_structure_hash="d",
            visible_text_hash="t",
            form_state_hash="f",
        )
        fp2 = build_fingerprint(
            url="https://b.com",
            title="Page",
            dom_structure_hash="d",
            visible_text_hash="t",
            form_state_hash="f",
        )
        assert fp1 != fp2

    def test_unicode_url(self) -> None:
        fp = build_fingerprint(
            url="https://example.com/путь/страница",
            title="Страница",
            dom_structure_hash="dom",
            visible_text_hash="text",
            form_state_hash="form",
        )
        assert isinstance(fp, str)
        assert len(fp) == 64


class TestInferIntent:
    def test_unknown_action_type_raises(self) -> None:
        elem = make_element(selector="button#go", element_type="button", label="Go")
        with pytest.raises(ValueError):
            infer_intent(elem, "some_unknown_type")

    def test_click_on_link(self) -> None:
        elem = make_element(
            selector="a[href='/about']",
            element_type="link",
            label="About",
            tag="a",
        )
        intent = infer_intent(elem, ActionType.CLICK.value)
        assert intent is not None

    def test_fill_on_text_input(self) -> None:
        elem = make_element(
            selector="input[name='email']",
            element_type="input_email",
            label="Email",
            tag="input",
        )
        intent = infer_intent(elem, ActionType.FILL.value)
        assert intent is not None


class TestSummarizeElementInventory:
    def test_empty_analyses(self) -> None:
        result = summarize_element_inventory(analyses={}, states_by_id={})
        assert result["total_elements"] == 0
        assert result["interactive_elements"] == 0
        assert result["non_interactive_elements"] == 0
        assert result["pages_with_elements"] == 0
        assert result["per_page"] == []

    def test_analysis_with_no_catalog(self) -> None:
        analyses = {"s1": {"archetype": "listing"}}
        result = summarize_element_inventory(analyses=analyses, states_by_id={})
        assert result["total_elements"] == 0

    def test_analysis_with_empty_entries(self) -> None:
        analyses: dict[str, dict[str, Any]] = {"s1": {"catalog": {"entries": []}}}
        result = summarize_element_inventory(analyses=analyses, states_by_id={})
        assert result["total_elements"] == 0

    def test_analysis_with_malformed_entry(self) -> None:
        analyses = {"s1": {"catalog": {"entries": ["not_a_dict", 42, None]}}}
        result = summarize_element_inventory(analyses=analyses, states_by_id={})
        assert result["total_elements"] == 0

    def test_states_by_id_none(self) -> None:
        analyses = {"s1": {"catalog": {"entries": [{"element_type": "button"}]}}}
        result = summarize_element_inventory(analyses=analyses, states_by_id=None)
        assert result["total_elements"] == 1
        assert result["per_page"][0]["title"] == ""


class TestExplorationGraphEdgeCases:
    def test_empty_graph(self) -> None:
        graph = ExplorationGraph()
        flows = graph.extract_flows()
        assert flows == []

    def test_single_state_no_actions(self) -> None:
        graph = ExplorationGraph()
        state = make_state(state_id="s0")
        graph.add_state(state)
        flows = graph.extract_flows()
        assert flows == []

    def test_duplicate_state_fingerprints(self) -> None:
        graph = ExplorationGraph()
        s1 = make_state(state_id="s1", url="https://a.com")
        s2 = make_state(state_id="s2", url="https://b.com")
        graph.add_state(s1)
        graph.add_state(s2)
        assert "s1" in graph.states
        assert "s2" in graph.states


class TestExplorationResultEdgeCases:
    def test_empty_result(self) -> None:
        result = ExplorationResult(
            config={"start_url": "https://example.com"},
        )
        assert len(result.states) == 0
        assert len(result.flows) == 0

    def test_result_with_flows_no_verdicts(self) -> None:
        result = make_exploration_result(num_flows=3)
        for flow in result.flows:
            assert flow.is_stable is False
            assert flow.stability_score == 0.0


class TestMakeHelpers:
    """Tests for conftest factory functions to verify they work correctly."""

    def test_make_state_unique_ids(self) -> None:
        s1 = make_state()
        s2 = make_state()
        assert s1.state_id != s2.state_id

    def test_make_state_custom_params(self) -> None:
        s = make_state(
            state_id="custom", url="https://custom.com", title="Custom", depth=3
        )
        assert s.state_id == "custom"
        assert s.url == "https://custom.com"
        assert s.title == "Custom"
        assert s.depth == 3

    def test_make_action_unique_ids(self) -> None:
        a1 = make_action()
        a2 = make_action()
        assert a1.action_id != a2.action_id

    def test_make_action_result_defaults(self) -> None:
        r = make_action_result()
        assert r.outcome == OutcomeType.NAVIGATION
        assert r.duration_ms == 100.0

    def test_make_exploration_result_defaults(self) -> None:
        result = make_exploration_result()
        assert len(result.states) == 2
        assert len(result.flows) == 1
        assert result.config["start_url"] == "https://example.com"

    def test_make_element_defaults(self) -> None:
        elem = make_element()
        assert elem.selector == "button#submit"
        assert elem.element_type == "button"

"""Tests for MBT model exporters."""

from __future__ import annotations

from pathlib import Path

from flowscout.core.action_types import ActionType
from flowscout.mbt.exporters import render_dot, render_graphwalker_json, render_mermaid
from flowscout.modeling.site_model import NavigationEdge, PageType, SiteModel


def _model() -> SiteModel:
    """Build a small SiteModel fixture for exporter tests."""
    return SiteModel(
        page_types=[
            PageType(page_type_id="home", name="Home"),
            PageType(page_type_id="catalog", name="Catalog"),
        ],
        navigation_edges=[
            NavigationEdge(
                from_page_type="home",
                to_page_type="catalog",
                trigger="Open catalog",
                action_type=ActionType.CLICK,
                occurrence_count=3,
                guards=["requires_search"],
                inferred_from="source page features imply guards: requires_search",
            ),
        ],
    )


def test_render_graphwalker_json_contains_vertices_and_transition_labels() -> None:
    """GraphWalker exporter should include nodes and action/count labels."""
    output = render_graphwalker_json(model=_model())

    assert '"models"' in output
    assert '"vertices"' in output
    assert '"edges"' in output
    assert "click (3x)" in output
    assert "requires_search" in output


def test_render_dot_contains_action_type_and_occurrence_count() -> None:
    """DOT exporter should render directed edge labels with MBT metadata."""
    output = render_dot(model=_model())

    assert output.startswith("digraph SiteModel")
    assert '"home" -> "catalog"' in output
    assert "click (3x)" in output
    assert "guard: requires_search" in output


def test_render_mermaid_uses_state_diagram_v2_syntax() -> None:
    """Mermaid exporter should emit valid ``stateDiagram-v2`` syntax."""
    output = render_mermaid(model=_model())

    assert output.startswith("stateDiagram-v2")
    assert "home --> catalog" in output
    assert "click (3x)" in output
    assert "guard: requires_search" in output


def test_exporters_do_not_import_exploration_result() -> None:
    """Exporter modules should stay model-only and avoid layer-1 imports."""
    sources = [
        Path("src/flowscout/mbt/exporters/graphwalker.py").read_text(),
        Path("src/flowscout/mbt/exporters/dot.py").read_text(),
        Path("src/flowscout/mbt/exporters/mermaid.py").read_text(),
    ]
    assert all("ExplorationResult" not in source for source in sources)

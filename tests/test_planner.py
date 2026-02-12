"""Tests for the smart planner."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from flowscout.core.archetypes import (
    PageArchetype,
)
from flowscout.smart.planner import FlowTemplate, PlannerAdvice, SmartPlanner

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_raw(
    archetype_hint: str = "listing",
    item_count: int = 10,
    has_search: bool = False,
    has_pagination: bool = False,
    has_filters: bool = False,
    text_length: int = 2000,
    heading_count: int = 2,
    form_input_count: int = 0,
    has_hero: bool = False,
    has_single_heading_focus: bool = False,
) -> dict[str, Any]:
    """Build a mock raw dict that will classify to the desired archetype."""
    repeated = []
    if archetype_hint in ("listing", "search_results"):
        repeated = [
            {
                "parent_selector": ".grid",
                "count": item_count,
                "tag_signature": "div>a>h3+p",
                "item_texts": [f"Entity {i}" for i in range(min(item_count, 10))],
                "item_selectors": [f".grid > div:nth({i})" for i in range(1, 4)],
            }
        ]

    return {
        "repeated_groups": repeated,
        "content_metrics": {
            "total_text_length": text_length,
            "heading_count": heading_count,
            "h1_texts": ["Page Title"],
            "h2_texts": [],
            "image_count": item_count if archetype_hint == "listing" else 2,
            "link_count": item_count + 5,
            "form_input_count": form_input_count,
            "interactive_count": item_count + 10,
        },
        "zone_hints": {
            "has_nav": True,
            "has_search_input": has_search,
            "has_pagination": has_pagination,
            "has_filters": has_filters,
            "has_hero": has_hero,
            "has_single_heading_focus": has_single_heading_focus,
        },
        "structural_skeleton": f"main(div({archetype_hint}))",
        "extracted_entities": [f"Entity {i}" for i in range(5)],
        "element_catalog": [],
    }


def _mock_state(state_id: str = "s1", url: str = "https://example.com") -> MagicMock:
    state = MagicMock()
    state.state_id = state_id
    state.url = url
    return state


def _mock_browser(raw: dict[str, Any]) -> MagicMock:
    browser = MagicMock()
    browser.analyze_page_structure = AsyncMock(return_value=raw)
    return browser


def _mock_graph() -> MagicMock:
    return MagicMock()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestSmartPlannerBasic:
    """Basic planner functionality."""

    @pytest.mark.asyncio
    async def test_on_state_discovered_returns_advice(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert isinstance(advice, PlannerAdvice)

    @pytest.mark.asyncio
    async def test_archetype_registered(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        dist = planner.registry.archetype_distribution()
        assert "listing" in dist

    @pytest.mark.asyncio
    async def test_entities_extracted(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert planner.context_store.has_entities

    @pytest.mark.asyncio
    async def test_coverage_recorded(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing", has_search=True)
        await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert "search_present" in planner.coverage.state.features_tested

    @pytest.mark.asyncio
    async def test_browser_failure_returns_empty_advice(self):
        planner = SmartPlanner()
        browser = MagicMock()
        browser.analyze_page_structure = AsyncMock(side_effect=RuntimeError("fail"))
        advice = await planner.on_state_discovered(
            _mock_state(), browser, _mock_graph()
        )
        assert isinstance(advice, PlannerAdvice)
        assert len(advice.active_flow_templates) == 0


class TestFlowTemplateDetection:
    """Flow template opportunity detection."""

    @pytest.mark.asyncio
    async def test_listing_triggers_browse_template(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert FlowTemplate.BROWSE.value in advice.active_flow_templates

    @pytest.mark.asyncio
    async def test_listing_with_search_triggers_search_template(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing", has_search=True)
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert FlowTemplate.SEARCH.value in advice.active_flow_templates

    @pytest.mark.asyncio
    async def test_listing_with_pagination_triggers_template(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing", has_pagination=True)
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert FlowTemplate.PAGINATION.value in advice.active_flow_templates

    @pytest.mark.asyncio
    async def test_listing_with_filters_triggers_template(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing", has_filters=True)
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert FlowTemplate.FILTER_VERIFY.value in advice.active_flow_templates

    @pytest.mark.asyncio
    async def test_detail_triggers_verify_template(self):
        planner = SmartPlanner()
        raw = _mock_raw(
            "detail",
            item_count=0,
            text_length=2000,
            has_single_heading_focus=True,
        )
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert FlowTemplate.DETAIL_VERIFY.value in advice.active_flow_templates

    @pytest.mark.asyncio
    async def test_form_triggers_crud_template(self):
        planner = SmartPlanner()
        raw = _mock_raw(
            "form",
            item_count=0,
            form_input_count=6,
            text_length=300,
            has_single_heading_focus=False,
        )
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert FlowTemplate.CRUD.value in advice.active_flow_templates


class TestPriorityOverrides:
    """Priority override generation."""

    @pytest.mark.asyncio
    async def test_listing_boosts_content_items(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert "__content_items__" in advice.priority_overrides
        assert advice.priority_overrides["__content_items__"] < 10

    @pytest.mark.asyncio
    async def test_search_action_boosted(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing", has_search=True)
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert "__search_action__" in advice.priority_overrides

    @pytest.mark.asyncio
    async def test_saturated_archetype_deprioritized(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        # Register 3 times with same skeleton
        for i in range(3):
            await planner.on_state_discovered(
                _mock_state(f"s{i}"), _mock_browser(raw), _mock_graph()
            )
        advice = await planner.on_state_discovered(
            _mock_state("s4"), _mock_browser(raw), _mock_graph()
        )
        assert advice.is_archetype_saturated is True


class TestContextualInputSuggestions:
    """Contextual input value suggestions."""

    @pytest.mark.asyncio
    async def test_search_value_suggested(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing", has_search=True)
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert "__search__" in advice.suggested_input_values
        assert advice.suggested_input_values["__search__"] != "test query"


class TestContentExpectations:
    """Content expectations attached to advice."""

    @pytest.mark.asyncio
    async def test_expectations_present(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        advice = await planner.on_state_discovered(
            _mock_state(), _mock_browser(raw), _mock_graph()
        )
        assert advice.content_expectations is not None
        assert advice.content_expectations.total_count > 0


class TestPlannerState:
    """Planner state retrieval."""

    @pytest.mark.asyncio
    async def test_get_analysis(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        await planner.on_state_discovered(
            _mock_state("s1"), _mock_browser(raw), _mock_graph()
        )
        analysis = planner.get_analysis("s1")
        assert analysis is not None
        assert analysis.archetype == PageArchetype.LISTING

    @pytest.mark.asyncio
    async def test_get_all_catalogs(self):
        planner = SmartPlanner()
        raw = _mock_raw("listing")
        await planner.on_state_discovered(
            _mock_state("s1"), _mock_browser(raw), _mock_graph()
        )
        catalogs = planner.get_all_catalogs()
        assert len(catalogs) > 0

    @pytest.mark.asyncio
    async def test_no_duplicate_templates_on_revisit(self):
        """Once a flow template is detected, it shouldn't re-trigger."""
        planner = SmartPlanner()
        raw = _mock_raw("listing", has_search=True)
        advice1 = await planner.on_state_discovered(
            _mock_state("s1"), _mock_browser(raw), _mock_graph()
        )
        assert FlowTemplate.SEARCH.value in advice1.active_flow_templates

        # Simulate search results discovered (marks search as done)
        planner._flow_features_detected.add(FlowTemplate.SEARCH.value)

        advice2 = await planner.on_state_discovered(
            _mock_state("s2"), _mock_browser(raw), _mock_graph()
        )
        assert FlowTemplate.SEARCH.value not in advice2.active_flow_templates

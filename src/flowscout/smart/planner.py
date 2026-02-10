"""Smart planner — coordinates archetype analysis, coverage, and flow advice."""

from __future__ import annotations

import logging
from enum import StrEnum, auto
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from flowscout.analysis.archetype import (
    ArchetypeRegistry,
    PageAnalysis,
    PageArchetype,
    build_page_analysis,
)
from flowscout.analysis.expectations import ExpectationChecker, ExpectationResult
from flowscout.discovery.context import ContextStore
from flowscout.smart.coverage import CoverageTracker

if TYPE_CHECKING:
    from flowscout.analysis.graph import ExplorationGraph
    from flowscout.core.browser import BrowserManager
    from flowscout.core.state import PageState

logger = logging.getLogger(__name__)


class FlowTemplate(StrEnum):
    BROWSE = auto()
    SEARCH = auto()
    CRUD = auto()
    FILTER_VERIFY = auto()
    PAGINATION = auto()
    DETAIL_VERIFY = auto()


class PlannerAdvice(BaseModel):
    """Advice from the smart planner for the current state."""

    priority_overrides: dict[str, int] = Field(default_factory=dict)
    skip_action_ids: set[str] = Field(default_factory=set)
    suggested_input_values: dict[str, str] = Field(default_factory=dict)
    active_flow_templates: list[str] = Field(default_factory=list)
    is_archetype_saturated: bool = False
    content_expectations: ExpectationResult | None = None


class SmartPlanner:
    """Coordinates archetype recognition, coverage tracking, and flow advice.

    Created once per exploration run when smart mode is enabled.
    """

    def __init__(
        self,
        *,
        archetype_instance_limit: int = 3,
        min_features_before_stop: int = 3,
        min_archetypes_before_stop: int = 2,
        stop_on_saturation: bool = True,
    ) -> None:
        self.registry = ArchetypeRegistry()
        self.coverage = CoverageTracker(
            archetype_instance_limit=archetype_instance_limit,
            min_features_before_stop=min_features_before_stop,
            min_archetypes_before_stop=min_archetypes_before_stop,
            stop_on_saturation=stop_on_saturation,
        )
        self.context_store = ContextStore()
        self._expectation_checker = ExpectationChecker()
        self._analyses: dict[str, PageAnalysis] = {}
        self._flow_features_detected: set[str] = set()

    async def on_state_discovered(
        self,
        state: PageState,
        browser: BrowserManager,
        graph: ExplorationGraph,
    ) -> PlannerAdvice:
        """Analyze a newly discovered state and return exploration advice.

        This is the main entry point called by the Navigator after each new state.
        """
        try:
            raw = await browser.analyze_page_structure()
        except (RuntimeError, OSError):
            logger.debug("Page analysis failed for %s", state.state_id, exc_info=True)
            return PlannerAdvice()

        analysis = build_page_analysis(raw)
        self._analyses[state.state_id] = analysis

        # Register archetype
        self.registry.register(state.state_id, analysis, url=state.url)

        # Track coverage
        self.coverage.record_archetype(
            analysis.archetype.value, analysis.structural_signature
        )

        # Extract entities for contextual input
        self.context_store.extract_from(analysis)

        # Check content expectations
        exp_result = self._expectation_checker.check(analysis)

        # Record features
        if analysis.has_search:
            self.coverage.record_feature("search_present")
        if analysis.has_pagination:
            self.coverage.record_feature("pagination_present")
        if analysis.has_filters:
            self.coverage.record_feature("filters_present")
        if analysis.repeated_structures:
            self.coverage.record_feature("repeated_content")
        if analysis.archetype != PageArchetype.UNKNOWN:
            self.coverage.record_feature(f"archetype_{analysis.archetype.value}")

        # Build advice
        advice = PlannerAdvice(content_expectations=exp_result)
        is_saturated = self.registry.is_saturated(analysis.structural_signature)
        advice.is_archetype_saturated = is_saturated

        # Detect flow template opportunities and generate priority overrides
        self._apply_flow_templates(analysis, advice, graph)

        # If archetype is saturated, suggest deprioritizing all same-type clicks
        if is_saturated:
            advice.priority_overrides["__saturated__"] = 90

        # Suggest contextual search values
        if analysis.has_search and self.context_store.has_entities:
            query = self.context_store.get_search_query()
            if query and query != "test query":
                advice.suggested_input_values["__search__"] = query

        return advice

    def _apply_flow_templates(
        self,
        analysis: PageAnalysis,
        advice: PlannerAdvice,
        graph: ExplorationGraph,
    ) -> None:
        """Detect flow template opportunities and set priority overrides."""
        templates: list[str] = []

        if analysis.archetype == PageArchetype.LISTING:
            # Browse-to-detail: boost content item clicks
            if FlowTemplate.BROWSE.value not in self._flow_features_detected:
                templates.append(FlowTemplate.BROWSE.value)
                # Content items get high priority
                advice.priority_overrides["__content_items__"] = 5

            # Search: if search is available and not yet tested
            if (
                analysis.has_search
                and FlowTemplate.SEARCH.value not in self._flow_features_detected
            ):
                templates.append(FlowTemplate.SEARCH.value)
                advice.priority_overrides["__search_action__"] = 3

            # Pagination
            if (
                analysis.has_pagination
                and FlowTemplate.PAGINATION.value not in self._flow_features_detected
            ):
                templates.append(FlowTemplate.PAGINATION.value)

            # Filter
            if (
                analysis.has_filters
                and FlowTemplate.FILTER_VERIFY.value not in self._flow_features_detected
            ):
                templates.append(FlowTemplate.FILTER_VERIFY.value)

        elif analysis.archetype == PageArchetype.DETAIL:
            if FlowTemplate.DETAIL_VERIFY.value not in self._flow_features_detected:
                templates.append(FlowTemplate.DETAIL_VERIFY.value)
                self.coverage.record_feature("detail_visited")

        elif analysis.archetype == PageArchetype.SEARCH_RESULTS:
            self.coverage.record_feature("search_executed")
            self._flow_features_detected.add(FlowTemplate.SEARCH.value)

        elif analysis.archetype == PageArchetype.FORM:
            if FlowTemplate.CRUD.value not in self._flow_features_detected:
                templates.append(FlowTemplate.CRUD.value)

        for t in templates:
            self.coverage.record_flow_template(t)

        advice.active_flow_templates = templates

    def get_analysis(self, state_id: str) -> PageAnalysis | None:
        """Retrieve the analysis for a given state."""
        return self._analyses.get(state_id)

    def get_all_catalogs(self) -> dict[str, Any]:
        """Return all page catalogs keyed by structural signature."""
        catalogs: dict[str, Any] = {}
        for analysis in self._analyses.values():
            sig = analysis.structural_signature
            if sig and sig not in catalogs:
                catalogs[sig] = analysis.catalog.model_dump()
        return catalogs

    def get_all_analyses(self) -> dict[str, Any]:
        """Return all analyses as serializable dicts, keyed by state_id."""
        return {sid: a.model_dump() for sid, a in self._analyses.items()}

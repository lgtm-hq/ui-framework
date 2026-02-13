"""Scenario synthesis — generates meaningful test scenarios from a site model."""

from __future__ import annotations

from collections import defaultdict

from pydantic import BaseModel, Field

from flowscout.core.action_types import ActionType
from flowscout.modeling.archetype import PageArchetype, ZoneType
from flowscout.modeling.site_model import NavigationEdge, PageType

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ScenarioStep(BaseModel):
    """A single step in a synthesized test scenario."""

    page_type: str
    action_description: str
    action_type: ActionType | None = None
    target_selector: str = ""
    expected_outcome: str = ""
    input_value: str = ""


class FlowScenario(BaseModel):
    """A synthesized test scenario from the navigation map."""

    scenario_id: str
    name: str
    description: str
    page_type_sequence: list[str] = Field(default_factory=list)
    steps: list[ScenarioStep] = Field(default_factory=list)
    priority: str = "important"
    template: str = ""
    tags: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Synthesizer
# ---------------------------------------------------------------------------


class ScenarioSynthesizer:
    """Generates test scenarios from page types and navigation edges."""

    def synthesize(
        self,
        page_types: list[PageType],
        nav_edges: list[NavigationEdge],
    ) -> list[FlowScenario]:
        scenarios: list[FlowScenario] = []
        counter = 0

        pt_by_id = {pt.page_type_id: pt for pt in page_types}
        edges_from: dict[str, list[NavigationEdge]] = defaultdict(list)
        for edge in nav_edges:
            edges_from[edge.from_page_type].append(edge)

        for pt in page_types:
            # 1. Load & Verify for every page type
            counter += 1
            scenarios.append(self._load_and_verify(pt, counter))

            # 2. LISTING → DETAIL: Browse & View Detail
            if pt.archetype == PageArchetype.LISTING:
                detail_edges = [
                    e
                    for e in edges_from.get(pt.page_type_id, [])
                    if pt_by_id.get(e.to_page_type, _EMPTY_PT).archetype
                    == PageArchetype.DETAIL
                ]
                if detail_edges:
                    counter += 1
                    detail_pt = pt_by_id[detail_edges[0].to_page_type]
                    scenarios.append(
                        self._browse_and_view(pt, detail_pt, detail_edges[0], counter)
                    )

            # 3. Search flow
            if "has_search" in pt.features:
                counter += 1
                scenarios.append(self._search_flow(pt, counter))

            # 4. Pagination flow
            if "has_pagination" in pt.features:
                counter += 1
                scenarios.append(self._pagination_flow(pt, counter))

            # 5. Filter flow
            if "has_filters" in pt.features:
                counter += 1
                scenarios.append(self._filter_flow(pt, counter))

            # 6. Form submission
            if pt.archetype == PageArchetype.FORM:
                counter += 1
                scenarios.append(self._form_submit(pt, counter))

        # 7. Round-trip verification for cycles
        seen_round_trips: set[tuple[str, str]] = set()
        for pt in page_types:
            for edge in edges_from.get(pt.page_type_id, []):
                return_edges = [
                    e
                    for e in edges_from.get(edge.to_page_type, [])
                    if e.to_page_type == pt.page_type_id
                ]
                if return_edges:
                    a, b = sorted([pt.page_type_id, edge.to_page_type])
                    pair = (a, b)
                    if pair not in seen_round_trips:
                        seen_round_trips.add(pair)
                        counter += 1
                        target_pt = pt_by_id.get(edge.to_page_type, _EMPTY_PT)
                        scenarios.append(
                            self._round_trip(
                                pt, target_pt, edge, return_edges[0], counter
                            )
                        )

        return scenarios

    # -- Template methods ----------------------------------------------------

    def _load_and_verify(self, pt: PageType, idx: int) -> FlowScenario:
        steps = [
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description=f"Navigate to {pt.name}",
                action_type=ActionType.NAVIGATE,
                target_selector="",
                expected_outcome="Page loads successfully with expected content",
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Verify page content is visible",
                action_type=None,
                expected_outcome=(
                    f"Content matches {pt.archetype.value} archetype expectations"
                ),
            ),
        ]

        return FlowScenario(
            scenario_id=f"scenario-{idx}",
            name=f"Load and verify {pt.name}",
            description=(
                f"Navigate to {pt.name} and verify the page content loads correctly."
            ),
            page_type_sequence=[pt.page_type_id],
            steps=steps,
            priority="important",
            template="load_verify",
            tags=["smoke", pt.archetype.value],
        )

    def _browse_and_view(
        self,
        listing_pt: PageType,
        detail_pt: PageType,
        edge: NavigationEdge,
        idx: int,
    ) -> FlowScenario:
        # Find a content item selector from the listing catalog
        item_selector = _find_content_item_selector(listing_pt)

        steps = [
            ScenarioStep(
                page_type=listing_pt.page_type_id,
                action_description=f"Navigate to {listing_pt.name}",
                action_type=ActionType.NAVIGATE,
            ),
            ScenarioStep(
                page_type=listing_pt.page_type_id,
                action_description="Verify listing content is displayed",
                expected_outcome="Listing items are visible",
            ),
            ScenarioStep(
                page_type=listing_pt.page_type_id,
                action_description=f"Click an item to view details ({edge.trigger})",
                action_type=ActionType.CLICK,
                target_selector=item_selector,
                expected_outcome="Navigation to detail page",
            ),
            ScenarioStep(
                page_type=detail_pt.page_type_id,
                action_description=f"Verify {detail_pt.name} content",
                expected_outcome="Detail content is visible (heading, text, images)",
            ),
        ]

        return FlowScenario(
            scenario_id=f"scenario-{idx}",
            name=f"Browse {listing_pt.name} and view detail",
            description=(
                f"Navigate to {listing_pt.name}, click an item, "
                f"and verify {detail_pt.name} loads with full content."
            ),
            page_type_sequence=[listing_pt.page_type_id, detail_pt.page_type_id],
            steps=steps,
            priority="critical",
            template="browse_detail",
            tags=["browse", "navigation", "critical-path"],
        )

    def _search_flow(self, pt: PageType, idx: int) -> FlowScenario:
        search_selector = _find_search_selector(pt)

        steps = [
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description=f"Navigate to {pt.name}",
                action_type=ActionType.NAVIGATE,
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Enter search query",
                action_type=ActionType.FILL,
                target_selector=search_selector,
                input_value="test search query",
                expected_outcome="Search results update",
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Verify search results are displayed",
                expected_outcome="Matching results are visible",
            ),
        ]

        return FlowScenario(
            scenario_id=f"scenario-{idx}",
            name=f"Search on {pt.name}",
            description=f"Navigate to {pt.name}, perform a search, and verify results.",
            page_type_sequence=[pt.page_type_id],
            steps=steps,
            priority="critical",
            template="search",
            tags=["search", "input"],
        )

    def _pagination_flow(self, pt: PageType, idx: int) -> FlowScenario:
        pagination_selector = _find_pagination_selector(pt)

        steps = [
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description=f"Navigate to {pt.name}",
                action_type=ActionType.NAVIGATE,
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Note current page content",
                expected_outcome="Initial content visible",
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Click next page / pagination control",
                action_type=ActionType.CLICK,
                target_selector=pagination_selector,
                expected_outcome="Content changes to next page",
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Verify content has changed",
                expected_outcome="Different content is displayed",
            ),
        ]

        return FlowScenario(
            scenario_id=f"scenario-{idx}",
            name=f"Paginate {pt.name}",
            description=f"Navigate to {pt.name} and verify pagination works.",
            page_type_sequence=[pt.page_type_id],
            steps=steps,
            priority="important",
            template="pagination",
            tags=["pagination", "navigation"],
        )

    def _filter_flow(self, pt: PageType, idx: int) -> FlowScenario:
        filter_selector = _find_filter_selector(pt)

        steps = [
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description=f"Navigate to {pt.name}",
                action_type=ActionType.NAVIGATE,
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Note current content",
                expected_outcome="Initial content visible",
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Apply a filter",
                action_type=ActionType.CLICK,
                target_selector=filter_selector,
                expected_outcome="Content filters to match selection",
            ),
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Verify filtered content",
                expected_outcome="Only matching items are displayed",
            ),
        ]

        return FlowScenario(
            scenario_id=f"scenario-{idx}",
            name=f"Filter {pt.name}",
            description=f"Navigate to {pt.name}, apply a filter, and verify results.",
            page_type_sequence=[pt.page_type_id],
            steps=steps,
            priority="important",
            template="filter",
            tags=["filter", "interaction"],
        )

    def _form_submit(self, pt: PageType, idx: int) -> FlowScenario:
        form_selectors = _find_form_selectors(pt)

        steps = [
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description=f"Navigate to {pt.name}",
                action_type=ActionType.NAVIGATE,
            ),
        ]

        # Add a fill step for each form field
        for selector, label in form_selectors:
            steps.append(
                ScenarioStep(
                    page_type=pt.page_type_id,
                    action_description=f"Fill {label}",
                    action_type=ActionType.FILL,
                    target_selector=selector,
                    input_value=f"test {label}",
                )
            )

        steps.append(
            ScenarioStep(
                page_type=pt.page_type_id,
                action_description="Submit the form",
                action_type=ActionType.SUBMIT_FORM,
                expected_outcome="Form submits successfully",
            )
        )

        return FlowScenario(
            scenario_id=f"scenario-{idx}",
            name=f"Submit {pt.name}",
            description=f"Navigate to {pt.name}, fill out the form, and submit.",
            page_type_sequence=[pt.page_type_id],
            steps=steps,
            priority="critical",
            template="form_submit",
            tags=["form", "submission"],
        )

    def _round_trip(
        self,
        pt_a: PageType,
        pt_b: PageType,
        edge_ab: NavigationEdge,
        edge_ba: NavigationEdge,
        idx: int,
    ) -> FlowScenario:
        steps = [
            ScenarioStep(
                page_type=pt_a.page_type_id,
                action_description=f"Navigate to {pt_a.name}",
                action_type=ActionType.NAVIGATE,
            ),
            ScenarioStep(
                page_type=pt_a.page_type_id,
                action_description=f"Go to {pt_b.name} ({edge_ab.trigger})",
                action_type=ActionType.CLICK,
                expected_outcome=f"Navigate to {pt_b.name}",
            ),
            ScenarioStep(
                page_type=pt_b.page_type_id,
                action_description=f"Return to {pt_a.name} ({edge_ba.trigger})",
                action_type=ActionType.CLICK,
                expected_outcome=f"Navigate back to {pt_a.name}",
            ),
            ScenarioStep(
                page_type=pt_a.page_type_id,
                action_description=f"Verify {pt_a.name} state is preserved",
                expected_outcome="Page content matches initial state",
            ),
        ]

        return FlowScenario(
            scenario_id=f"scenario-{idx}",
            name=f"Round trip: {pt_a.name} ↔ {pt_b.name}",
            description=(
                f"Navigate {pt_a.name} → {pt_b.name} → {pt_a.name} "
                f"and verify state is preserved."
            ),
            page_type_sequence=[
                pt_a.page_type_id,
                pt_b.page_type_id,
                pt_a.page_type_id,
            ],
            steps=steps,
            priority="nice-to-have",
            template="round_trip",
            tags=["navigation", "round-trip"],
        )


# ---------------------------------------------------------------------------
# Catalog helpers — extract selectors from PageCatalog
# ---------------------------------------------------------------------------


def _find_content_item_selector(pt: PageType) -> str:
    """Find a content item selector from a listing page's catalog."""
    for entry in pt.catalog.entries:
        if entry.zone_type == ZoneType.MAIN_CONTENT and entry.element_type in (
            "link",
            "button",
            "other",
        ):
            return str(entry.selector)
    return ""


def _find_search_selector(pt: PageType) -> str:
    """Find a search input selector from a page's catalog."""
    for entry in pt.catalog.entries:
        if entry.zone_type == ZoneType.SEARCH and "input" in entry.element_type:
            return str(entry.selector)
    # Fallback: any input with search-like attributes
    for entry in pt.catalog.entries:
        if entry.input_type == "search" or "search" in entry.semantic_name.lower():
            return str(entry.selector)
    return ""


def _find_pagination_selector(pt: PageType) -> str:
    """Find a pagination control selector."""
    for entry in pt.catalog.entries:
        if entry.zone_type == ZoneType.PAGINATION:
            return str(entry.selector)
    return ""


def _find_filter_selector(pt: PageType) -> str:
    """Find a filter control selector."""
    for entry in pt.catalog.entries:
        if entry.zone_type == ZoneType.FILTER:
            return str(entry.selector)
    return ""


def _find_form_selectors(pt: PageType) -> list[tuple[str, str]]:
    """Find form input selectors and their labels."""
    results: list[tuple[str, str]] = []
    for entry in pt.catalog.entries:
        if entry.zone_type == ZoneType.FORM and "input" in entry.element_type:
            label = entry.semantic_name or entry.label or entry.tag
            results.append((entry.selector, label))
    # Also check main content for form inputs
    if not results:
        for entry in pt.catalog.entries:
            if "input" in entry.element_type:
                label = entry.semantic_name or entry.label or entry.tag
                results.append((entry.selector, label))
    return results


# Sentinel for lookups
_EMPTY_PT = PageType(
    page_type_id="",
    name="",
    archetype=PageArchetype.UNKNOWN,
    structural_signature="",
)

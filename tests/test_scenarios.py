"""Tests for scenario synthesis."""

from flowscout.core.archetypes import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)
from flowscout.modeling.site_model import NavigationEdge, PageType
from flowscout.discovery.actions import ActionType, OutcomeType
from flowscout.modeling.scenarios import ScenarioSynthesizer

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_page_type(
    page_type_id: str = "pt_a",
    name: str = "Movie Listing",
    archetype: PageArchetype = PageArchetype.LISTING,
    features: set[str] | None = None,
    catalog_entries: list[CatalogEntry] | None = None,
) -> PageType:
    entries = catalog_entries or [
        CatalogEntry(
            selector="a.movie-card",
            tag="a",
            label="Movie card",
            zone_type=ZoneType.MAIN_CONTENT,
            element_type="link",
            semantic_name="movie_card",
        ),
    ]
    return PageType(
        page_type_id=page_type_id,
        name=name,
        archetype=archetype,
        url_pattern="https://example.com/movies",
        structural_signature=page_type_id,
        instance_count=3,
        representative_url="https://example.com/movies",
        catalog=PageCatalog(
            archetype=archetype,
            url_pattern="",
            entries=entries,
        ),
        features=features or set(),
    )


def _make_edge(
    from_pt: str,
    to_pt: str,
    trigger: str = "Click item",
    action_type: ActionType = ActionType.CLICK,
) -> NavigationEdge:
    return NavigationEdge(
        from_page_type=from_pt,
        to_page_type=to_pt,
        trigger=trigger,
        action_type=action_type,
        outcome=OutcomeType.NAVIGATION,
        occurrence_count=5,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class FlowScenarioSynthesizer:
    def test_empty_input_returns_empty(self) -> None:
        synth = ScenarioSynthesizer()
        result = synth.synthesize([], [])
        assert result == []

    def test_every_page_type_gets_load_verify(self) -> None:
        pt = _make_page_type()
        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([pt], [])

        load_scenarios = [s for s in scenarios if s.template == "load_verify"]
        assert len(load_scenarios) == 1
        assert "Load" in load_scenarios[0].name

    def test_listing_with_detail_edge_generates_browse_scenario(self) -> None:
        listing = _make_page_type("pt_listing", "Movies", PageArchetype.LISTING)
        detail = _make_page_type("pt_detail", "Movie Detail", PageArchetype.DETAIL)
        edge = _make_edge("pt_listing", "pt_detail")

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([listing, detail], [edge])

        browse = [s for s in scenarios if s.template == "browse_detail"]
        assert len(browse) == 1
        assert browse[0].priority == "critical"
        assert "pt_listing" in browse[0].page_type_sequence
        assert "pt_detail" in browse[0].page_type_sequence

    def test_search_feature_generates_search_scenario(self) -> None:
        pt = _make_page_type(
            features={"has_search"},
            catalog_entries=[
                CatalogEntry(
                    selector="input[type='search']",
                    tag="input",
                    label="Search",
                    zone_type=ZoneType.SEARCH,
                    element_type="input_search",
                    semantic_name="search_input",
                    input_type="search",
                ),
            ],
        )

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([pt], [])

        search = [s for s in scenarios if s.template == "search"]
        assert len(search) == 1
        assert search[0].priority == "critical"

    def test_pagination_generates_pagination_scenario(self) -> None:
        pt = _make_page_type(features={"has_pagination"})

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([pt], [])

        pagination = [s for s in scenarios if s.template == "pagination"]
        assert len(pagination) == 1
        assert pagination[0].priority == "important"

    def test_filter_generates_filter_scenario(self) -> None:
        pt = _make_page_type(features={"has_filters"})

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([pt], [])

        filters = [s for s in scenarios if s.template == "filter"]
        assert len(filters) == 1

    def test_form_generates_submit_scenario(self) -> None:
        pt = _make_page_type(
            name="Contact Form",
            archetype=PageArchetype.FORM,
            catalog_entries=[
                CatalogEntry(
                    selector="input[name='email']",
                    tag="input",
                    label="Email",
                    zone_type=ZoneType.FORM,
                    element_type="input_email",
                    semantic_name="email",
                    input_type="email",
                ),
            ],
        )

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([pt], [])

        form = [s for s in scenarios if s.template == "form_submit"]
        assert len(form) == 1
        assert form[0].priority == "critical"

    def test_round_trip_detection(self) -> None:
        pt_a = _make_page_type("pt_a", "Listing", PageArchetype.LISTING)
        pt_b = _make_page_type("pt_b", "Detail", PageArchetype.DETAIL)
        edge_ab = _make_edge("pt_a", "pt_b", "Click item")
        edge_ba = _make_edge("pt_b", "pt_a", "Back to listing")

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([pt_a, pt_b], [edge_ab, edge_ba])

        round_trips = [s for s in scenarios if s.template == "round_trip"]
        assert len(round_trips) == 1
        assert round_trips[0].priority == "nice-to-have"

    def test_scenario_ids_unique(self) -> None:
        pt = _make_page_type(features={"has_search", "has_pagination", "has_filters"})

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([pt], [])

        ids = [s.scenario_id for s in scenarios]
        assert len(ids) == len(set(ids))

    def test_tags_applied_correctly(self) -> None:
        pt = _make_page_type(features={"has_search"})

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([pt], [])

        search = next(s for s in scenarios if s.template == "search")
        assert "search" in search.tags

"""Tests for shared component extraction."""

from flowscout.core.archetypes import CatalogEntry, PageArchetype, PageCatalog, ZoneType
from flowscout.modeling.components import InteractionPattern, extract_shared_components


def _catalog(entries: list[CatalogEntry]) -> PageCatalog:
    return PageCatalog(
        archetype=PageArchetype.LISTING,
        url_pattern="/movies",
        entries=entries,
    )


def test_extracts_navigation_component_when_present_on_all_pages() -> None:
    nav_entry = CatalogEntry(
        selector="a[href='/home']",
        tag="a",
        label="Home",
        zone_type=ZoneType.NAVIGATION,
        element_type="link",
        semantic_name="home",
    )
    page_catalogs = {
        "listing_sig": _catalog(
            [
                nav_entry,
                CatalogEntry(
                    selector=".movie-card",
                    tag="div",
                    label="Movie card",
                    zone_type=ZoneType.MAIN_CONTENT,
                    element_type="other",
                    semantic_name="movie_card",
                ),
            ]
        ),
        "detail_sig": _catalog(
            [
                nav_entry,
                CatalogEntry(
                    selector="h1.movie-title",
                    tag="h1",
                    label="Movie title",
                    zone_type=ZoneType.MAIN_CONTENT,
                    element_type="heading",
                    semantic_name="movie_title",
                ),
            ]
        ),
        "search_sig": _catalog(
            [
                nav_entry,
                CatalogEntry(
                    selector="input[type='search']",
                    tag="input",
                    label="Search",
                    zone_type=ZoneType.SEARCH,
                    element_type="input_search",
                    semantic_name="search",
                ),
            ]
        ),
    }

    components = extract_shared_components(
        page_catalogs=page_catalogs, min_frequency=0.6
    )

    assert components
    navigation = next(c for c in components if c.zone == ZoneType.NAVIGATION)
    assert navigation.class_name == "NavigationComponent"
    assert navigation.appears_on == ["detail_sig", "listing_sig", "search_sig"]
    assert navigation.frequency == 1.0
    assert any(entry.selector == "a[href='/home']" for entry in navigation.entries)


def test_does_not_extract_component_below_frequency_threshold() -> None:
    nav_entry = CatalogEntry(
        selector="a[href='/home']",
        tag="a",
        label="Home",
        zone_type=ZoneType.NAVIGATION,
        element_type="link",
        semantic_name="home",
    )
    page_catalogs = {
        "listing_sig": _catalog([nav_entry]),
        "detail_sig": _catalog(
            [
                CatalogEntry(
                    selector="h1.movie-title",
                    tag="h1",
                    label="Movie title",
                    zone_type=ZoneType.MAIN_CONTENT,
                    element_type="heading",
                    semantic_name="movie_title",
                )
            ]
        ),
        "search_sig": _catalog(
            [
                CatalogEntry(
                    selector="input[type='search']",
                    tag="input",
                    label="Search",
                    zone_type=ZoneType.SEARCH,
                    element_type="input_search",
                    semantic_name="search",
                )
            ]
        ),
    }

    components = extract_shared_components(
        page_catalogs=page_catalogs, min_frequency=0.6
    )

    assert components == []


def test_detects_dropdown_pattern_on_shared_component() -> None:
    page_catalogs = {
        "listing_sig": _catalog(
            [
                CatalogEntry(
                    selector="button[aria-haspopup='listbox']",
                    tag="button",
                    label="Theme",
                    zone_type=ZoneType.HEADER,
                    element_type="dropdown_trigger",
                    semantic_name="theme_trigger",
                ),
                CatalogEntry(
                    selector="[role='option']",
                    tag="div",
                    label="Dark",
                    zone_type=ZoneType.HEADER,
                    element_type="dropdown_option",
                    aria_role="option",
                    semantic_name="theme_option",
                ),
            ]
        ),
        "detail_sig": _catalog(
            [
                CatalogEntry(
                    selector="button[aria-haspopup='listbox']",
                    tag="button",
                    label="Theme",
                    zone_type=ZoneType.HEADER,
                    element_type="dropdown_trigger",
                    semantic_name="theme_trigger",
                ),
                CatalogEntry(
                    selector="[role='option']",
                    tag="div",
                    label="Dark",
                    zone_type=ZoneType.HEADER,
                    element_type="dropdown_option",
                    aria_role="option",
                    semantic_name="theme_option",
                ),
            ]
        ),
    }

    components = extract_shared_components(
        page_catalogs=page_catalogs, min_frequency=0.6
    )

    assert components
    header_component = next(c for c in components if c.zone == ZoneType.HEADER)
    assert InteractionPattern.DROPDOWN in header_component.interaction_patterns


def test_detects_search_pattern_on_shared_component() -> None:
    search_entry = CatalogEntry(
        selector="input[type='search']",
        tag="input",
        label="Search",
        zone_type=ZoneType.SEARCH,
        element_type="input_search",
        semantic_name="search_input",
    )
    page_catalogs = {
        "listing_sig": _catalog([search_entry]),
        "detail_sig": _catalog([search_entry]),
    }

    components = extract_shared_components(
        page_catalogs=page_catalogs, min_frequency=0.6
    )

    assert components
    search_component = next(c for c in components if c.zone == ZoneType.SEARCH)
    assert InteractionPattern.SEARCH in search_component.interaction_patterns

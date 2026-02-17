"""Tests for shared codegen primitives."""

from __future__ import annotations

from flowscout.codegen.primitives import (
    ZONE_LABELS,
    build_entry_property_names,
    catalog_to_class_name,
    entry_locator,
    group_by_zone,
    selector_to_property_name,
    to_kebab_case,
    to_snake_case,
)
from flowscout.core.archetypes import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)


class TestToSnakeCase:
    def test_pascal_case(self) -> None:
        assert to_snake_case("HomePage") == "home_page"

    def test_single_word(self) -> None:
        assert to_snake_case("Page") == "page"

    def test_multi_word(self) -> None:
        assert to_snake_case("NavigationComponent") == "navigation_component"


class TestToKebabCase:
    def test_pascal_case(self) -> None:
        assert to_kebab_case("HomePage") == "home-page"

    def test_single_word(self) -> None:
        assert to_kebab_case("Page") == "page"


class TestCatalogToClassName:
    def test_listing_archetype(self) -> None:
        catalog = PageCatalog(archetype=PageArchetype.LISTING)
        assert "Listing" in catalog_to_class_name(catalog)
        assert "Page" in catalog_to_class_name(catalog)

    def test_with_url_pattern(self) -> None:
        catalog = PageCatalog(
            archetype=PageArchetype.DETAIL,
            url_pattern="/movies/1",
        )
        name = catalog_to_class_name(catalog)
        assert "Detail" in name

    def test_pascal_case_output(self) -> None:
        catalog = PageCatalog(archetype=PageArchetype.LISTING)
        name = catalog_to_class_name(catalog)
        assert name[0].isupper()
        assert "_" not in name


class TestSelectorToPropertyName:
    def test_from_label(self) -> None:
        assert selector_to_property_name("a", "Home", "a") == "home"

    def test_from_aria_label(self) -> None:
        name = selector_to_property_name("[aria-label='Search']", "", "button")
        assert name == "search"

    def test_from_id(self) -> None:
        name = selector_to_property_name("#main-nav", "", "nav")
        assert name == "main_nav"

    def test_fallback_to_tag(self) -> None:
        name = selector_to_property_name("div:nth-of-type(3)", "", "div")
        assert name.startswith("div")

    def test_max_length(self) -> None:
        name = selector_to_property_name("div", "A" * 50, "div")
        assert len(name) <= 40

    def test_cleans_special_chars(self) -> None:
        name = selector_to_property_name("div", "Click Here!", "div")
        assert "!" not in name


class TestEntryLocator:
    def test_preferred_selector(self) -> None:
        entry = CatalogEntry(
            selector="div.fallback",
            preferred_selector="[data-testid='main']",
            tag="div",
            label="Main",
            zone_type=ZoneType.MAIN_CONTENT,
            element_type="other",
        )
        assert entry_locator(entry) == "[data-testid='main']"

    def test_default_selector(self) -> None:
        entry = CatalogEntry(
            selector="div.fallback",
            tag="div",
            label="Main",
            zone_type=ZoneType.MAIN_CONTENT,
            element_type="other",
        )
        assert entry_locator(entry) == "div.fallback"


class TestGroupByZone:
    def test_groups_entries(self) -> None:
        entries = [
            CatalogEntry(
                selector="a",
                tag="a",
                label="Link",
                zone_type=ZoneType.NAVIGATION,
                element_type="link",
            ),
            CatalogEntry(
                selector="input",
                tag="input",
                label="Search",
                zone_type=ZoneType.SEARCH,
                element_type="input_search",
            ),
        ]
        grouped = group_by_zone(entries)
        assert ZoneType.NAVIGATION in grouped
        assert ZoneType.SEARCH in grouped
        assert len(grouped[ZoneType.NAVIGATION]) == 1


class TestBuildEntryPropertyNames:
    def test_builds_mapping(self) -> None:
        entries = [
            CatalogEntry(
                selector="a[href='/']",
                tag="a",
                label="Home",
                zone_type=ZoneType.NAVIGATION,
                element_type="link",
                semantic_name="home",
            ),
        ]
        names = build_entry_property_names(entries)
        assert names["a[href='/']"] == "home"

    def test_deduplicates(self) -> None:
        entries = [
            CatalogEntry(
                selector="a.link1",
                tag="a",
                label="Link",
                zone_type=ZoneType.NAVIGATION,
                element_type="link",
                semantic_name="link",
            ),
            CatalogEntry(
                selector="a.link2",
                tag="a",
                label="Link",
                zone_type=ZoneType.NAVIGATION,
                element_type="link",
                semantic_name="link",
            ),
        ]
        names = build_entry_property_names(entries)
        assert names["a.link1"] == "link"
        assert names["a.link2"] == "link_2"


class TestZoneLabels:
    def test_all_zones_have_labels(self) -> None:
        for zone_type in ZoneType:
            assert zone_type in ZONE_LABELS

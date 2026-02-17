"""Tests for the POM builder."""

from __future__ import annotations

from conftest import make_catalog

from flowscout.codegen.pom_builder import build_pom_suite, build_pom_suite_for_preview
from flowscout.codegen.pom_model import MethodKind, PropertyKind
from flowscout.core.archetypes import (
    CatalogEntry,
    PageArchetype,
    ZoneType,
)
from flowscout.modeling.components import InteractionPattern, SharedComponent


class TestBuildPomSuite:
    def test_empty_catalogs_returns_empty_suite(self) -> None:
        suite = build_pom_suite({})
        assert suite.pages == []
        assert suite.components == []

    def test_single_catalog_produces_one_page(self) -> None:
        catalog = make_catalog(url_pattern="/movies")
        suite = build_pom_suite(
            {"sig1": catalog.model_dump()},
            base_url="https://example.com",
        )
        assert len(suite.pages) == 1
        assert suite.pages[0].class_name.endswith("Page")

    def test_base_page_has_navigate_method(self) -> None:
        catalog = make_catalog()
        suite = build_pom_suite({"sig1": catalog.model_dump()})
        navigate_methods = [
            m for m in suite.base_page.methods if m.kind == MethodKind.NAVIGATE
        ]
        assert len(navigate_methods) == 1

    def test_page_has_locator_properties(self) -> None:
        catalog = make_catalog()
        suite = build_pom_suite(
            {"sig1": catalog.model_dump()},
            base_url="https://example.com",
        )
        locator_props = [
            p for p in suite.pages[0].properties if p.kind == PropertyKind.LOCATOR
        ]
        assert len(locator_props) == 3

    def test_page_inherits_base_page(self) -> None:
        catalog = make_catalog()
        suite = build_pom_suite({"sig1": catalog.model_dump()})
        assert suite.pages[0].parent_class == "BasePage"

    def test_search_method_generated(self) -> None:
        catalog = make_catalog()
        suite = build_pom_suite(
            {"sig1": catalog.model_dump()},
            base_url="https://example.com",
        )
        search_methods = [
            m for m in suite.pages[0].methods if m.kind == MethodKind.SEARCH
        ]
        assert len(search_methods) == 1

    def test_listing_has_select_item(self) -> None:
        entries = [
            CatalogEntry(
                selector=".card",
                tag="div",
                label="Card",
                zone_type=ZoneType.MAIN_CONTENT,
                element_type="link",
                semantic_name="card",
            ),
        ]
        catalog = make_catalog(
            PageArchetype.LISTING,
            entries=entries,
            url_pattern="/items",
        )
        suite = build_pom_suite(
            {"sig1": catalog.model_dump()},
            base_url="https://example.com",
        )
        select_methods = [
            m for m in suite.pages[0].methods if m.kind == MethodKind.SELECT_ITEM
        ]
        assert len(select_methods) == 1


class TestComponentPartitioning:
    def test_high_frequency_goes_to_base(self) -> None:
        catalog = make_catalog(url_pattern="/movies")
        nav = SharedComponent(
            component_id="nav",
            name="Nav",
            class_name="NavigationComponent",
            entries=[
                CatalogEntry(
                    selector="a[href='/']",
                    tag="a",
                    label="Home",
                    zone_type=ZoneType.NAVIGATION,
                    element_type="link",
                    semantic_name="home",
                ),
            ],
            appears_on=["sig1"],
            frequency=0.9,
            zone=ZoneType.NAVIGATION,
        )
        suite = build_pom_suite(
            {"sig1": catalog.model_dump()},
            shared_components=[nav.model_dump()],
        )
        base_component_props = [
            p for p in suite.base_page.properties if p.kind == PropertyKind.COMPONENT
        ]
        assert len(base_component_props) == 1
        assert base_component_props[0].component_class_name == "NavigationComponent"

    def test_low_frequency_goes_to_page(self) -> None:
        catalog = make_catalog(url_pattern="/movies")
        sidebar = SharedComponent(
            component_id="sidebar",
            name="Sidebar",
            class_name="SidebarComponent",
            entries=[
                CatalogEntry(
                    selector=".sidebar",
                    tag="aside",
                    label="Sidebar",
                    zone_type=ZoneType.SIDEBAR,
                    element_type="other",
                    semantic_name="sidebar",
                ),
            ],
            appears_on=["sig1"],
            frequency=0.5,
            zone=ZoneType.SIDEBAR,
        )
        suite = build_pom_suite(
            {"sig1": catalog.model_dump()},
            shared_components=[sidebar.model_dump()],
        )
        page_component_props = [
            p for p in suite.pages[0].properties if p.kind == PropertyKind.COMPONENT
        ]
        assert len(page_component_props) == 1

    def test_shared_entries_stripped_from_page(self) -> None:
        catalog = make_catalog(url_pattern="/movies")
        nav = SharedComponent(
            component_id="nav",
            name="Nav",
            class_name="NavigationComponent",
            entries=[
                CatalogEntry(
                    selector="a[href='/home']",
                    tag="a",
                    label="Home",
                    zone_type=ZoneType.NAVIGATION,
                    element_type="link",
                    semantic_name="home",
                ),
            ],
            appears_on=["sig1"],
            frequency=0.9,
            zone=ZoneType.NAVIGATION,
        )
        suite = build_pom_suite(
            {"sig1": catalog.model_dump()},
            shared_components=[nav.model_dump()],
        )
        page_locators = [
            p for p in suite.pages[0].properties if p.kind == PropertyKind.LOCATOR
        ]
        # "a[href='/home']" should be stripped, only search input remains
        selectors = [p.selector for p in page_locators]
        assert "a[href='/home']" not in selectors


class TestPatternMethods:
    def test_dropdown_pattern(self) -> None:
        component = SharedComponent(
            component_id="theme",
            name="ThemeDropdown",
            class_name="ThemeComponent",
            entries=[
                CatalogEntry(
                    selector="button.trigger",
                    tag="button",
                    label="Theme",
                    zone_type=ZoneType.HEADER,
                    element_type="dropdown_trigger",
                    semantic_name="trigger",
                ),
            ],
            appears_on=[],
            frequency=0.5,
            zone=ZoneType.HEADER,
            interaction_patterns=[InteractionPattern.DROPDOWN],
        )
        suite = build_pom_suite(
            {"sig1": make_catalog().model_dump()},
            shared_components=[component.model_dump()],
        )
        comp = suite.components[0]
        method_kinds = {m.kind for m in comp.methods}
        assert MethodKind.OPEN in method_kinds
        assert MethodKind.CLOSE in method_kinds
        assert MethodKind.SELECT_OPTION in method_kinds

    def test_tabs_pattern(self) -> None:
        component = SharedComponent(
            component_id="tabs",
            name="Tabs",
            class_name="TabsComponent",
            entries=[
                CatalogEntry(
                    selector="[role='tab']",
                    tag="button",
                    label="Tab",
                    zone_type=ZoneType.NAVIGATION,
                    element_type="tab",
                    semantic_name="tab",
                ),
            ],
            appears_on=[],
            frequency=0.5,
            zone=ZoneType.NAVIGATION,
            interaction_patterns=[InteractionPattern.TABS],
        )
        suite = build_pom_suite(
            {"sig1": make_catalog().model_dump()},
            shared_components=[component.model_dump()],
        )
        comp = suite.components[0]
        method_kinds = {m.kind for m in comp.methods}
        assert MethodKind.SWITCH_TAB in method_kinds


    def test_search_pattern(self) -> None:
        component = SharedComponent(
            component_id="search",
            name="SearchBar",
            class_name="SearchComponent",
            entries=[
                CatalogEntry(
                    selector="input[type='search']",
                    tag="input",
                    label="Search",
                    zone_type=ZoneType.SEARCH,
                    element_type="input_search",
                    semantic_name="search",
                ),
            ],
            appears_on=[],
            frequency=0.5,
            zone=ZoneType.SEARCH,
            interaction_patterns=[InteractionPattern.SEARCH],
        )
        suite = build_pom_suite(
            {"sig1": make_catalog().model_dump()},
            shared_components=[component.model_dump()],
        )
        comp = suite.components[0]
        method_kinds = {m.kind for m in comp.methods}
        assert MethodKind.SEARCH in method_kinds

    def test_form_pattern(self) -> None:
        component = SharedComponent(
            component_id="login",
            name="LoginForm",
            class_name="LoginFormComponent",
            entries=[
                CatalogEntry(
                    selector="input[name='email']",
                    tag="input",
                    label="Email",
                    zone_type=ZoneType.MAIN_CONTENT,
                    element_type="input_email",
                    semantic_name="email",
                ),
            ],
            appears_on=[],
            frequency=0.5,
            zone=ZoneType.MAIN_CONTENT,
            interaction_patterns=[InteractionPattern.FORM],
        )
        suite = build_pom_suite(
            {"sig1": make_catalog().model_dump()},
            shared_components=[component.model_dump()],
        )
        comp = suite.components[0]
        method_kinds = {m.kind for m in comp.methods}
        assert MethodKind.FILL_AND_SUBMIT in method_kinds

    def test_pagination_pattern(self) -> None:
        component = SharedComponent(
            component_id="pager",
            name="Pagination",
            class_name="PaginationComponent",
            entries=[
                CatalogEntry(
                    selector="a.next",
                    tag="a",
                    label="Next",
                    zone_type=ZoneType.FOOTER,
                    element_type="link",
                    semantic_name="next",
                ),
            ],
            appears_on=[],
            frequency=0.5,
            zone=ZoneType.FOOTER,
            interaction_patterns=[InteractionPattern.PAGINATION],
        )
        suite = build_pom_suite(
            {"sig1": make_catalog().model_dump()},
            shared_components=[component.model_dump()],
        )
        comp = suite.components[0]
        method_kinds = {m.kind for m in comp.methods}
        assert MethodKind.NEXT_PAGE in method_kinds
        assert MethodKind.PREVIOUS_PAGE in method_kinds

    def test_toggle_pattern(self) -> None:
        component = SharedComponent(
            component_id="toggle",
            name="SettingsToggle",
            class_name="ToggleComponent",
            entries=[
                CatalogEntry(
                    selector="input[type='checkbox']",
                    tag="input",
                    label="Enable",
                    zone_type=ZoneType.MAIN_CONTENT,
                    element_type="input_checkbox",
                    semantic_name="enable",
                ),
            ],
            appears_on=[],
            frequency=0.5,
            zone=ZoneType.MAIN_CONTENT,
            interaction_patterns=[InteractionPattern.TOGGLE],
        )
        suite = build_pom_suite(
            {"sig1": make_catalog().model_dump()},
            shared_components=[component.model_dump()],
        )
        comp = suite.components[0]
        method_kinds = {m.kind for m in comp.methods}
        assert MethodKind.TOGGLE in method_kinds
        assert MethodKind.IS_CHECKED in method_kinds


class TestBuildPomSuiteForPreview:
    def test_returns_pom_classes_by_page_type_id(self) -> None:
        catalog = make_catalog(url_pattern="/movies")
        result = build_pom_suite_for_preview(
            [{"page_type_id": "listing_1", "catalog": catalog.model_dump()}],
            base_url="https://example.com",
        )
        assert "listing_1" in result
        assert result["listing_1"].class_name.endswith("Page")

    def test_skips_empty_page_type_id(self) -> None:
        catalog = make_catalog()
        result = build_pom_suite_for_preview(
            [{"page_type_id": "", "catalog": catalog.model_dump()}],
        )
        assert result == {}

    def test_skips_empty_catalog(self) -> None:
        result = build_pom_suite_for_preview(
            [{"page_type_id": "empty", "catalog": {}}],
        )
        assert result == {}

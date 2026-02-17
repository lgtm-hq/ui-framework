"""Tests for POM rendering adapters."""

from __future__ import annotations

from flowscout.codegen.adapters import ADAPTERS, get_adapter
from flowscout.codegen.adapters.playwright_python import PlaywrightPythonAdapter
from flowscout.codegen.adapters.playwright_ts import PlaywrightTSAdapter
from flowscout.codegen.pom_model import (
    MethodKind,
    POMClass,
    POMMethod,
    POMProperty,
    PropertyKind,
)
from flowscout.modeling.archetype import PageArchetype, ZoneType

import pytest


def _make_page_class(
    *,
    base_url: str = "https://example.com",
    parent_class: str = "",
) -> POMClass:
    return POMClass(
        class_name="MoviesListingPage",
        parent_class=parent_class,
        archetype=PageArchetype.LISTING,
        url_pattern="/movies",
        base_url=base_url,
        properties=[
            POMProperty(
                name="home",
                selector="a[href='/home']",
                zone=ZoneType.NAVIGATION,
                zone_label="Navigation",
            ),
            POMProperty(
                name="search",
                selector="input[type='search']",
                zone=ZoneType.SEARCH,
                zone_label="Search",
                element_type="input_search",
            ),
        ],
        methods=[
            POMMethod(
                kind=MethodKind.NAVIGATE,
                name="navigate",
            ),
            POMMethod(
                kind=MethodKind.SEARCH,
                name="search",
                parameters=[("query", "str")],
                selector="input[type='search']",
            ),
        ],
    )


def _make_component_class() -> POMClass:
    return POMClass(
        class_name="NavigationComponent",
        is_component=True,
        component_name="NavigationBar",
        component_zone=ZoneType.NAVIGATION,
        properties=[
            POMProperty(
                name="home",
                selector="a[href='/']",
                element_type="link",
            ),
        ],
        methods=[
            POMMethod(
                kind=MethodKind.ASSERT_VISIBLE,
                name="assert_visible",
                target_property="home",
            ),
            POMMethod(
                kind=MethodKind.CLICK,
                name="click_home",
                target_property="home",
            ),
        ],
    )


def _make_base_page_class() -> POMClass:
    return POMClass(
        class_name="BasePage",
        properties=[
            POMProperty(
                name="navigation_component",
                selector="",
                kind=PropertyKind.COMPONENT,
                component_class_name="NavigationComponent",
            ),
        ],
        methods=[
            POMMethod(
                kind=MethodKind.NAVIGATE,
                name="navigate",
                parameters=[("path", "str")],
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TestAdapterRegistry:
    def test_pytest_returns_python_adapter(self) -> None:
        adapter = get_adapter("pytest")
        assert isinstance(adapter, PlaywrightPythonAdapter)

    def test_playwright_returns_ts_adapter(self) -> None:
        adapter = get_adapter("playwright")
        assert isinstance(adapter, PlaywrightTSAdapter)

    def test_unknown_framework_raises(self) -> None:
        with pytest.raises(KeyError, match="Unknown framework"):
            get_adapter("selenium")

    def test_registry_has_two_entries(self) -> None:
        assert len(ADAPTERS) == 2


# ---------------------------------------------------------------------------
# Python Adapter
# ---------------------------------------------------------------------------


class TestPlaywrightPythonAdapter:
    def setup_method(self) -> None:
        self.adapter = PlaywrightPythonAdapter()

    def test_file_extension(self) -> None:
        assert self.adapter.file_extension() == ".py"

    def test_base_page_filename(self) -> None:
        assert self.adapter.base_page_filename() == "base_page.py"

    def test_class_to_filename(self) -> None:
        assert self.adapter.class_to_filename("HomePage") == "home_page.py"

    def test_render_page_has_class_def(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "class MoviesListingPage:" in output

    def test_render_page_with_base(self) -> None:
        pom = _make_page_class(parent_class="BasePage")
        output = self.adapter.render_page(pom)
        assert "class MoviesListingPage(BasePage):" in output
        assert "super().__init__(page)" in output
        assert "super().navigate(self.URL)" in output

    def test_render_page_has_constructor(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "def __init__(self, page: Page)" in output

    def test_render_page_has_locators(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "page.locator(\"a[href='/home']\")" in output

    def test_render_page_has_zone_comments(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "# Navigation" in output
        assert "# Search" in output

    def test_render_page_has_navigate(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "def navigate(self)" in output

    def test_render_page_has_search(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "def search(self, query: str)" in output

    def test_render_page_no_navigate_without_url(self) -> None:
        pom = _make_page_class(base_url="")
        # Remove navigate method (builder wouldn't add it without base_url)
        non_nav = [m for m in pom.methods if m.kind != MethodKind.NAVIGATE]
        pom = pom.model_copy(update={"methods": non_nav})
        output = self.adapter.render_page(pom)
        assert "def navigate" not in output

    def test_render_component(self) -> None:
        comp = _make_component_class()
        output = self.adapter.render_component(comp)
        assert "class NavigationComponent:" in output
        assert "def assert_visible(self)" in output
        assert "def click_home(self)" in output

    def test_render_base_page(self) -> None:
        base = _make_base_page_class()
        output = self.adapter.render_base_page(base)
        assert "class BasePage:" in output
        assert "def navigate(self, path: str)" in output
        assert "self.navigation_component = NavigationComponent(page)" in output

    def test_render_component_has_fill_method(self) -> None:
        comp = POMClass(
            class_name="SearchComponent",
            is_component=True,
            component_name="Search",
            component_zone=ZoneType.SEARCH,
            properties=[
                POMProperty(
                    name="search_input",
                    selector="input[type='search']",
                    element_type="input_search",
                ),
            ],
            methods=[
                POMMethod(
                    kind=MethodKind.FILL,
                    name="fill_search_input",
                    parameters=[("value", "str")],
                    target_property="search_input",
                ),
            ],
        )
        output = self.adapter.render_component(comp)
        assert "def fill_search_input(self, value: str)" in output


# ---------------------------------------------------------------------------
# TypeScript Adapter
# ---------------------------------------------------------------------------


class TestPlaywrightTSAdapter:
    def setup_method(self) -> None:
        self.adapter = PlaywrightTSAdapter()

    def test_file_extension(self) -> None:
        assert self.adapter.file_extension() == ".ts"

    def test_base_page_filename(self) -> None:
        assert self.adapter.base_page_filename() == "base-page.ts"

    def test_class_to_filename(self) -> None:
        assert self.adapter.class_to_filename("HomePage") == "home-page.ts"

    def test_render_page_has_export_class(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "export class MoviesListingPage" in output

    def test_render_page_with_base(self) -> None:
        pom = _make_page_class(parent_class="BasePage")
        output = self.adapter.render_page(pom)
        assert "extends BasePage" in output
        assert "super(page);" in output

    def test_render_page_has_readonly_locators(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "readonly home: Locator;" in output

    def test_render_page_has_constructor(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "constructor(public readonly page: Page)" in output

    def test_render_page_has_async_navigate(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "async navigate()" in output

    def test_render_page_has_zone_comments(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "// Navigation" in output
        assert "// Search" in output

    def test_render_component(self) -> None:
        comp = _make_component_class()
        output = self.adapter.render_component(comp)
        assert "export class NavigationComponent" in output
        assert "async assertVisible()" in output
        assert "async clickHome()" in output

    def test_render_base_page(self) -> None:
        base = _make_base_page_class()
        output = self.adapter.render_base_page(base)
        assert "export class BasePage" in output
        assert "async navigate(path: string)" in output

    def test_render_page_has_async_search(self) -> None:
        pom = _make_page_class()
        output = self.adapter.render_page(pom)
        assert "async search(query: string)" in output

    def test_render_component_has_fill_method(self) -> None:
        comp = POMClass(
            class_name="SearchComponent",
            is_component=True,
            component_name="Search",
            component_zone=ZoneType.SEARCH,
            properties=[
                POMProperty(
                    name="search_input",
                    selector="input[type='search']",
                    element_type="input_search",
                ),
            ],
            methods=[
                POMMethod(
                    kind=MethodKind.FILL,
                    name="fill_search_input",
                    parameters=[("value", "str")],
                    target_property="search_input",
                ),
            ],
        )
        output = self.adapter.render_component(comp)
        assert "async fillSearchInput(value: string)" in output
        assert "await this.search_input.fill(value);" in output

    def test_render_base_page_with_components(self) -> None:
        base = _make_base_page_class()
        output = self.adapter.render_base_page(base)
        assert "export class BasePage" in output
        assert "async navigate(path: string)" in output
        assert "this.navigation_component = new NavigationComponent(page);" in output

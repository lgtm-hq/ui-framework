"""Tests for Page Object Model generation."""

from __future__ import annotations

import tempfile
from pathlib import Path


from flowscout.core.archetypes import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)
from flowscout.codegen.page_objects import (
    _catalog_to_class_name,
    _generate_python_pom,
    _generate_typescript_pom,
    _selector_to_property_name,
    generate_page_objects,
)
from flowscout.modeling.components import SharedComponent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_catalog(
    archetype: PageArchetype = PageArchetype.LISTING,
    entries: list[CatalogEntry] | None = None,
    url_pattern: str = "",
) -> PageCatalog:
    if entries is None:
        entries = [
            CatalogEntry(
                selector="a[href='/home']",
                tag="a",
                label="Home",
                zone_type=ZoneType.NAVIGATION,
                element_type="link",
                semantic_name="home",
            ),
            CatalogEntry(
                selector="input[type='search']",
                tag="input",
                label="Search",
                zone_type=ZoneType.SEARCH,
                element_type="input_search",
                input_type="search",
                semantic_name="search",
            ),
            CatalogEntry(
                selector=".movie-card",
                tag="div",
                label="Movie 1",
                zone_type=ZoneType.MAIN_CONTENT,
                element_type="other",
                semantic_name="movie_1",
            ),
        ]
    return PageCatalog(
        archetype=archetype,
        url_pattern=url_pattern,
        entries=entries,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestClassNameGeneration:
    """Class name generation from catalogs."""

    def test_listing_archetype(self) -> None:
        catalog = _make_catalog(PageArchetype.LISTING)
        name = _catalog_to_class_name(catalog)
        assert "Listing" in name
        assert "Page" in name

    def test_detail_archetype(self) -> None:
        catalog = _make_catalog(PageArchetype.DETAIL)
        name = _catalog_to_class_name(catalog)
        assert "Detail" in name

    def test_with_url_pattern(self) -> None:
        catalog = _make_catalog(PageArchetype.LISTING, url_pattern="/movies")
        name = _catalog_to_class_name(catalog)
        assert "Movies" in name

    def test_name_is_pascal_case(self) -> None:
        catalog = _make_catalog(PageArchetype.LISTING)
        name = _catalog_to_class_name(catalog)
        assert name[0].isupper()
        assert "_" not in name


class TestPropertyNameGeneration:
    """Property name generation from selectors/labels."""

    def test_from_label(self) -> None:
        name = _selector_to_property_name("a[href='/']", "Home", "a")
        assert name == "home"

    def test_from_aria_label(self) -> None:
        name = _selector_to_property_name("[aria-label='Search']", "", "button")
        assert name == "search"

    def test_from_id_selector(self) -> None:
        name = _selector_to_property_name("#main-nav", "", "nav")
        assert name == "main_nav"

    def test_from_href(self) -> None:
        name = _selector_to_property_name("a[href='/about']", "", "a")
        assert name == "about"

    def test_fallback_to_tag(self) -> None:
        name = _selector_to_property_name("div:nth-of-type(3)", "", "div")
        assert name.startswith("div")

    def test_max_length(self) -> None:
        name = _selector_to_property_name("div", "A" * 50, "div")
        assert len(name) <= 40

    def test_special_chars_cleaned(self) -> None:
        name = _selector_to_property_name("div", "Click Here!", "div")
        assert "!" not in name
        assert " " not in name


class TestPythonPOMGeneration:
    """Python POM class output."""

    def test_has_class_definition(self) -> None:
        catalog = _make_catalog()
        output = _generate_python_pom(catalog, "ListingPage", "https://example.com")
        assert "class ListingPage:" in output

    def test_has_constructor(self) -> None:
        catalog = _make_catalog()
        output = _generate_python_pom(catalog, "ListingPage", "https://example.com")
        assert "def __init__(self, page: Page)" in output

    def test_has_locator_assignments(self) -> None:
        catalog = _make_catalog()
        output = _generate_python_pom(catalog, "ListingPage", "https://example.com")
        assert "page.locator(" in output

    def test_has_navigate_method(self) -> None:
        catalog = _make_catalog()
        output = _generate_python_pom(catalog, "ListingPage", "https://example.com")
        assert "def navigate(self)" in output

    def test_has_search_method(self) -> None:
        catalog = _make_catalog()
        output = _generate_python_pom(catalog, "ListingPage", "https://example.com")
        assert "def search(self, query: str)" in output

    def test_has_select_item_method(self) -> None:
        catalog = _make_catalog(PageArchetype.LISTING)
        output = _generate_python_pom(catalog, "ListingPage", "https://example.com")
        assert "def select_item(self, index: int" in output

    def test_zone_comments(self) -> None:
        catalog = _make_catalog()
        output = _generate_python_pom(catalog, "ListingPage", "https://example.com")
        assert "# Navigation" in output
        assert "# Search" in output
        assert "# Content" in output

    def test_no_base_url_no_navigate(self) -> None:
        catalog = _make_catalog()
        output = _generate_python_pom(catalog, "ListingPage", "")
        assert "def navigate" not in output

    def test_deduplication(self) -> None:
        entries = [
            CatalogEntry(
                selector="a.link",
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
        catalog = _make_catalog(entries=entries)
        output = _generate_python_pom(catalog, "TestPage", "https://example.com")
        assert "self.link " in output or "self.link=" in output
        assert "self.link_2" in output


class TestTypeScriptPOMGeneration:
    """TypeScript POM class output."""

    def test_has_class_definition(self) -> None:
        catalog = _make_catalog()
        output = _generate_typescript_pom(catalog, "ListingPage", "https://example.com")
        assert "export class ListingPage" in output

    def test_has_readonly_properties(self) -> None:
        catalog = _make_catalog()
        output = _generate_typescript_pom(catalog, "ListingPage", "https://example.com")
        assert "readonly" in output
        assert ": Locator;" in output

    def test_has_constructor(self) -> None:
        catalog = _make_catalog()
        output = _generate_typescript_pom(catalog, "ListingPage", "https://example.com")
        assert "constructor(public readonly page: Page)" in output

    def test_has_navigate(self) -> None:
        catalog = _make_catalog()
        output = _generate_typescript_pom(catalog, "ListingPage", "https://example.com")
        assert "async navigate()" in output


class TestFileGeneration:
    """End-to-end file generation."""

    def test_generates_python_files(self) -> None:
        catalog = _make_catalog(url_pattern="/movies")
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generate_page_objects(
                {"sig1": catalog.model_dump()},
                tmpdir,
                framework="pytest",
                base_url="https://example.com",
            )
            assert len(paths) == 2
            assert any(path.endswith("/base_page.py") for path in paths)
            page_path = next(
                path
                for path in paths
                if path.endswith("_page.py") and not path.endswith("base_page.py")
            )
            content = Path(page_path).read_text()
            assert "class" in content

    def test_generates_typescript_files(self) -> None:
        catalog = _make_catalog()
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generate_page_objects(
                {"sig1": catalog.model_dump()},
                tmpdir,
                framework="playwright",
                base_url="https://example.com",
            )
            assert len(paths) == 2
            assert any(path.endswith("/base-page.ts") for path in paths)
            assert any(path.endswith(".ts") for path in paths)

    def test_skips_empty_catalogs(self) -> None:
        empty = PageCatalog()
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generate_page_objects(
                {"sig1": empty.model_dump()},
                tmpdir,
            )
            assert len(paths) == 0

    def test_multiple_catalogs(self) -> None:
        catalog1 = _make_catalog(PageArchetype.LISTING, url_pattern="/movies")
        catalog2 = _make_catalog(PageArchetype.DETAIL, url_pattern="/movie/1")
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generate_page_objects(
                {
                    "sig1": catalog1.model_dump(),
                    "sig2": catalog2.model_dump(),
                },
                tmpdir,
                framework="pytest",
                base_url="https://example.com",
            )
            assert len(paths) == 3

    def test_generates_component_classes_and_composes_pages(self) -> None:
        catalog = _make_catalog(PageArchetype.LISTING, url_pattern="/movies")
        navigation_component = SharedComponent(
            component_id="component-navigation",
            name="NavigationBar",
            class_name="NavigationComponent",
            entries=[
                CatalogEntry(
                    selector="a[href='/home']",
                    tag="a",
                    label="Home",
                    zone_type=ZoneType.NAVIGATION,
                    element_type="link",
                    semantic_name="home",
                )
            ],
            appears_on=["sig1"],
            frequency=1.0,
            zone=ZoneType.NAVIGATION,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generate_page_objects(
                {"sig1": catalog.model_dump()},
                tmpdir,
                framework="pytest",
                base_url="https://example.com",
                shared_components=[navigation_component.model_dump()],
            )

            component_path = Path(tmpdir) / "components" / "navigation_component.py"
            assert component_path.exists()
            component_content = component_path.read_text()
            assert "class NavigationComponent" in component_content
            assert "def click_home" in component_content

            page_path = next(
                path
                for path in paths
                if path.endswith("_page.py") and not path.endswith("base_page.py")
            )
            page_content = Path(page_path).read_text()
            assert "from pages.base_page import BasePage" in page_content
            assert "(BasePage)" in page_content
            assert (
                "from pages.components.navigation_component import NavigationComponent"
                not in page_content
            )
            assert (
                "self.navigation_component = NavigationComponent(page)"
                not in page_content
            )

            base_path = next(path for path in paths if path.endswith("base_page.py"))
            base_content = Path(base_path).read_text()
            assert (
                "from pages.components.navigation_component import NavigationComponent"
                in base_content
            )
            assert (
                "self.navigation_component = NavigationComponent(page)" in base_content
            )
            # Shared selectors should be removed from page-level properties.
            assert "self.home = page.locator(\"a[href='/home']\")" not in page_content

    def test_base_page_contains_high_frequency_components(self) -> None:
        catalog = _make_catalog(PageArchetype.LISTING, url_pattern="/movies")
        base_component = SharedComponent(
            component_id="component-navigation",
            name="NavigationBar",
            class_name="NavigationComponent",
            entries=[
                CatalogEntry(
                    selector="a[href='/home']",
                    tag="a",
                    label="Home",
                    zone_type=ZoneType.NAVIGATION,
                    element_type="link",
                    semantic_name="home",
                )
            ],
            appears_on=["sig1"],
            frequency=0.85,
            zone=ZoneType.NAVIGATION,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generate_page_objects(
                {"sig1": catalog.model_dump()},
                tmpdir,
                framework="pytest",
                base_url="https://example.com",
                shared_components=[base_component.model_dump()],
            )

            base_path = next(path for path in paths if path.endswith("base_page.py"))
            base_content = Path(base_path).read_text()
            assert "class BasePage:" in base_content
            assert "def navigate(self, path: str)" in base_content
            assert (
                "self.navigation_component = NavigationComponent(page)" in base_content
            )

            page_path = next(
                path
                for path in paths
                if path.endswith("_page.py") and not path.endswith("base_page.py")
            )
            page_content = Path(page_path).read_text()
            assert "class MoviesListingPage(BasePage):" in page_content
            assert "super().__init__(page)" in page_content
            assert "super().navigate(self.URL)" in page_content

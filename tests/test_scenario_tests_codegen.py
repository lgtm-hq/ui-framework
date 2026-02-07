"""Tests for scenario-based test code generation."""

import ast
import tempfile
from pathlib import Path

from flowscout.analysis.archetype import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)
from flowscout.analysis.site_model import NavigationEdge, PageType, SiteModel, SiteModelSummary
from flowscout.codegen.scenario_tests import generate_scenario_tests
from flowscout.discovery.actions import ActionType, OutcomeType
from flowscout.smart.scenarios import ScenarioSynthesizer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_site_model() -> SiteModel:
    """Build a minimal site model with listing + detail for testing."""
    listing_catalog = PageCatalog(
        archetype=PageArchetype.LISTING,
        url_pattern="/movies",
        entries=[
            CatalogEntry(
                selector="a.movie-card",
                tag="a",
                label="Movie card",
                zone_type=ZoneType.MAIN_CONTENT,
                element_type="link",
                semantic_name="movie_card",
            ),
            CatalogEntry(
                selector="input[type='search']",
                tag="input",
                label="Search movies",
                zone_type=ZoneType.SEARCH,
                element_type="input_search",
                semantic_name="search_movies",
                input_type="search",
            ),
        ],
    )

    detail_catalog = PageCatalog(
        archetype=PageArchetype.DETAIL,
        url_pattern="/movies/:id",
        entries=[
            CatalogEntry(
                selector="h1.movie-title",
                tag="h1",
                label="Movie title",
                zone_type=ZoneType.MAIN_CONTENT,
                element_type="heading",
                semantic_name="movie_title",
            ),
        ],
    )

    listing = PageType(
        page_type_id="sig_listing",
        name="Movie Listing",
        archetype=PageArchetype.LISTING,
        url_pattern="https://example.com/movies",
        structural_signature="sig_listing",
        instance_count=3,
        representative_url="https://example.com/movies",
        catalog=listing_catalog,
        features={"has_search"},
    )

    detail = PageType(
        page_type_id="sig_detail",
        name="Movie Detail",
        archetype=PageArchetype.DETAIL,
        url_pattern="https://example.com/movies/[^/]+",
        structural_signature="sig_detail",
        instance_count=5,
        representative_url="https://example.com/movies/1",
        catalog=detail_catalog,
    )

    edge = NavigationEdge(
        from_page_type="sig_listing",
        to_page_type="sig_detail",
        trigger="Click movie card",
        action_type=ActionType.CLICK,
        outcome=OutcomeType.NAVIGATION,
        occurrence_count=5,
    )

    synth = ScenarioSynthesizer()
    scenarios = synth.synthesize([listing, detail], [edge])

    return SiteModel(
        page_types=[listing, detail],
        navigation_edges=[edge],
        test_scenarios=scenarios,
        summary=SiteModelSummary(
            total_page_types=2,
            total_navigation_edges=1,
            total_scenarios=len(scenarios),
        ),
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestPytestGeneration:
    def test_generated_code_is_valid_python(self):
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model, output, framework="pytest", base_url="https://example.com",
            )
            code = Path(output).read_text()
            # Must parse without syntax errors
            ast.parse(code)

    def test_generated_code_imports_pom_classes(self):
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model, output, framework="pytest", base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "from pages." in code
            assert "import" in code

    def test_generated_code_has_test_functions(self):
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model, output, framework="pytest", base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "def test_" in code

    def test_generated_code_has_docstrings(self):
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model, output, framework="pytest", base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "Priority:" in code

    def test_scenario_count_matches(self):
        model = _build_site_model()
        scenario_count = len(model.test_scenarios)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model, output, framework="pytest", base_url="https://example.com",
            )
            code = Path(output).read_text()
            test_count = code.count("def test_")
            assert test_count == scenario_count


class TestTypescriptGeneration:
    def test_generated_typescript_has_test_blocks(self):
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.spec.ts")
            generate_scenario_tests(
                model, output, framework="playwright", base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "test.describe(" in code
            assert "test(" in code
            assert "import" in code

    def test_typescript_uses_await(self):
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.spec.ts")
            generate_scenario_tests(
                model, output, framework="playwright", base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "await" in code


class TestEmptyModel:
    def test_empty_model_generates_empty_file(self):
        model = SiteModel()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model, output, framework="pytest", base_url="https://example.com",
            )
            code = Path(output).read_text()
            # Should have header but no test functions
            assert "def test_" not in code

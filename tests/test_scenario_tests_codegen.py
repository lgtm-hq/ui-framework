"""Tests for scenario-based test code generation."""

import ast
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from flowscout.analysis.archetype import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)
from flowscout.analysis.site_model import (
    NavigationEdge,
    PageType,
    SiteModel,
    SiteModelSummary,
)
from flowscout.cli import _build_output_dirs
from flowscout.codegen.scenario_tests import generate_scenario_tests
from flowscout.core.state import ExplorerConfig
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
    def test_generated_code_is_valid_python(self) -> None:
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            # Must parse without syntax errors
            ast.parse(code)

    def test_generated_code_imports_pom_classes(self) -> None:
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "from pages." in code
            assert "import" in code

    def test_generated_code_has_test_functions(self) -> None:
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "def test_" in code

    def test_generated_code_has_docstrings(self) -> None:
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "Priority:" in code

    def test_scenario_count_matches(self) -> None:
        model = _build_site_model()
        scenario_count = len(model.test_scenarios)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            test_count = code.count("def test_")
            assert test_count == scenario_count


class TestTypescriptGeneration:
    def test_generated_typescript_has_test_blocks(self) -> None:
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.spec.ts")
            generate_scenario_tests(
                model,
                output,
                framework="playwright",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "test.describe(" in code
            assert "test(" in code
            assert "import" in code

    def test_typescript_uses_await(self) -> None:
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.spec.ts")
            generate_scenario_tests(
                model,
                output,
                framework="playwright",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "await" in code


class TestEmptyModel:
    def test_empty_model_generates_empty_file(self) -> None:
        model = SiteModel()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            # Should have header but no test functions
            assert "def test_" not in code


# ---------------------------------------------------------------------------
# Smart Assertion Tests
# ---------------------------------------------------------------------------


class TestSmartAssertions:
    def test_listing_load_verify_has_visibility_assertion(
        self,
    ) -> None:
        """LISTING page type with MAIN_CONTENT entries."""
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "to_be_visible()" in code
            # Still valid Python
            ast.parse(code)

    def test_detail_browse_has_heading_assertion(self) -> None:
        """browse_detail test has visibility assertion."""
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            # The browse_detail scenario should have a visibility assertion
            # for the detail page's MAIN_CONTENT entry (movie_title)
            assert "movie_title" in code
            assert "to_be_visible()" in code

    def test_search_has_content_assertion(self) -> None:
        """has_search feature → search verification has visibility assertion."""
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            # Search scenario should assert content is visible
            assert "to_be_visible()" in code
            assert "movie_card" in code

    def test_title_assertion_present(self) -> None:
        """load_verify always has to_have_title assertion."""
        model = _build_site_model()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            assert "to_have_title" in code

    def test_empty_catalog_fallback(self) -> None:
        """Empty catalog → graceful degradation to comments (no regression)."""
        empty_pt = PageType(
            page_type_id="sig_empty",
            name="Empty Page",
            archetype=PageArchetype.LANDING,
            structural_signature="sig_empty",
            instance_count=1,
            representative_url="https://example.com/empty",
            catalog=PageCatalog(archetype=PageArchetype.LANDING),
        )

        synth = ScenarioSynthesizer()
        scenarios = synth.synthesize([empty_pt], [])

        model = SiteModel(
            page_types=[empty_pt],
            navigation_edges=[],
            test_scenarios=scenarios,
            summary=SiteModelSummary(
                total_page_types=1, total_scenarios=len(scenarios)
            ),
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "scenario_tests.py")
            generate_scenario_tests(
                model,
                output,
                framework="pytest",
                base_url="https://example.com",
            )
            code = Path(output).read_text()
            # Should still have title assertion from load_verify
            assert "to_have_title" in code
            # Should be valid Python even without catalog entries
            ast.parse(code)


# ---------------------------------------------------------------------------
# Workspace Layout Tests
# ---------------------------------------------------------------------------


class TestBuildOutputDirs:
    def test_build_output_dirs_smart_workspace(self) -> None:
        """Smart workspace path structure is correct."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExplorerConfig(
                start_url="https://example.com/movies",
                output_dir=tmpdir,
            )
            now = datetime(2026, 2, 7, 14, 30, 0, tzinfo=timezone.utc)
            run_dir, workspace_dir = _build_output_dirs(
                config,
                now,
                smart_workspace=True,
            )

            assert workspace_dir is not None
            assert "example.com" in str(workspace_dir)
            assert "runs" in str(run_dir)
            assert "2026-02-07_14.30.00" in str(run_dir)
            assert run_dir.exists()

    def test_build_output_dirs_legacy(self) -> None:
        """Legacy path structure unchanged."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExplorerConfig(
                start_url="https://example.com/movies",
                output_dir=tmpdir,
            )
            now = datetime(2026, 2, 7, 14, 30, 0, tzinfo=timezone.utc)
            run_dir, workspace_dir = _build_output_dirs(
                config,
                now,
                smart_workspace=False,
            )

            assert workspace_dir is None
            assert "2026" in str(run_dir)
            assert "02.February" in str(run_dir)
            assert "07-02-2026" in str(run_dir)
            assert "14.30.00" in str(run_dir)
            assert run_dir.exists()

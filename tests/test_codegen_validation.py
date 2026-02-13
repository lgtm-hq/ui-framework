"""Validation tests for generated page objects and scenario tests."""

from __future__ import annotations

import shutil
import subprocess  # nosec B404 - used only for CompletedProcess test doubles
from pathlib import Path
from typing import Any

import pytest

from flowscout.codegen.page_objects import generate_page_objects
from flowscout.codegen.scenario_tests import generate_scenario_tests
from flowscout.codegen.validator import (
    validate_python_imports,
    validate_python_playwright_api,
    validate_python_sources,
    validate_typescript_playwright_api,
    validate_typescript_sources,
)
from flowscout.modeling.archetype import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)
from flowscout.modeling.scenarios import ScenarioSynthesizer
from flowscout.modeling.site_model import (
    NavigationEdge,
    PageType,
    SiteModel,
    SiteModelSummary,
)
from flowscout.discovery.actions import ActionType, OutcomeType


def _build_minimal_site_model() -> SiteModel:
    """Build a small but representative site model for codegen tests."""
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
            )
        ],
    )

    listing = PageType(
        page_type_id="sig_listing",
        name="Movie Listing",
        archetype=PageArchetype.LISTING,
        url_pattern="https://example.com/movies",
        structural_signature="sig_listing",
        instance_count=2,
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
        instance_count=2,
        representative_url="https://example.com/movies/1",
        catalog=detail_catalog,
    )
    edge = NavigationEdge(
        from_page_type="sig_listing",
        to_page_type="sig_detail",
        trigger="Open movie card",
        action_type=ActionType.CLICK,
        outcome=OutcomeType.NAVIGATION,
        occurrence_count=2,
    )
    scenarios = ScenarioSynthesizer().synthesize(
        page_types=[listing, detail],
        nav_edges=[edge],
    )

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


def test_python_codegen_roundtrip_validation(tmp_path: Path) -> None:
    """Generated Python POMs/tests should compile and have resolvable imports."""
    model = _build_minimal_site_model()
    pages_dir = tmp_path / "pages"
    scenario_path = tmp_path / "scenario_tests.py"

    page_paths = generate_page_objects(
        catalogs={
            page_type.page_type_id: page_type.catalog
            for page_type in model.page_types
            if page_type.catalog.entries
        },
        output_dir=str(pages_dir),
        framework="pytest",
        base_url="https://example.com",
    )
    generate_scenario_tests(
        site_model=model,
        output_path=str(scenario_path),
        framework="pytest",
        base_url="https://example.com",
    )

    python_paths = [*page_paths, str(scenario_path)]
    validate_python_sources(paths=python_paths)
    validate_python_playwright_api(paths=python_paths)
    for path in python_paths:
        validate_python_imports(
            test_file=path,
            package_root=tmp_path,
            package_prefix="pages",
        )


def test_typescript_codegen_roundtrip_validation(tmp_path: Path) -> None:
    """Generated TypeScript POMs/tests should pass ``tsc --noEmit`` checks."""
    if shutil.which("tsc") is None:
        pytest.skip("tsc is required for TypeScript codegen validation.")

    model = _build_minimal_site_model()
    pages_dir = tmp_path / "pages"
    scenario_path = tmp_path / "scenario_tests.spec.ts"

    page_paths = generate_page_objects(
        catalogs={
            page_type.page_type_id: page_type.catalog
            for page_type in model.page_types
            if page_type.catalog.entries
        },
        output_dir=str(pages_dir),
        framework="playwright",
        base_url="https://example.com",
    )
    generate_scenario_tests(
        site_model=model,
        output_path=str(scenario_path),
        framework="playwright",
        base_url="https://example.com",
    )

    ts_paths = [*page_paths, str(scenario_path)]
    validate_typescript_playwright_api(paths=ts_paths)
    validate_typescript_sources(
        paths=ts_paths,
        cwd=tmp_path,
    )


def test_typescript_validation_uses_no_emit_flag(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """TypeScript validator should invoke ``tsc`` with ``--noEmit``."""
    source_path = tmp_path / "sample.ts"
    source_path.write_text("export const value = 1;")

    captured: dict[str, Any] = {}

    def _fake_runner(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
        command = list(args[0]) if args else []
        captured["command"] = command
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout="",
            stderr="",
        )

    monkeypatch.setattr(shutil, "which", lambda _: "/usr/local/bin/tsc")
    validate_typescript_sources(
        paths=[source_path],
        cwd=tmp_path,
        runner=_fake_runner,
    )

    assert "--noEmit" in captured["command"]

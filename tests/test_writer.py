"""Tests for POM file writer and preview rendering."""

from __future__ import annotations

import tempfile
from pathlib import Path

from flowscout.codegen.adapters.playwright_python import PlaywrightPythonAdapter
from flowscout.codegen.adapters.playwright_ts import PlaywrightTSAdapter
from flowscout.codegen.pom_model import (
    MethodKind,
    POMClass,
    POMMethod,
    POMProperty,
    POMSuite,
)
from flowscout.codegen.writer import render_previews, write_pom_suite
from flowscout.modeling.archetype import PageArchetype, ZoneType


def _make_suite() -> POMSuite:
    return POMSuite(
        base_page=POMClass(
            class_name="BasePage",
            methods=[
                POMMethod(
                    kind=MethodKind.NAVIGATE,
                    name="navigate",
                    parameters=[("path", "str")],
                ),
            ],
        ),
        components=[
            POMClass(
                class_name="NavComponent",
                is_component=True,
                component_name="Navigation",
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
                        kind=MethodKind.CLICK,
                        name="click_home",
                        target_property="home",
                    ),
                ],
            ),
        ],
        pages=[
            POMClass(
                class_name="MoviesPage",
                parent_class="BasePage",
                archetype=PageArchetype.LISTING,
                url_pattern="/movies",
                base_url="https://example.com",
                properties=[
                    POMProperty(
                        name="card",
                        selector=".movie-card",
                        zone=ZoneType.MAIN_CONTENT,
                        zone_label="Content",
                    ),
                ],
                methods=[
                    POMMethod(
                        kind=MethodKind.NAVIGATE,
                        name="navigate",
                    ),
                ],
            ),
        ],
    )


class TestWritePomSuite:
    def test_python_creates_expected_files(self) -> None:
        suite = _make_suite()
        adapter = PlaywrightPythonAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = write_pom_suite(suite, adapter, tmpdir)
            assert len(paths) == 3
            assert any(p.endswith("base_page.py") for p in paths)
            assert any(p.endswith("nav_component.py") for p in paths)
            assert any(p.endswith("movies_page.py") for p in paths)

    def test_typescript_creates_expected_files(self) -> None:
        suite = _make_suite()
        adapter = PlaywrightTSAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = write_pom_suite(suite, adapter, tmpdir)
            assert len(paths) == 3
            assert any(p.endswith("base-page.ts") for p in paths)
            assert any(p.endswith("nav-component.ts") for p in paths)
            assert any(p.endswith("movies-page.ts") for p in paths)

    def test_creates_components_directory(self) -> None:
        suite = _make_suite()
        adapter = PlaywrightPythonAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            write_pom_suite(suite, adapter, tmpdir)
            assert (Path(tmpdir) / "components").is_dir()

    def test_files_have_content(self) -> None:
        suite = _make_suite()
        adapter = PlaywrightPythonAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = write_pom_suite(suite, adapter, tmpdir)
            for path in paths:
                content = Path(path).read_text()
                assert len(content) > 0
                assert "class " in content

    def test_no_components_skips_directory(self) -> None:
        suite = POMSuite(
            pages=[
                POMClass(
                    class_name="SimplePage",
                    archetype=PageArchetype.LANDING,
                    properties=[
                        POMProperty(
                            name="heading",
                            selector="h1",
                            zone_label="Content",
                        ),
                    ],
                ),
            ],
        )
        adapter = PlaywrightPythonAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = write_pom_suite(suite, adapter, tmpdir)
            assert not (Path(tmpdir) / "components").exists()
            assert len(paths) == 2


class TestRenderPreviews:
    def test_returns_python_and_typescript(self) -> None:
        page_class = POMClass(
            class_name="MoviesPage",
            archetype=PageArchetype.LISTING,
            base_url="https://example.com",
            properties=[
                POMProperty(
                    name="card",
                    selector=".card",
                    zone_label="Content",
                ),
            ],
            methods=[
                POMMethod(
                    kind=MethodKind.NAVIGATE,
                    name="navigate",
                ),
            ],
        )
        previews = render_previews(
            {"listing_1": page_class},
            python_adapter=PlaywrightPythonAdapter(),
            ts_adapter=PlaywrightTSAdapter(),
        )
        assert "listing_1" in previews
        preview = previews["listing_1"]
        assert preview["class_name"] == "MoviesPage"
        assert "class MoviesPage" in preview["python"]
        assert "export class MoviesPage" in preview["typescript"]

    def test_empty_input_returns_empty(self) -> None:
        previews = render_previews(
            {},
            python_adapter=PlaywrightPythonAdapter(),
            ts_adapter=PlaywrightTSAdapter(),
        )
        assert previews == {}

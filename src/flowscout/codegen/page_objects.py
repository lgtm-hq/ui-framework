"""Page Object Model generation from element catalogs.

Thin facade delegating to pom_builder -> adapter -> writer pipeline.
"""

from __future__ import annotations

from typing import Any

from flowscout.codegen.adapters import get_adapter
from flowscout.codegen.adapters.playwright_python import PlaywrightPythonAdapter
from flowscout.codegen.adapters.playwright_ts import PlaywrightTSAdapter
from flowscout.codegen.pom_builder import build_pom_suite, build_pom_suite_for_preview
from flowscout.codegen.writer import render_previews, write_pom_suite


def generate_page_objects(
    catalogs: dict[str, Any],
    output_dir: str,
    *,
    framework: str = "pytest",
    base_url: str = "",
    shared_components: list[Any] | None = None,
) -> list[str]:
    """Generate POM classes from page catalogs.

    Args:
        catalogs: sig -> PageCatalog dict (from SmartPlanner.get_all_catalogs()).
        output_dir: Directory to write POM files into.
        framework: "pytest" for Python or "playwright" for TypeScript.
        base_url: Base URL for navigate() methods.
        shared_components: Optional shared components from SiteModel.

    Returns:
        List of generated file paths.
    """
    suite = build_pom_suite(
        catalogs,
        base_url=base_url,
        shared_components=shared_components,
    )
    if not suite.pages and not suite.components:
        return []
    adapter = get_adapter(framework)
    return write_pom_suite(suite, adapter, output_dir)


def generate_page_object_previews(
    page_types: list[Any],
    *,
    shared_components: list[Any] | None = None,
    base_url: str = "",
) -> dict[str, dict[str, str]]:
    """Generate per-page type POM code previews for report embedding.

    Args:
        page_types: SiteModel page type objects/dicts.
        shared_components: Optional shared components from SiteModel.
        base_url: Base URL for generated navigate methods.

    Returns:
        Mapping of page_type_id -> preview payload with class name and
        Python/TypeScript source.
    """
    page_classes = build_pom_suite_for_preview(
        page_types,
        shared_components=shared_components,
        base_url=base_url,
    )
    if not page_classes:
        return {}
    return render_previews(
        page_classes,
        python_adapter=PlaywrightPythonAdapter(),
        ts_adapter=PlaywrightTSAdapter(),
    )

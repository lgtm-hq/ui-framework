"""POM-based test generation — generates tests that use Page Object Model classes."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flowscout.analysis.archetype import PageArchetype, PageCatalog, ZoneType
from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.codegen.page_objects import (
    _catalog_to_class_name,
    _parse_catalog,
    _to_snake_case,
)


def generate_pom_tests(
    result: ExplorationResult,
    catalogs: dict[str, Any],
    output_path: str,
    *,
    framework: str = "pytest",
) -> str:
    """Generate POM-based tests from exploration results.

    Args:
        result: The exploration result.
        catalogs: sig -> PageCatalog dict.
        output_path: Where to write the test file.
        framework: "pytest" or "playwright".

    Returns:
        Path to the generated test file.
    """
    if framework == "pytest":
        content = _generate_pytest_pom_tests(result, catalogs)
    else:
        content = _generate_playwright_pom_tests(result, catalogs)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return str(path)


def _generate_pytest_pom_tests(
    result: ExplorationResult,
    catalogs: dict[str, Any],
) -> str:
    """Generate pytest tests that import and use POM classes."""
    start_url = result.config.get("start_url", "https://example.com")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Map sigs to class names and modules
    pom_info: dict[str, tuple[str, str]] = {}  # sig -> (class_name, module_name)
    for sig, catalog_data in catalogs.items():
        catalog = _parse_catalog(catalog_data)
        if not catalog.entries:
            continue
        class_name = _catalog_to_class_name(catalog)
        module_name = _to_snake_case(class_name)
        pom_info[sig] = (class_name, module_name)

    lines: list[str] = [
        '"""',
        "Auto-generated POM-based Playwright tests.",
        "",
        f"Source: {start_url}",
        f"Generated: {timestamp}",
        '"""',
        "",
        "import pytest",
        "from playwright.sync_api import Page, expect",
        "",
    ]

    # Import POM classes
    for sig, (class_name, module_name) in pom_info.items():
        lines.append(f"from pages.{module_name} import {class_name}")
    lines.append("")
    lines.append("")

    # Find catalogs that are listings with search
    used_names: set[str] = set()

    for sig, catalog_data in catalogs.items():
        catalog = _parse_catalog(catalog_data)
        if not catalog.entries:
            continue
        if sig not in pom_info:
            continue

        class_name, _ = pom_info[sig]
        archetype = catalog.archetype

        # Generate archetype-appropriate tests
        if archetype == PageArchetype.LISTING:
            _add_listing_tests(lines, class_name, catalog, used_names)
        elif archetype == PageArchetype.DETAIL:
            _add_detail_tests(lines, class_name, catalog, used_names)
        elif archetype == PageArchetype.FORM:
            _add_form_tests(lines, class_name, catalog, used_names)
        elif archetype == PageArchetype.SEARCH_RESULTS:
            _add_search_tests(lines, class_name, catalog, used_names)

    # Generate navigation test if we have a listing
    _add_navigation_test(lines, catalogs, pom_info, used_names)

    return "\n".join(lines)


def _add_listing_tests(
    lines: list[str],
    class_name: str,
    catalog: PageCatalog,
    used_names: set[str],
) -> None:
    """Add tests for a listing page."""
    func_name = _unique_name(f"test_{_to_snake_case(class_name)}_loads", used_names)
    var_name = _to_snake_case(class_name).replace("_page", "")

    lines.extend([
        f"def {func_name}(page: Page) -> None:",
        f'    """{class_name}: page loads with content."""',
        f"    {var_name} = {class_name}(page)",
        f"    {var_name}.navigate()",
        f"    expect(page).to_have_url(page.url)",
        "",
        "",
    ])

    # Search test if search zone exists
    has_search = any(e.zone_type == ZoneType.SEARCH for e in catalog.entries)
    if has_search:
        func_name = _unique_name(
            f"test_{_to_snake_case(class_name)}_search", used_names
        )
        lines.extend([
            f"def {func_name}(page: Page) -> None:",
            f'    """{class_name}: search returns results."""',
            f"    {var_name} = {class_name}(page)",
            f"    {var_name}.navigate()",
            f'    {var_name}.search("test query")',
            "",
            "",
        ])


def _add_detail_tests(
    lines: list[str],
    class_name: str,
    catalog: PageCatalog,
    used_names: set[str],
) -> None:
    """Add tests for a detail page."""
    func_name = _unique_name(f"test_{_to_snake_case(class_name)}_content", used_names)
    var_name = _to_snake_case(class_name).replace("_page", "")

    lines.extend([
        f"def {func_name}(page: Page) -> None:",
        f'    """{class_name}: detail page has expected content."""',
        f"    {var_name} = {class_name}(page)",
        f"    {var_name}.navigate()",
        f"    expect(page).to_have_url(page.url)",
        "",
        "",
    ])


def _add_form_tests(
    lines: list[str],
    class_name: str,
    catalog: PageCatalog,
    used_names: set[str],
) -> None:
    """Add tests for a form page."""
    func_name = _unique_name(f"test_{_to_snake_case(class_name)}_visible", used_names)
    var_name = _to_snake_case(class_name).replace("_page", "")

    lines.extend([
        f"def {func_name}(page: Page) -> None:",
        f'    """{class_name}: form page loads."""',
        f"    {var_name} = {class_name}(page)",
        f"    {var_name}.navigate()",
        "",
        "",
    ])


def _add_search_tests(
    lines: list[str],
    class_name: str,
    catalog: PageCatalog,
    used_names: set[str],
) -> None:
    """Add tests for a search results page."""
    func_name = _unique_name(f"test_{_to_snake_case(class_name)}_loads", used_names)
    var_name = _to_snake_case(class_name).replace("_page", "")

    lines.extend([
        f"def {func_name}(page: Page) -> None:",
        f'    """{class_name}: search results visible."""',
        f"    {var_name} = {class_name}(page)",
        f"    {var_name}.navigate()",
        "",
        "",
    ])


def _add_navigation_test(
    lines: list[str],
    catalogs: dict[str, Any],
    pom_info: dict[str, tuple[str, str]],
    used_names: set[str],
) -> None:
    """Add a navigation test that goes listing -> detail if both exist."""
    listing_sig = None
    detail_sig = None

    for sig, catalog_data in catalogs.items():
        catalog = _parse_catalog(catalog_data)
        if catalog.archetype == PageArchetype.LISTING and sig in pom_info:
            listing_sig = sig
        if catalog.archetype == PageArchetype.DETAIL and sig in pom_info:
            detail_sig = sig

    if listing_sig and detail_sig:
        listing_class, _ = pom_info[listing_sig]
        detail_class, _ = pom_info[detail_sig]
        func_name = _unique_name("test_browse_and_select_item", used_names)
        listing_var = _to_snake_case(listing_class).replace("_page", "")
        detail_var = _to_snake_case(detail_class).replace("_page", "")

        lines.extend([
            f"def {func_name}(page: Page) -> None:",
            f'    """Navigate from listing to detail page."""',
            f"    {listing_var} = {listing_class}(page)",
            f"    {listing_var}.navigate()",
            f"    {listing_var}.select_item(0)",
            f"    {detail_var} = {detail_class}(page)",
            f"    expect(page).to_have_url(page.url)",
            "",
            "",
        ])


def _unique_name(base: str, used: set[str]) -> str:
    """Generate a unique test function name."""
    if base not in used:
        used.add(base)
        return base
    i = 2
    while f"{base}_{i}" in used:
        i += 1
    name = f"{base}_{i}"
    used.add(name)
    return name


def _generate_playwright_pom_tests(
    result: ExplorationResult,
    catalogs: dict[str, Any],
) -> str:
    """Generate Playwright Test (TypeScript) tests using POM classes."""
    start_url = result.config.get("start_url", "https://example.com")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    pom_info: dict[str, tuple[str, str]] = {}
    for sig, catalog_data in catalogs.items():
        catalog = _parse_catalog(catalog_data)
        if not catalog.entries:
            continue
        class_name = _catalog_to_class_name(catalog)
        module_name = re.sub(r"(?<!^)(?=[A-Z])", "-", class_name).lower()
        pom_info[sig] = (class_name, module_name)

    lines: list[str] = [
        f"// Auto-generated POM-based Playwright tests",
        f"// Source: {start_url}",
        f"// Generated: {timestamp}",
        "",
        "import { test, expect } from '@playwright/test';",
    ]

    for sig, (class_name, module_name) in pom_info.items():
        lines.append(f"import {{ {class_name} }} from './pages/{module_name}';")
    lines.extend(["", ""])

    for sig, catalog_data in catalogs.items():
        catalog = _parse_catalog(catalog_data)
        if not catalog.entries or sig not in pom_info:
            continue
        class_name, _ = pom_info[sig]
        archetype = catalog.archetype

        lines.append(f"test.describe('{class_name}', () => {{")

        if archetype == PageArchetype.LISTING:
            lines.extend([
                f"  test('loads content', async ({{ page }}) => {{",
                f"    const listing = new {class_name}(page);",
                f"    await listing.navigate();",
                f"    await expect(page).toHaveURL(page.url());",
                f"  }});",
            ])
        elif archetype == PageArchetype.DETAIL:
            lines.extend([
                f"  test('has expected content', async ({{ page }}) => {{",
                f"    const detail = new {class_name}(page);",
                f"    await detail.navigate();",
                f"    await expect(page).toHaveURL(page.url());",
                f"  }});",
            ])

        lines.extend(["});", ""])

    return "\n".join(lines)

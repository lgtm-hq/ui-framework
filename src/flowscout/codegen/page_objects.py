"""Page Object Model generation from element catalogs."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flowscout.analysis.archetype import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)


def generate_page_objects(
    catalogs: dict[str, Any],
    output_dir: str,
    *,
    framework: str = "pytest",
    base_url: str = "",
) -> list[str]:
    """Generate POM classes from page catalogs.

    Args:
        catalogs: sig -> PageCatalog dict (from SmartPlanner.get_all_catalogs()).
        output_dir: Directory to write POM files into.
        framework: "pytest" for Python or "playwright" for TypeScript.
        base_url: Base URL for navigate() methods.

    Returns:
        List of generated file paths.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    generated: list[str] = []
    for sig, catalog_data in catalogs.items():
        catalog = _parse_catalog(catalog_data)
        if not catalog.entries:
            continue

        class_name = _catalog_to_class_name(catalog)
        if framework == "pytest":
            content = _generate_python_pom(catalog, class_name, base_url)
            filename = _to_snake_case(class_name) + ".py"
        else:
            content = _generate_typescript_pom(catalog, class_name, base_url)
            filename = _to_kebab_case(class_name) + ".ts"

        path = out / filename
        path.write_text(content)
        generated.append(str(path))

    return generated


def _parse_catalog(data: Any) -> PageCatalog:
    """Parse catalog from either a dict or PageCatalog."""
    if isinstance(data, PageCatalog):
        return data
    if isinstance(data, dict):
        return PageCatalog.model_validate(data)
    return PageCatalog()


def _catalog_to_class_name(catalog: PageCatalog) -> str:
    """Generate a class name from archetype and URL pattern."""
    archetype = catalog.archetype.value if catalog.archetype else "page"
    url_part = catalog.url_pattern or ""

    # Extract last path segment
    if url_part:
        segment = url_part.rstrip("/").split("/")[-1]
        segment = re.sub(r"[^\w]", "_", segment)
    else:
        segment = ""

    # Build name
    parts = []
    if segment:
        parts.append(segment)
    parts.append(archetype)
    parts.append("page")

    raw = "_".join(parts)
    # Convert to PascalCase
    return "".join(w.capitalize() for w in raw.split("_") if w)


def _to_snake_case(name: str) -> str:
    """Convert PascalCase to snake_case."""
    result = re.sub(r"(?<!^)(?=[A-Z])", "_", name)
    return result.lower()


def _to_kebab_case(name: str) -> str:
    """Convert PascalCase to kebab-case."""
    result = re.sub(r"(?<!^)(?=[A-Z])", "-", name)
    return result.lower()


def _selector_to_property_name(selector: str, label: str, tag: str) -> str:
    """Generate a clean property name from selector/label/tag."""
    # Prefer label if clean enough
    text = label if label and len(label) <= 30 else ""

    if not text:
        # Extract from selector
        m = re.search(r"\[aria-label=['\"]([^'\"]+)['\"]", selector)
        if m:
            text = m.group(1)
        elif "#" in selector:
            text = selector.split("#")[-1].split("[")[0].split("]")[0]
        elif "href=" in selector:
            m = re.search(r"href=['\"]([^'\"]+)['\"]", selector)
            if m:
                href = m.group(1).strip("/")
                text = href.split("/")[-1] if "/" in href else href
                if not text or text == "#":
                    text = selector

    if not text:
        text = selector

    # Sanitize
    clean = re.sub(r"[^\w\s]", " ", text.lower())
    clean = re.sub(r"\s+", "_", clean.strip())
    clean = re.sub(r"_+", "_", clean).strip("_")

    if not clean or not clean[0].isalpha():
        clean = f"{tag}_{clean}" if clean else tag

    return clean[:40]


def _group_by_zone(entries: list[CatalogEntry]) -> dict[ZoneType, list[CatalogEntry]]:
    """Group catalog entries by zone."""
    zones: dict[ZoneType, list[CatalogEntry]] = {}
    for entry in entries:
        zones.setdefault(entry.zone_type, []).append(entry)
    return zones


_ZONE_LABELS: dict[ZoneType, str] = {
    ZoneType.NAVIGATION: "Navigation",
    ZoneType.HEADER: "Header",
    ZoneType.SEARCH: "Search",
    ZoneType.FILTER: "Filters",
    ZoneType.MAIN_CONTENT: "Content",
    ZoneType.SIDEBAR: "Sidebar",
    ZoneType.PAGINATION: "Pagination",
    ZoneType.FOOTER: "Footer",
    ZoneType.FORM: "Form",
}


def _generate_python_pom(
    catalog: PageCatalog, class_name: str, base_url: str
) -> str:
    """Generate a Python POM class."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    archetype = catalog.archetype.value if catalog.archetype else "unknown"
    url_pattern = catalog.url_pattern or "*"

    lines: list[str] = [
        '"""',
        f"Auto-generated Page Object Model — {class_name}.",
        "",
        f"Archetype: {archetype}",
        f"URL pattern: {url_pattern}",
        f"Generated: {timestamp}",
        '"""',
        "",
        "from playwright.sync_api import Locator, Page, expect",
        "",
        "",
        f"class {class_name}:",
        f'    """Page object for: {archetype} page.',
        f"    URL pattern: {url_pattern}",
        '    """',
        "",
    ]

    if base_url:
        lines.append(f'    URL = "{base_url}"')
        lines.append("")

    # Constructor
    lines.append("    def __init__(self, page: Page) -> None:")
    lines.append("        self.page = page")

    grouped = _group_by_zone(catalog.entries)
    seen_names: set[str] = set()

    for zone_type in ZoneType:
        zone_entries = grouped.get(zone_type, [])
        if not zone_entries:
            continue

        label = _ZONE_LABELS.get(zone_type, zone_type.value)
        lines.append(f"        # {label}")

        for entry in zone_entries:
            prop_name = _selector_to_property_name(
                entry.selector, entry.semantic_name or entry.label, entry.tag
            )
            # Deduplicate
            if prop_name in seen_names:
                i = 2
                while f"{prop_name}_{i}" in seen_names:
                    i += 1
                prop_name = f"{prop_name}_{i}"
            seen_names.add(prop_name)

            sel_escaped = entry.selector.replace('"', '\\"')
            lines.append(
                f'        self.{prop_name} = page.locator("{sel_escaped}")'
            )

    lines.append("")

    # Navigate method
    if base_url:
        lines.extend([
            "    def navigate(self) -> None:",
            "        self.page.goto(self.URL)",
            '        self.page.wait_for_load_state("networkidle")',
            "",
        ])

    # Search method if search zone exists
    if ZoneType.SEARCH in grouped:
        search_entries = grouped[ZoneType.SEARCH]
        input_entry = next(
            (e for e in search_entries if "input" in e.element_type), None
        )
        if input_entry:
            sel = input_entry.selector.replace('"', '\\"')
            lines.extend([
                "    def search(self, query: str) -> None:",
                f'        self.page.fill("{sel}", query)',
                f'        self.page.press("{sel}", "Enter")',
                "",
            ])

    # Select item method if listing with content items
    if (
        catalog.archetype == PageArchetype.LISTING
        and ZoneType.MAIN_CONTENT in grouped
    ):
        content_entries = [
            e for e in grouped[ZoneType.MAIN_CONTENT]
            if e.element_type in ("link", "button", "other")
        ]
        if content_entries:
            sel = content_entries[0].selector.replace('"', '\\"')
            lines.extend([
                "    def select_item(self, index: int = 0) -> None:",
                f'        self.page.locator("{sel}").nth(index).click()',
                "",
            ])

    return "\n".join(lines)


def _generate_typescript_pom(
    catalog: PageCatalog, class_name: str, base_url: str
) -> str:
    """Generate a TypeScript POM class."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    archetype = catalog.archetype.value if catalog.archetype else "unknown"
    url_pattern = catalog.url_pattern or "*"

    lines: list[str] = [
        f"// Auto-generated Page Object Model — {class_name}",
        f"// Archetype: {archetype}",
        f"// URL pattern: {url_pattern}",
        f"// Generated: {timestamp}",
        "",
        "import { type Locator, type Page } from '@playwright/test';",
        "",
        f"export class {class_name} {{",
    ]

    if base_url:
        lines.append(f"  static readonly URL = '{base_url}';")
        lines.append("")

    # Readonly properties
    grouped = _group_by_zone(catalog.entries)
    seen_names: set[str] = set()

    for zone_type in ZoneType:
        zone_entries = grouped.get(zone_type, [])
        if not zone_entries:
            continue

        label = _ZONE_LABELS.get(zone_type, zone_type.value)
        lines.append(f"  // {label}")

        for entry in zone_entries:
            prop_name = _selector_to_property_name(
                entry.selector, entry.semantic_name or entry.label, entry.tag
            )
            if prop_name in seen_names:
                i = 2
                while f"{prop_name}_{i}" in seen_names:
                    i += 1
                prop_name = f"{prop_name}_{i}"
            seen_names.add(prop_name)

            lines.append(f"  readonly {prop_name}: Locator;")

    lines.append("")

    # Constructor
    lines.append("  constructor(public readonly page: Page) {")
    seen_names_ctor: set[str] = set()

    for zone_type in ZoneType:
        zone_entries = grouped.get(zone_type, [])
        if not zone_entries:
            continue

        for entry in zone_entries:
            prop_name = _selector_to_property_name(
                entry.selector, entry.semantic_name or entry.label, entry.tag
            )
            if prop_name in seen_names_ctor:
                i = 2
                while f"{prop_name}_{i}" in seen_names_ctor:
                    i += 1
                prop_name = f"{prop_name}_{i}"
            seen_names_ctor.add(prop_name)

            sel_escaped = entry.selector.replace("'", "\\'")
            lines.append(
                f"    this.{prop_name} = page.locator('{sel_escaped}');"
            )

    lines.append("  }")
    lines.append("")

    # Navigate
    if base_url:
        lines.extend([
            "  async navigate() {",
            f"    await this.page.goto({class_name}.URL);",
            "    await this.page.waitForLoadState('networkidle');",
            "  }",
            "",
        ])

    # Search
    if ZoneType.SEARCH in grouped:
        search_entries = grouped[ZoneType.SEARCH]
        input_entry = next(
            (e for e in search_entries if "input" in e.element_type), None
        )
        if input_entry:
            sel = input_entry.selector.replace("'", "\\'")
            lines.extend([
                "  async search(query: string) {",
                f"    await this.page.fill('{sel}', query);",
                f"    await this.page.press('{sel}', 'Enter');",
                "  }",
                "",
            ])

    # Select item
    if (
        catalog.archetype == PageArchetype.LISTING
        and ZoneType.MAIN_CONTENT in grouped
    ):
        content_entries = [
            e for e in grouped[ZoneType.MAIN_CONTENT]
            if e.element_type in ("link", "button", "other")
        ]
        if content_entries:
            sel = content_entries[0].selector.replace("'", "\\'")
            lines.extend([
                "  async selectItem(index: number = 0) {",
                f"    await this.page.locator('{sel}').nth(index).click();",
                "  }",
                "",
            ])

    lines.append("}")
    lines.append("")

    return "\n".join(lines)

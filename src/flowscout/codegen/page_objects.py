"""Page Object Model generation from element catalogs."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flowscout.modeling.archetype import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)
from flowscout.modeling.components import SharedComponent


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
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    parsed_components = [
        _parse_shared_component(component_data)
        for component_data in (shared_components or [])
    ]
    parsed_components = [
        component for component in parsed_components if component.entries
    ]
    page_components = _build_page_component_map(parsed_components=parsed_components)

    generated: list[str] = []
    if parsed_components:
        components_dir = out / "components"
        components_dir.mkdir(parents=True, exist_ok=True)
        for component in parsed_components:
            if framework == "pytest":
                content = _generate_python_component(component)
                filename = _to_snake_case(component.class_name) + ".py"
            else:
                content = _generate_typescript_component(component)
                filename = _to_kebab_case(component.class_name) + ".ts"

            path = components_dir / filename
            path.write_text(content)
            generated.append(str(path))

    for sig, catalog_data in catalogs.items():
        catalog = _parse_catalog(catalog_data)
        components_for_page = page_components.get(sig, [])
        filtered_catalog = _strip_component_entries(
            catalog=catalog,
            components_for_page=components_for_page,
        )
        if not filtered_catalog.entries and not components_for_page:
            continue

        class_name = _catalog_to_class_name(catalog)
        if framework == "pytest":
            content = _generate_python_pom(
                filtered_catalog,
                class_name,
                base_url,
                page_components=components_for_page,
            )
            filename = _to_snake_case(class_name) + ".py"
        else:
            content = _generate_typescript_pom(
                filtered_catalog,
                class_name,
                base_url,
                page_components=components_for_page,
            )
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


def _parse_shared_component(data: Any) -> SharedComponent:
    """Parse a shared component from dict/model input."""
    if isinstance(data, SharedComponent):
        return data
    if isinstance(data, dict):
        return SharedComponent.model_validate(data)
    return SharedComponent(component_id="", name="", class_name="")


def _build_page_component_map(
    *,
    parsed_components: list[SharedComponent],
) -> dict[str, list[SharedComponent]]:
    """Index components by page_type_id."""
    component_map: dict[str, list[SharedComponent]] = {}
    for component in parsed_components:
        for page_type_id in component.appears_on:
            component_map.setdefault(page_type_id, []).append(component)

    for page_type_id, component_list in component_map.items():
        component_map[page_type_id] = sorted(
            component_list,
            key=lambda component: component.class_name,
        )
    return component_map


def _strip_component_entries(
    *,
    catalog: PageCatalog,
    components_for_page: list[SharedComponent],
) -> PageCatalog:
    """Remove entries that are provided by shared components."""
    if not components_for_page:
        return catalog

    shared_entry_keys = {
        (entry.zone_type, entry.selector)
        for component in components_for_page
        for entry in component.entries
    }
    if not shared_entry_keys:
        return catalog

    filtered_entries = [
        entry
        for entry in catalog.entries
        if (entry.zone_type, entry.selector) not in shared_entry_keys
    ]
    return catalog.model_copy(update={"entries": filtered_entries})


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
    return "".join(word.capitalize() for word in raw.split("_") if word)


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
        match = re.search(r"\[aria-label=['\"]([^'\"]+)['\"]", selector)
        if match:
            text = match.group(1)
        elif "#" in selector:
            text = selector.split("#")[-1].split("[")[0].split("]")[0]
        elif "href=" in selector:
            match = re.search(r"href=['\"]([^'\"]+)['\"]", selector)
            if match:
                href = match.group(1).strip("/")
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


def _build_entry_property_names(entries: list[CatalogEntry]) -> dict[str, str]:
    """Build selector -> property_name mapping with collision handling."""
    names: dict[str, str] = {}
    seen_names: set[str] = set()
    for entry in entries:
        prop_name = _selector_to_property_name(
            entry.selector, entry.semantic_name or entry.label, entry.tag
        )
        if prop_name in seen_names:
            index = 2
            while f"{prop_name}_{index}" in seen_names:
                index += 1
            prop_name = f"{prop_name}_{index}"
        seen_names.add(prop_name)
        names[entry.selector] = prop_name
    return names


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


def _generate_python_component(component: SharedComponent) -> str:
    """Generate a Python shared component class."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry_names = _build_entry_property_names(component.entries)

    lines: list[str] = [
        '"""',
        f"Auto-generated Shared Component — {component.class_name}.",
        "",
        f"Component: {component.name}",
        f"Zone: {component.zone.value}",
        f"Generated: {timestamp}",
        '"""',
        "",
        "from playwright.sync_api import Locator, Page, expect",
        "",
        "",
        f"class {component.class_name}:",
        f'    """Reusable component: {component.name}."""',
        "",
        "    def __init__(self, page: Page) -> None:",
        "        self.page = page",
    ]

    for entry in component.entries:
        prop_name = entry_names[entry.selector]
        selector = entry.selector.replace('"', '\\"')
        lines.append(f'        self.{prop_name} = page.locator("{selector}")')
    lines.append("")

    if component.entries:
        first = entry_names[component.entries[0].selector]
        lines.extend(
            [
                "    def assert_visible(self) -> None:",
                f"        expect(self.{first}).to_be_visible()",
                "",
            ]
        )

    for entry in component.entries:
        prop_name = entry_names[entry.selector]
        if "input" in entry.element_type:
            lines.extend(
                [
                    f"    def fill_{prop_name}(self, value: str) -> None:",
                    f"        self.{prop_name}.fill(value)",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    f"    def click_{prop_name}(self) -> None:",
                    f"        self.{prop_name}.click()",
                    "",
                ]
            )

    return "\n".join(lines)


def _generate_typescript_component(component: SharedComponent) -> str:
    """Generate a TypeScript shared component class."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry_names = _build_entry_property_names(component.entries)

    lines: list[str] = [
        f"// Auto-generated Shared Component — {component.class_name}",
        f"// Component: {component.name}",
        f"// Zone: {component.zone.value}",
        f"// Generated: {timestamp}",
        "",
        "import { type Locator, type Page, expect } from '@playwright/test';",
        "",
        f"export class {component.class_name} {{",
    ]

    for entry in component.entries:
        lines.append(f"  readonly {entry_names[entry.selector]}: Locator;")
    lines.append("")

    lines.extend(
        [
            "  constructor(public readonly page: Page) {",
        ]
    )
    for entry in component.entries:
        prop_name = entry_names[entry.selector]
        selector = entry.selector.replace("'", "\\'")
        lines.append(f"    this.{prop_name} = page.locator('{selector}');")
    lines.append("  }")
    lines.append("")

    if component.entries:
        first = entry_names[component.entries[0].selector]
        lines.extend(
            [
                "  async assertVisible() {",
                f"    await expect(this.{first}).toBeVisible();",
                "  }",
                "",
            ]
        )

    for entry in component.entries:
        prop_name = entry_names[entry.selector]
        method_suffix = prop_name.title().replace("_", "")
        if "input" in entry.element_type:
            lines.extend(
                [
                    f"  async fill{method_suffix}(value: string) {{",
                    f"    await this.{prop_name}.fill(value);",
                    "  }",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    f"  async click{method_suffix}() {{",
                    f"    await this.{prop_name}.click();",
                    "  }",
                    "",
                ]
            )

    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _generate_python_pom(
    catalog: PageCatalog,
    class_name: str,
    base_url: str,
    *,
    page_components: list[SharedComponent] | None = None,
) -> str:
    """Generate a Python POM class."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    archetype = catalog.archetype.value if catalog.archetype else "unknown"
    url_pattern = catalog.url_pattern or "*"
    page_components = page_components or []

    imports = ["from playwright.sync_api import Locator, Page, expect"]
    for component in page_components:
        module_name = _to_snake_case(component.class_name)
        imports.append(
            f"from pages.components.{module_name} import {component.class_name}"
        )

    lines: list[str] = [
        '"""',
        f"Auto-generated Page Object Model — {class_name}.",
        "",
        f"Archetype: {archetype}",
        f"URL pattern: {url_pattern}",
        f"Generated: {timestamp}",
        '"""',
        "",
        *imports,
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

    if page_components:
        lines.append("        # Shared components")
        for component in page_components:
            prop_name = _to_snake_case(component.class_name)
            lines.append(f"        self.{prop_name} = {component.class_name}(page)")

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
                index = 2
                while f"{prop_name}_{index}" in seen_names:
                    index += 1
                prop_name = f"{prop_name}_{index}"
            seen_names.add(prop_name)

            selector = entry.selector.replace('"', '\\"')
            lines.append(f'        self.{prop_name} = page.locator("{selector}")')

    lines.append("")

    # Navigate method
    if base_url:
        lines.extend(
            [
                "    def navigate(self) -> None:",
                "        self.page.goto(self.URL)",
                '        self.page.wait_for_load_state("networkidle")',
                "",
            ]
        )

    # Search method if search zone exists
    if ZoneType.SEARCH in grouped:
        search_entries = grouped[ZoneType.SEARCH]
        input_entry = next(
            (entry for entry in search_entries if "input" in entry.element_type), None
        )
        if input_entry:
            selector = input_entry.selector.replace('"', '\\"')
            lines.extend(
                [
                    "    def search(self, query: str) -> None:",
                    f'        self.page.fill("{selector}", query)',
                    f'        self.page.press("{selector}", "Enter")',
                    "",
                ]
            )

    # Select item method if listing with content items
    if catalog.archetype == PageArchetype.LISTING and ZoneType.MAIN_CONTENT in grouped:
        content_entries = [
            entry
            for entry in grouped[ZoneType.MAIN_CONTENT]
            if entry.element_type in ("link", "button", "other")
        ]
        if content_entries:
            selector = content_entries[0].selector.replace('"', '\\"')
            lines.extend(
                [
                    "    def select_item(self, index: int = 0) -> None:",
                    f'        self.page.locator("{selector}").nth(index).click()',
                    "",
                ]
            )

    return "\n".join(lines)


def _generate_typescript_pom(
    catalog: PageCatalog,
    class_name: str,
    base_url: str,
    *,
    page_components: list[SharedComponent] | None = None,
) -> str:
    """Generate a TypeScript POM class."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    archetype = catalog.archetype.value if catalog.archetype else "unknown"
    url_pattern = catalog.url_pattern or "*"
    page_components = page_components or []

    lines: list[str] = [
        f"// Auto-generated Page Object Model — {class_name}",
        f"// Archetype: {archetype}",
        f"// URL pattern: {url_pattern}",
        f"// Generated: {timestamp}",
        "",
        "import { type Locator, type Page } from '@playwright/test';",
    ]
    for component in page_components:
        module_name = _to_kebab_case(component.class_name)
        lines.append(
            f"import {{ {component.class_name} }} from './components/{module_name}';"
        )
    lines.extend(
        [
            "",
            f"export class {class_name} {{",
        ]
    )

    if base_url:
        lines.append(f"  static readonly URL = '{base_url}';")
        lines.append("")

    for component in page_components:
        prop_name = _to_snake_case(component.class_name)
        lines.append(f"  readonly {prop_name}: {component.class_name};")

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
                index = 2
                while f"{prop_name}_{index}" in seen_names:
                    index += 1
                prop_name = f"{prop_name}_{index}"
            seen_names.add(prop_name)

            lines.append(f"  readonly {prop_name}: Locator;")

    lines.append("")

    # Constructor
    lines.append("  constructor(public readonly page: Page) {")
    for component in page_components:
        prop_name = _to_snake_case(component.class_name)
        lines.append(f"    this.{prop_name} = new {component.class_name}(page);")

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
                index = 2
                while f"{prop_name}_{index}" in seen_names_ctor:
                    index += 1
                prop_name = f"{prop_name}_{index}"
            seen_names_ctor.add(prop_name)

            selector = entry.selector.replace("'", "\\'")
            lines.append(f"    this.{prop_name} = page.locator('{selector}');")

    lines.append("  }")
    lines.append("")

    # Navigate
    if base_url:
        lines.extend(
            [
                "  async navigate() {",
                f"    await this.page.goto({class_name}.URL);",
                "    await this.page.waitForLoadState('networkidle');",
                "  }",
                "",
            ]
        )

    # Search
    if ZoneType.SEARCH in grouped:
        search_entries = grouped[ZoneType.SEARCH]
        input_entry = next(
            (entry for entry in search_entries if "input" in entry.element_type), None
        )
        if input_entry:
            selector = input_entry.selector.replace("'", "\\'")
            lines.extend(
                [
                    "  async search(query: string) {",
                    f"    await this.page.fill('{selector}', query);",
                    f"    await this.page.press('{selector}', 'Enter');",
                    "  }",
                    "",
                ]
            )

    # Select item
    if catalog.archetype == PageArchetype.LISTING and ZoneType.MAIN_CONTENT in grouped:
        content_entries = [
            entry
            for entry in grouped[ZoneType.MAIN_CONTENT]
            if entry.element_type in ("link", "button", "other")
        ]
        if content_entries:
            selector = content_entries[0].selector.replace("'", "\\'")
            lines.extend(
                [
                    "  async selectItem(index: number = 0) {",
                    f"    await this.page.locator('{selector}').nth(index).click();",
                    "  }",
                    "",
                ]
            )

    lines.append("}")
    lines.append("")

    return "\n".join(lines)

"""Shared naming and formatting primitives for code generation."""

from __future__ import annotations

import re

from flowscout.modeling.archetype import CatalogEntry, PageCatalog, ZoneType


def to_snake_case(name: str) -> str:
    """Convert PascalCase to snake_case."""
    result = re.sub(r"(?<!^)(?=[A-Z])", "_", name)
    return result.lower()


def to_kebab_case(name: str) -> str:
    """Convert PascalCase to kebab-case."""
    result = re.sub(r"(?<!^)(?=[A-Z])", "-", name)
    return result.lower()


def catalog_to_class_name(catalog: PageCatalog) -> str:
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


def selector_to_property_name(selector: str, label: str, tag: str) -> str:
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


def entry_locator(entry: CatalogEntry) -> str:
    """Return preferred selector when provided, else default CSS selector."""
    preferred = str(entry.preferred_selector or "").strip()
    return preferred or entry.selector


def group_by_zone(
    entries: list[CatalogEntry],
) -> dict[ZoneType, list[CatalogEntry]]:
    """Group catalog entries by zone."""
    zones: dict[ZoneType, list[CatalogEntry]] = {}
    for entry in entries:
        zones.setdefault(entry.zone_type, []).append(entry)
    return zones


def build_entry_property_names(
    entries: list[CatalogEntry],
) -> dict[str, str]:
    """Build selector -> property_name mapping with collision handling."""
    names: dict[str, str] = {}
    seen_names: set[str] = set()
    for entry in entries:
        prop_name = selector_to_property_name(
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


ZONE_LABELS: dict[ZoneType, str] = {
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

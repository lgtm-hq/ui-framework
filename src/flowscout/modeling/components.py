"""Shared component extraction for reusable cross-page UI blocks."""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Mapping

from pydantic import BaseModel, Field

from flowscout.core.archetypes import CatalogEntry, PageCatalog, ZoneType

_ZONE_COMPONENT_NAMES: dict[ZoneType, tuple[str, str]] = {
    ZoneType.NAVIGATION: ("NavigationBar", "NavigationComponent"),
    ZoneType.HEADER: ("HeaderArea", "HeaderComponent"),
    ZoneType.SEARCH: ("SearchPanel", "SearchComponent"),
    ZoneType.FILTER: ("FilterPanel", "FilterComponent"),
    ZoneType.SIDEBAR: ("SidebarArea", "SidebarComponent"),
    ZoneType.PAGINATION: ("PaginationControls", "PaginationComponent"),
    ZoneType.FOOTER: ("FooterArea", "FooterComponent"),
    ZoneType.FORM: ("FormSection", "FormComponent"),
    ZoneType.MAIN_CONTENT: ("SharedContent", "ContentComponent"),
}


class SharedComponent(BaseModel):
    """A reusable component observed across multiple page types."""

    component_id: str
    name: str
    class_name: str
    entries: list[CatalogEntry] = Field(default_factory=list)
    appears_on: list[str] = Field(default_factory=list)
    frequency: float = 0.0
    zone: ZoneType = ZoneType.MAIN_CONTENT


def extract_shared_components(
    *,
    page_catalogs: Mapping[str, PageCatalog],
    min_frequency: float = 0.6,
) -> list[SharedComponent]:
    """Extract zone-based shared components from page catalogs."""
    if not page_catalogs:
        return []

    normalized = {
        page_type_id: catalog
        for page_type_id, catalog in page_catalogs.items()
        if catalog.entries
    }
    if not normalized:
        return []

    total_pages = len(normalized)
    min_pages = max(1, math.ceil(total_pages * min_frequency))

    selector_pages: dict[tuple[ZoneType, str], set[str]] = defaultdict(set)
    representative_entries: dict[tuple[ZoneType, str], CatalogEntry] = {}
    for page_type_id, catalog in normalized.items():
        seen_on_page: set[tuple[ZoneType, str]] = set()
        for entry in catalog.entries:
            key = (entry.zone_type, entry.selector)
            if key in seen_on_page:
                continue
            seen_on_page.add(key)
            selector_pages[key].add(page_type_id)
            representative_entries.setdefault(key, entry)

    zone_entries: dict[ZoneType, list[CatalogEntry]] = defaultdict(list)
    zone_pages: dict[ZoneType, set[str]] = defaultdict(set)
    for key, pages in selector_pages.items():
        if len(pages) < min_pages:
            continue
        zone, _selector = key
        zone_entries[zone].append(representative_entries[key].model_copy(deep=True))
        zone_pages[zone].update(pages)

    components: list[SharedComponent] = []
    for zone in sorted(zone_entries, key=lambda value: value.value):
        entries = sorted(zone_entries[zone], key=lambda entry: entry.selector)
        appears_on = sorted(zone_pages[zone])
        frequency = len(appears_on) / total_pages
        if frequency < min_frequency:
            continue

        name, class_name = _ZONE_COMPONENT_NAMES.get(
            zone,
            (
                f"{zone.value.replace('_', ' ').title()} Area",
                f"{zone.value.replace('_', ' ').title().replace(' ', '')}Component",
            ),
        )
        components.append(
            SharedComponent(
                component_id=f"component-{zone.value}",
                name=name,
                class_name=class_name,
                entries=entries,
                appears_on=appears_on,
                frequency=round(frequency, 4),
                zone=zone,
            )
        )

    components.sort(
        key=lambda component: (-component.frequency, component.name.lower())
    )
    return components

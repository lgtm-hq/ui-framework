"""Builds POMSuite from PageCatalogs and SharedComponents."""

from __future__ import annotations

from typing import Any, Callable

from flowscout.codegen.pom_model import (
    MethodKind,
    POMClass,
    POMMethod,
    POMProperty,
    POMSuite,
    PropertyKind,
)
from flowscout.codegen.primitives import (
    ZONE_LABELS,
    build_entry_property_names,
    catalog_to_class_name,
    entry_locator,
    group_by_zone,
    selector_to_property_name,
    to_snake_case,
)
from flowscout.modeling.archetype import (
    CatalogEntry,
    PageArchetype,
    PageCatalog,
    ZoneType,
)
from flowscout.modeling.components import InteractionPattern, SharedComponent


def build_pom_suite(
    catalogs: dict[str, Any],
    *,
    base_url: str = "",
    shared_components: list[Any] | None = None,
) -> POMSuite:
    """Build a complete POMSuite from catalog data."""
    parsed_catalogs = [
        (signature, _parse_catalog(catalog_data))
        for signature, catalog_data in catalogs.items()
    ]
    parsed_components = [_parse_shared_component(c) for c in (shared_components or [])]
    parsed_components = [c for c in parsed_components if c.entries]

    if not parsed_components and not any(
        catalog.entries for _sig, catalog in parsed_catalogs
    ):
        return POMSuite()

    base_components, page_scoped_components = _partition_components(
        parsed_components=parsed_components,
    )
    page_component_map = _build_page_component_map(
        parsed_components=page_scoped_components,
    )

    base_page = _build_base_page(base_components=base_components)

    components = [_build_component_class(c) for c in parsed_components]

    pages: list[POMClass] = []
    for sig, catalog in parsed_catalogs:
        components_for_page = page_component_map.get(sig, [])
        all_components = [*base_components, *components_for_page]
        filtered_catalog = _strip_component_entries(
            catalog=catalog,
            components_for_page=all_components,
        )
        if not filtered_catalog.entries and not all_components:
            continue

        class_name = catalog_to_class_name(catalog)
        pages.append(
            build_page_class(
                catalog=filtered_catalog,
                class_name=class_name,
                base_url=base_url,
                page_components=components_for_page,
            )
        )

    return POMSuite(base_page=base_page, components=components, pages=pages)


def build_pom_suite_for_preview(
    page_types: list[Any],
    *,
    shared_components: list[Any] | None = None,
    base_url: str = "",
) -> dict[str, POMClass]:
    """Build per-page-type POMClass for report preview rendering.

    Returns mapping of page_type_id -> POMClass.
    """
    parsed_components = [_parse_shared_component(c) for c in (shared_components or [])]
    parsed_components = [c for c in parsed_components if c.entries]
    base_components, page_scoped_components = _partition_components(
        parsed_components=parsed_components,
    )
    page_component_map = _build_page_component_map(
        parsed_components=page_scoped_components,
    )

    result: dict[str, POMClass] = {}
    for page_type in page_types:
        if isinstance(page_type, dict):
            page_type_id = str(page_type.get("page_type_id", "")).strip()
            catalog_data = page_type.get("catalog", {})
        else:
            page_type_id = str(getattr(page_type, "page_type_id", "")).strip()
            catalog_data = getattr(page_type, "catalog", {})

        if not page_type_id:
            continue

        catalog = _parse_catalog(catalog_data)
        components_for_page = page_component_map.get(page_type_id, [])
        all_components = [*base_components, *components_for_page]
        filtered_catalog = _strip_component_entries(
            catalog=catalog,
            components_for_page=all_components,
        )
        if not filtered_catalog.entries and not all_components:
            continue

        class_name = catalog_to_class_name(catalog)
        result[page_type_id] = build_page_class(
            catalog=filtered_catalog,
            class_name=class_name,
            base_url=base_url,
            page_components=components_for_page,
        )

    return result


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Component partitioning
# ---------------------------------------------------------------------------


BASE_COMPONENT_FREQUENCY_THRESHOLD = 0.8


def _partition_components(
    *,
    parsed_components: list[SharedComponent],
) -> tuple[list[SharedComponent], list[SharedComponent]]:
    """Split components into base-level and page-scoped buckets."""
    base_components = [
        c
        for c in parsed_components
        if c.frequency >= BASE_COMPONENT_FREQUENCY_THRESHOLD
    ]
    page_scoped = [
        c
        for c in parsed_components
        if c.frequency < BASE_COMPONENT_FREQUENCY_THRESHOLD
    ]
    return base_components, page_scoped


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
            key=lambda c: c.class_name,
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


# ---------------------------------------------------------------------------
# POMClass builders
# ---------------------------------------------------------------------------


def _build_base_page(
    *,
    base_components: list[SharedComponent],
) -> POMClass:
    """Build POMClass for the BasePage."""
    properties: list[POMProperty] = []
    for component in base_components:
        prop_name = to_snake_case(component.class_name)
        properties.append(
            POMProperty(
                name=prop_name,
                selector="",
                kind=PropertyKind.COMPONENT,
                component_class_name=component.class_name,
            )
        )

    methods = [
        POMMethod(
            kind=MethodKind.NAVIGATE,
            name="navigate",
            parameters=[("path", "str")],
        ),
    ]

    return POMClass(
        class_name="BasePage",
        properties=properties,
        methods=methods,
    )


def _build_component_class(component: SharedComponent) -> POMClass:
    """Build POMClass for a shared component."""
    entry_names = build_entry_property_names(component.entries)

    properties: list[POMProperty] = []
    for entry in component.entries:
        prop_name = entry_names[entry.selector]
        properties.append(
            POMProperty(
                name=prop_name,
                selector=entry_locator(entry),
                element_type=entry.element_type,
            )
        )

    methods: list[POMMethod] = []

    # assert_visible on first property
    if component.entries:
        first_prop = entry_names[component.entries[0].selector]
        methods.append(
            POMMethod(
                kind=MethodKind.ASSERT_VISIBLE,
                name="assert_visible",
                target_property=first_prop,
            )
        )

    # Per-entry fill/click methods
    for entry in component.entries:
        prop_name = entry_names[entry.selector]
        if "input" in entry.element_type:
            methods.append(
                POMMethod(
                    kind=MethodKind.FILL,
                    name=f"fill_{prop_name}",
                    parameters=[("value", "str")],
                    target_property=prop_name,
                )
            )
        else:
            methods.append(
                POMMethod(
                    kind=MethodKind.CLICK,
                    name=f"click_{prop_name}",
                    target_property=prop_name,
                )
            )

    # Pattern methods
    methods.extend(_build_pattern_methods(component=component, entry_names=entry_names))

    return POMClass(
        class_name=component.class_name,
        properties=properties,
        methods=methods,
        is_component=True,
        component_name=component.name,
        component_zone=component.zone,
    )


def build_page_class(
    *,
    catalog: PageCatalog,
    class_name: str,
    base_url: str,
    page_components: list[SharedComponent] | None = None,
) -> POMClass:
    """Build POMClass for a page object."""
    page_components = page_components or []

    properties: list[POMProperty] = []

    # Component properties
    for component in page_components:
        prop_name = to_snake_case(component.class_name)
        properties.append(
            POMProperty(
                name=prop_name,
                selector="",
                kind=PropertyKind.COMPONENT,
                component_class_name=component.class_name,
            )
        )

    # Locator properties grouped by zone
    grouped = group_by_zone(catalog.entries)
    seen_names: set[str] = set()

    for zone_type in ZoneType:
        zone_entries = grouped.get(zone_type, [])
        if not zone_entries:
            continue

        zone_label = ZONE_LABELS.get(zone_type, zone_type.value)

        for entry in zone_entries:
            prop_name = selector_to_property_name(
                entry.selector, entry.semantic_name or entry.label, entry.tag
            )
            if prop_name in seen_names:
                index = 2
                while f"{prop_name}_{index}" in seen_names:
                    index += 1
                prop_name = f"{prop_name}_{index}"
            seen_names.add(prop_name)

            properties.append(
                POMProperty(
                    name=prop_name,
                    selector=entry_locator(entry),
                    zone=zone_type,
                    zone_label=zone_label,
                    element_type=entry.element_type,
                )
            )

    # Methods
    methods: list[POMMethod] = []

    if base_url:
        methods.append(
            POMMethod(
                kind=MethodKind.NAVIGATE,
                name="navigate",
            )
        )

    # Search method
    if ZoneType.SEARCH in grouped:
        search_entries = grouped[ZoneType.SEARCH]
        input_entry = next(
            (e for e in search_entries if "input" in e.element_type), None
        )
        if input_entry:
            methods.append(
                POMMethod(
                    kind=MethodKind.SEARCH,
                    name="search",
                    parameters=[("query", "str")],
                    selector=entry_locator(input_entry),
                )
            )

    # Select item method for listings
    if catalog.archetype == PageArchetype.LISTING and ZoneType.MAIN_CONTENT in grouped:
        content_entries = [
            e
            for e in grouped[ZoneType.MAIN_CONTENT]
            if e.element_type in ("link", "button", "other")
        ]
        if content_entries:
            methods.append(
                POMMethod(
                    kind=MethodKind.SELECT_ITEM,
                    name="select_item",
                    parameters=[("index", "int")],
                    selector=entry_locator(content_entries[0]),
                )
            )

    archetype = catalog.archetype if catalog.archetype else PageArchetype.UNKNOWN
    return POMClass(
        class_name=class_name,
        parent_class="BasePage",
        archetype=archetype,
        url_pattern=catalog.url_pattern or "",
        base_url=base_url,
        properties=properties,
        methods=methods,
    )


# ---------------------------------------------------------------------------
# Pattern method builders
# ---------------------------------------------------------------------------


def _find_component_prop_name(
    *,
    component: SharedComponent,
    entry_names: dict[str, str],
    predicate: Callable[[CatalogEntry], bool],
) -> str:
    """Find the first component property name matching a predicate."""
    for entry in component.entries:
        if predicate(entry):
            return entry_names[entry.selector]
    if component.entries:
        return entry_names[component.entries[0].selector]
    return ""


def _build_pattern_methods(
    *,
    component: SharedComponent,
    entry_names: dict[str, str],
) -> list[POMMethod]:
    """Build POMMethod list from detected interaction patterns."""
    methods: list[POMMethod] = []
    patterns = set(component.interaction_patterns)

    if InteractionPattern.DROPDOWN in patterns:
        trigger_prop = _find_component_prop_name(
            component=component,
            entry_names=entry_names,
            predicate=lambda entry: (
                "dropdown_trigger" in entry.element_type
                or entry.element_type in {"select", "combobox", "button"}
            ),
        )
        if trigger_prop:
            methods.extend(
                [
                    POMMethod(
                        kind=MethodKind.OPEN,
                        name="open",
                        target_property=trigger_prop,
                    ),
                    POMMethod(
                        kind=MethodKind.CLOSE,
                        name="close",
                    ),
                    POMMethod(
                        kind=MethodKind.SELECT_OPTION,
                        name="select",
                        parameters=[("value", "str")],
                    ),
                ]
            )

    if InteractionPattern.TABS in patterns:
        methods.append(
            POMMethod(
                kind=MethodKind.SWITCH_TAB,
                name="switch_to",
                parameters=[("tab_name", "str")],
            )
        )

    if InteractionPattern.SEARCH in patterns:
        search_prop = _find_component_prop_name(
            component=component,
            entry_names=entry_names,
            predicate=lambda entry: (
                "search" in entry.element_type or "search" in entry.label.lower()
            ),
        )
        if search_prop:
            methods.append(
                POMMethod(
                    kind=MethodKind.SEARCH,
                    name="search",
                    parameters=[("query", "str")],
                    target_property=search_prop,
                )
            )

    if InteractionPattern.FORM in patterns:
        methods.append(
            POMMethod(
                kind=MethodKind.FILL_AND_SUBMIT,
                name="fill_and_submit",
            )
        )

    if InteractionPattern.PAGINATION in patterns:
        methods.extend(
            [
                POMMethod(
                    kind=MethodKind.NEXT_PAGE,
                    name="next_page",
                ),
                POMMethod(
                    kind=MethodKind.PREVIOUS_PAGE,
                    name="previous_page",
                ),
            ]
        )

    if InteractionPattern.TOGGLE in patterns:
        methods.extend(
            [
                POMMethod(
                    kind=MethodKind.TOGGLE,
                    name="toggle",
                    parameters=[("name", "str")],
                ),
                POMMethod(
                    kind=MethodKind.IS_CHECKED,
                    name="is_checked",
                    parameters=[("name", "str")],
                ),
            ]
        )

    return methods

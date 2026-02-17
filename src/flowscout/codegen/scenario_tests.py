"""Test generation from site model scenarios — always uses POM classes."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flowscout.modeling.archetype import CatalogEntry, PageArchetype, ZoneType
from flowscout.modeling.site_model import SiteModel
from flowscout.modeling.flows import FlowTemplate
from flowscout.codegen.primitives import (
    catalog_to_class_name as _catalog_to_class_name,
    group_by_zone as _group_by_zone,
    selector_to_property_name as _selector_to_property_name,
    to_snake_case as _to_snake_case,
)
from flowscout.modeling.scenarios import FlowScenario


def generate_scenario_tests(
    site_model: SiteModel,
    output_path: str,
    *,
    framework: str = "pytest",
    base_url: str = "",
) -> str:
    """Generate test file from site model scenarios.

    POM classes must be generated first (via generate_page_objects).
    Generated tests import and use POM classes for all interactions.

    Args:
        site_model: The SiteModel with page_types, navigation_edges, scenarios.
        output_path: Path to write the generated test file.
        framework: "pytest" for Python or "playwright" for TypeScript.
        base_url: Base URL for navigation.

    Returns:
        Path to the generated test file.
    """
    # Build mapping: page_type_id → POM class name + module name
    pom_map = _build_pom_map(site_model)

    # Build mapping: page_type_id → PageType (for URLs)
    pt_map = {pt.page_type_id: pt for pt in site_model.page_types}

    if framework == "pytest":
        content = _generate_pytest(site_model, pom_map, pt_map, base_url)
    else:
        content = _generate_playwright_test(site_model, pom_map, pt_map, base_url)

    Path(output_path).write_text(content)
    return output_path


# ---------------------------------------------------------------------------
# POM mapping
# ---------------------------------------------------------------------------


class _PomInfo:
    """POM class metadata for a page type."""

    def __init__(self, class_name: str, module_name: str, var_name: str) -> None:
        self.class_name = class_name
        self.module_name = module_name
        self.var_name = var_name


def _build_pom_map(site_model: SiteModel) -> dict[str, _PomInfo]:
    """Map page_type_id → POM class info."""
    pom_map: dict[str, _PomInfo] = {}

    for pt in site_model.page_types:
        if not pt.catalog.entries:
            continue

        class_name = _catalog_to_class_name(pt.catalog)
        module_name = _to_snake_case(class_name)
        var_name = _to_var_name(class_name)
        pom_map[pt.page_type_id] = _PomInfo(class_name, module_name, var_name)

    return pom_map


def _to_var_name(class_name: str) -> str:
    """Convert PascalCase class name to a short variable name."""
    # MovieListingPage → listing, MovieDetailPage → detail
    # Remove "Page" suffix, take last meaningful word
    name = class_name.removesuffix("Page")
    words = re.findall(r"[A-Z][a-z]*", name)
    if words:
        return str(words[-1].lower())
    return str(_to_snake_case(name)).replace("_", "")


def _sanitize_test_name(text: str) -> str:
    """Convert text to a valid test function name."""
    clean = re.sub(r"[^\w\s]", "", text.lower())
    clean = re.sub(r"\s+", "_", clean.strip())
    clean = re.sub(r"_+", "_", clean).strip("_")
    return clean[:60]


def _to_ts_regex_literal(pattern: str) -> str:
    """Convert a regex pattern into a safe TypeScript regex literal body."""
    return pattern.replace("/", r"\/")


# ---------------------------------------------------------------------------
# Catalog → POM property mapping
# ---------------------------------------------------------------------------


def _catalog_property_map(
    catalog: Any,
) -> dict[ZoneType, list[tuple[CatalogEntry, str]]]:
    """Build ZoneType → [(CatalogEntry, property_name)] using the same
    deduplication logic as page_objects.py so property names match POM classes."""
    from flowscout.modeling.archetype import PageCatalog

    if isinstance(catalog, dict):
        catalog = PageCatalog.model_validate(catalog)
    if not hasattr(catalog, "entries") or not catalog.entries:
        return {}

    grouped = _group_by_zone(catalog.entries)
    result: dict[ZoneType, list[tuple[CatalogEntry, str]]] = {}
    seen_names: set[str] = set()

    # Iterate in the same ZoneType order as page_objects._generate_python_pom
    for zone_type in ZoneType:
        zone_entries = grouped.get(zone_type, [])
        if not zone_entries:
            continue
        zone_list: list[tuple[CatalogEntry, str]] = []
        for entry in zone_entries:
            prop_name = _selector_to_property_name(
                entry.selector,
                entry.semantic_name or entry.label,
                entry.tag,
            )
            if prop_name in seen_names:
                i = 2
                while f"{prop_name}_{i}" in seen_names:
                    i += 1
                prop_name = f"{prop_name}_{i}"
            seen_names.add(prop_name)
            zone_list.append((entry, prop_name))
        result[zone_type] = zone_list

    return result


def _find_pom_property(
    prop_map: dict[ZoneType, list[tuple[CatalogEntry, str]]],
    zone_type: ZoneType,
    element_type_prefix: str | None = None,
) -> str | None:
    """Find the first POM property name for a zone and element type."""
    entries = prop_map.get(zone_type, [])
    for entry, prop_name in entries:
        if element_type_prefix is None:
            return prop_name
        if entry.element_type.startswith(element_type_prefix):
            return prop_name
    return None


# ---------------------------------------------------------------------------
# Pytest assertion emission
# ---------------------------------------------------------------------------


def _emit_pytest_verification(
    lines: list[str],
    template: str,
    pom: _PomInfo | None,
    pt: Any,
    prop_map: dict[ZoneType, list[tuple[CatalogEntry, str]]],
    indent: str = "        ",
) -> None:
    """Emit real pytest assertions based on scenario template and page archetype."""
    var = pom.var_name if pom else None
    archetype = pt.archetype if pt and hasattr(pt, "archetype") else None
    url_pattern = pt.url_pattern if pt and hasattr(pt, "url_pattern") else None

    if template == "load_verify":
        # Title assertion always
        lines.append(f'{indent}expect(page).to_have_title(re.compile(r".+"))')

        if archetype == PageArchetype.LISTING:
            prop = _find_pom_property(prop_map, ZoneType.MAIN_CONTENT)
            if prop and var:
                lines.append(f"{indent}expect({var}.{prop}.first).to_be_visible()")
                return
        elif archetype == PageArchetype.DETAIL:
            prop = _find_pom_property(prop_map, ZoneType.HEADER) or _find_pom_property(
                prop_map,
                ZoneType.MAIN_CONTENT,
            )
            if prop and var:
                lines.append(f"{indent}expect({var}.{prop}).to_be_visible()")
                return
        elif archetype == PageArchetype.FORM:
            prop = _find_pom_property(prop_map, ZoneType.FORM, "input")
            if prop and var:
                lines.append(f"{indent}expect({var}.{prop}).to_be_visible()")
                return
        elif archetype == PageArchetype.SEARCH_RESULTS:
            prop = _find_pom_property(prop_map, ZoneType.SEARCH, "input")
            if prop and var:
                lines.append(f"{indent}expect({var}.{prop}).to_be_visible()")
                return

        # Fallback: URL assertion or comment
        if url_pattern and var:
            pattern = url_pattern.replace("\\", "\\\\")
            lines.append(f'{indent}expect(page).to_have_url(re.compile(r"{pattern}"))')
        else:
            lines.append(f"{indent}# Verify: page content loaded")

    elif template == "browse_detail":
        if url_pattern and var:
            pattern = url_pattern.replace("\\", "\\\\")
            lines.append(f'{indent}expect(page).to_have_url(re.compile(r"{pattern}"))')
        prop = _find_pom_property(
            prop_map, ZoneType.MAIN_CONTENT
        ) or _find_pom_property(prop_map, ZoneType.HEADER)
        if prop and var:
            lines.append(f"{indent}expect({var}.{prop}).to_be_visible()")
        elif not url_pattern:
            lines.append(f"{indent}# Verify: detail content is visible")

    elif template == "search":
        prop = _find_pom_property(prop_map, ZoneType.MAIN_CONTENT)
        if prop and var:
            lines.append(f"{indent}expect({var}.{prop}.first).to_be_visible()")
        elif url_pattern and var:
            pattern = url_pattern.replace("\\", "\\\\")
            lines.append(f'{indent}expect(page).to_have_url(re.compile(r"{pattern}"))')
        else:
            lines.append(f"{indent}# Verify: search results are displayed")

    elif template == "pagination":
        prop = _find_pom_property(prop_map, ZoneType.MAIN_CONTENT)
        if prop and var:
            lines.append(f"{indent}expect({var}.{prop}.first).to_be_visible()")
        if url_pattern and var:
            pattern = url_pattern.replace("\\", "\\\\")
            lines.append(f'{indent}expect(page).to_have_url(re.compile(r"{pattern}"))')
        if not prop and not url_pattern:
            lines.append(f"{indent}# Verify: content has changed")

    elif template == "filter":
        prop = _find_pom_property(prop_map, ZoneType.MAIN_CONTENT)
        if prop and var:
            lines.append(f"{indent}expect({var}.{prop}.first).to_be_visible()")
        elif url_pattern and var:
            pattern = url_pattern.replace("\\", "\\\\")
            lines.append(f'{indent}expect(page).to_have_url(re.compile(r"{pattern}"))')
        else:
            lines.append(f"{indent}# Verify: filtered content is displayed")

    elif template == "form_submit":
        if url_pattern and var:
            pattern = url_pattern.replace("\\", "\\\\")
            lines.append(f'{indent}expect(page).to_have_url(re.compile(r"{pattern}"))')
        else:
            lines.append(f"{indent}# Verify: form submitted successfully")

    elif template == "round_trip":
        if url_pattern and var:
            pattern = url_pattern.replace("\\", "\\\\")
            lines.append(f'{indent}expect(page).to_have_url(re.compile(r"{pattern}"))')
        else:
            lines.append(f"{indent}# Verify: returned to original page")

    else:
        # Unknown template — fall back
        if url_pattern and var:
            pattern = url_pattern.replace("\\", "\\\\")
            lines.append(f'{indent}expect(page).to_have_url(re.compile(r"{pattern}"))')
        else:
            lines.append(f"{indent}# Verify: expected outcome")


# ---------------------------------------------------------------------------
# TypeScript assertion emission
# ---------------------------------------------------------------------------


def _emit_ts_verification(
    lines: list[str],
    template: str,
    pom: _PomInfo | None,
    pt: Any,
    prop_map: dict[ZoneType, list[tuple[CatalogEntry, str]]],
    indent: str = "    ",
) -> None:
    """Emit real TypeScript assertions based on scenario template and page archetype."""
    var = pom.var_name if pom else None
    archetype = pt.archetype if pt and hasattr(pt, "archetype") else None
    url_pattern = pt.url_pattern if pt and hasattr(pt, "url_pattern") else None

    if template == "load_verify":
        lines.append(f"{indent}await expect(page).toHaveTitle(/.+/);")

        if archetype == PageArchetype.LISTING:
            prop = _find_pom_property(prop_map, ZoneType.MAIN_CONTENT)
            if prop and var:
                lines.append(
                    f"{indent}await expect({var}.{prop}.first()).toBeVisible();"
                )
                return
        elif archetype == PageArchetype.DETAIL:
            prop = _find_pom_property(prop_map, ZoneType.HEADER) or _find_pom_property(
                prop_map,
                ZoneType.MAIN_CONTENT,
            )
            if prop and var:
                lines.append(f"{indent}await expect({var}.{prop}).toBeVisible();")
                return
        elif archetype == PageArchetype.FORM:
            prop = _find_pom_property(prop_map, ZoneType.FORM, "input")
            if prop and var:
                lines.append(f"{indent}await expect({var}.{prop}).toBeVisible();")
                return
        elif archetype == PageArchetype.SEARCH_RESULTS:
            prop = _find_pom_property(prop_map, ZoneType.SEARCH, "input")
            if prop and var:
                lines.append(f"{indent}await expect({var}.{prop}).toBeVisible();")
                return

        if url_pattern and var:
            pattern = _to_ts_regex_literal(url_pattern)
            lines.append(f"{indent}await expect(page).toHaveURL(/{pattern}/);")
        else:
            lines.append(f"{indent}// Verify: page content loaded")

    elif template == "browse_detail":
        if url_pattern and var:
            pattern = _to_ts_regex_literal(url_pattern)
            lines.append(f"{indent}await expect(page).toHaveURL(/{pattern}/);")
        prop = _find_pom_property(
            prop_map, ZoneType.MAIN_CONTENT
        ) or _find_pom_property(prop_map, ZoneType.HEADER)
        if prop and var:
            lines.append(f"{indent}await expect({var}.{prop}).toBeVisible();")
        elif not url_pattern:
            lines.append(f"{indent}// Verify: detail content is visible")

    elif template == "search":
        prop = _find_pom_property(prop_map, ZoneType.MAIN_CONTENT)
        if prop and var:
            lines.append(f"{indent}await expect({var}.{prop}.first()).toBeVisible();")
        elif url_pattern and var:
            pattern = _to_ts_regex_literal(url_pattern)
            lines.append(f"{indent}await expect(page).toHaveURL(/{pattern}/);")
        else:
            lines.append(f"{indent}// Verify: search results are displayed")

    elif template == "pagination":
        prop = _find_pom_property(prop_map, ZoneType.MAIN_CONTENT)
        if prop and var:
            lines.append(f"{indent}await expect({var}.{prop}.first()).toBeVisible();")
        if url_pattern and var:
            pattern = _to_ts_regex_literal(url_pattern)
            lines.append(f"{indent}await expect(page).toHaveURL(/{pattern}/);")
        if not prop and not url_pattern:
            lines.append(f"{indent}// Verify: content has changed")

    elif template == "filter":
        prop = _find_pom_property(prop_map, ZoneType.MAIN_CONTENT)
        if prop and var:
            lines.append(f"{indent}await expect({var}.{prop}.first()).toBeVisible();")
        elif url_pattern and var:
            pattern = _to_ts_regex_literal(url_pattern)
            lines.append(f"{indent}await expect(page).toHaveURL(/{pattern}/);")
        else:
            lines.append(f"{indent}// Verify: filtered content is displayed")

    elif template == "form_submit":
        if url_pattern and var:
            pattern = _to_ts_regex_literal(url_pattern)
            lines.append(f"{indent}await expect(page).toHaveURL(/{pattern}/);")
        else:
            lines.append(f"{indent}// Verify: form submitted successfully")

    elif template == "round_trip":
        if url_pattern and var:
            pattern = _to_ts_regex_literal(url_pattern)
            lines.append(f"{indent}await expect(page).toHaveURL(/{pattern}/);")
        else:
            lines.append(f"{indent}// Verify: returned to original page")

    else:
        if url_pattern and var:
            pattern = _to_ts_regex_literal(url_pattern)
            lines.append(f"{indent}await expect(page).toHaveURL(/{pattern}/);")
        else:
            lines.append(f"{indent}// Verify: expected outcome")


# ---------------------------------------------------------------------------
# Pytest generation
# ---------------------------------------------------------------------------


def _generate_pytest(
    site_model: SiteModel,
    pom_map: dict[str, _PomInfo],
    pt_map: dict[str, Any],
    base_url: str,
) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = [
        '"""Scenario-based tests generated by Flowscout site model.',
        "",
        f"Generated: {timestamp}",
        f"Base URL: {base_url}",
        '"""',
        "",
        "import re",
        "",
        "import pytest",
        "from playwright.sync_api import Page, expect",
        "",
    ]

    # Import POM classes
    imported: set[str] = set()
    for pom in pom_map.values():
        if pom.class_name not in imported:
            lines.append(f"from pages.{pom.module_name} import {pom.class_name}")
            imported.add(pom.class_name)

    if imported:
        lines.append("")
        lines.append("")

    # Group scenarios by priority for ordering
    priority_order = {"critical": 0, "important": 1, "nice-to-have": 2}
    sorted_scenarios = sorted(
        site_model.test_scenarios,
        key=lambda s: priority_order.get(
            (
                s.priority
                if isinstance(s, FlowScenario)
                else s.get("priority", "important")
            ),
            1,
        ),
    )

    # Group scenarios by template for class organization
    template_groups: dict[str, list[Any]] = {}
    for scenario in sorted_scenarios:
        if isinstance(scenario, FlowScenario):
            template = scenario.template or "general"
        else:
            template = scenario.get("template", "general")
        template_groups.setdefault(template, []).append(scenario)

    flow_template_lookup = _build_flow_template_lookup(site_model.flow_templates)

    used_names: set[str] = set()

    for template, scenarios in template_groups.items():
        class_name = "".join(w.capitalize() for w in template.split("_")) + "Tests"
        lines.append(f"class Test{class_name}:")
        lines.append(f'    """Tests from {template} template."""')
        lines.append("")

        for scenario in scenarios:
            sc = (
                scenario
                if isinstance(scenario, FlowScenario)
                else FlowScenario.model_validate(scenario)
            )

            func_name = _sanitize_test_name(sc.name)
            if func_name in used_names:
                func_name = f"{func_name}_{sc.scenario_id.split('-')[-1]}"
            used_names.add(func_name)

            variant_rows = _select_parametric_variants(
                scenario=sc,
                template=flow_template_lookup.get(tuple(sc.page_type_sequence)),
            )
            if variant_rows:
                values = [
                    {"url": row["url"], "content_id": row["content_id"]}
                    for row in variant_rows
                ]
                ids = [row["content_id"] for row in variant_rows]
                lines.append(
                    f"    @pytest.mark.parametrize('variant', {values!r}, ids={ids!r})"
                )
                lines.append(
                    f"    def test_{func_name}("
                    "self, page: Page, variant: dict[str, str]"
                    ") -> None:"
                )
            else:
                lines.append(f"    def test_{func_name}(self, page: Page) -> None:")
            lines.append(f'        """{sc.description}')
            lines.append("")
            lines.append(f"        Priority: {sc.priority}")
            if sc.tags:
                lines.append(f"        Tags: {', '.join(sc.tags)}")
            lines.append('        """')

            # Generate step code
            _generate_pytest_steps(
                lines,
                sc,
                pom_map,
                pt_map,
                base_url,
                variant_variable="variant" if variant_rows else None,
            )
            if variant_rows:
                lines.append("        assert variant['content_id']")

            lines.append("")

        lines.append("")

    return "\n".join(lines)


def _build_flow_template_lookup(
    flow_templates: list[FlowTemplate],
) -> dict[tuple[str, ...], FlowTemplate]:
    """Map page-type sequences to flow templates."""
    lookup: dict[tuple[str, ...], FlowTemplate] = {}
    for template in flow_templates:
        key = tuple(template.page_type_sequence)
        if key and key not in lookup:
            lookup[key] = template
    return lookup


def _select_parametric_variants(
    *,
    scenario: FlowScenario,
    template: FlowTemplate | None,
) -> list[dict[str, str]]:
    """Return parametrization rows when scenario has meaningful data variants."""
    if template is None:
        return []
    if len(scenario.page_type_sequence) < 2:
        return []
    if len(template.data_variants) < 2:
        return []

    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for variant in template.data_variants:
        url = str(variant.url or "").strip()
        if not url:
            continue
        content_id = str(variant.content_id or "").strip() or "variant"
        key = (url, content_id)
        if key in seen:
            continue
        seen.add(key)
        rows.append({"url": url, "content_id": content_id})
    return rows


def _generate_pytest_steps(
    lines: list[str],
    scenario: FlowScenario,
    pom_map: dict[str, _PomInfo],
    pt_map: dict[str, Any],
    base_url: str,
    variant_variable: str | None = None,
) -> None:
    """Generate pytest step code for a scenario."""
    instantiated: set[str] = set()
    used_variant_navigation = False

    # Pre-compute property maps for all page types referenced by this scenario
    prop_maps: dict[str, dict[ZoneType, list[tuple[CatalogEntry, str]]]] = {}
    for step in scenario.steps:
        pt = pt_map.get(step.page_type)
        if pt and hasattr(pt, "catalog") and step.page_type not in prop_maps:
            prop_maps[step.page_type] = _catalog_property_map(pt.catalog)

    template = scenario.template or "general"

    for step in scenario.steps:
        pom = pom_map.get(step.page_type)
        pt = pt_map.get(step.page_type)

        if step.action_type == "navigate" and pom:
            # Instantiate POM and navigate
            if pom.var_name not in instantiated:
                lines.append(f"        {pom.var_name} = {pom.class_name}(page)")
                instantiated.add(pom.var_name)
            if variant_variable and not used_variant_navigation:
                lines.append(f"        page.goto({variant_variable}['url'])")
                used_variant_navigation = True
            else:
                lines.append(f"        {pom.var_name}.navigate()")

        elif step.action_type == "fill" and step.target_selector:
            # Fill input — use POM search method if it's a search step
            if pom and "search" in step.action_description.lower():
                if pom.var_name not in instantiated:
                    lines.append(f"        {pom.var_name} = {pom.class_name}(page)")
                    instantiated.add(pom.var_name)
                value = step.input_value or "test query"
                lines.append(f'        {pom.var_name}.search("{value}")')
            else:
                sel = step.target_selector.replace('"', '\\"')
                value = step.input_value or "test input"
                lines.append(f'        page.fill("{sel}", "{value}")')

        elif step.action_type == "click" and pom:
            if pom.var_name not in instantiated:
                lines.append(f"        {pom.var_name} = {pom.class_name}(page)")
                instantiated.add(pom.var_name)

            if step.target_selector:
                sel = step.target_selector.replace('"', '\\"')
                lines.append(f'        page.click("{sel}")')
            elif (
                "item" in step.action_description.lower()
                or "detail" in step.action_description.lower()
            ):
                lines.append(f"        {pom.var_name}.select_item(0)")
            else:
                lines.append(f"        # {step.action_description}")

        elif step.action_type == "submit_form":
            lines.append("        # Submit form (press Enter or click submit button)")
            lines.append('        page.keyboard.press("Enter")')

        elif step.action_type is None and step.expected_outcome:
            # Verification step — ensure POM is instantiated if needed
            if pom and pom.var_name not in instantiated:
                lines.append(f"        {pom.var_name} = {pom.class_name}(page)")
                instantiated.add(pom.var_name)
            prop_map = prop_maps.get(step.page_type, {})
            _emit_pytest_verification(
                lines,
                template,
                pom,
                pt,
                prop_map,
                indent="        ",
            )
        else:
            lines.append(f"        # {step.action_description}")


# ---------------------------------------------------------------------------
# Playwright Test (TypeScript) generation
# ---------------------------------------------------------------------------


def _generate_playwright_test(
    site_model: SiteModel,
    pom_map: dict[str, _PomInfo],
    pt_map: dict[str, Any],
    base_url: str,
) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = [
        "// Scenario-based tests generated by Flowscout site model",
        f"// Generated: {timestamp}",
        f"// Base URL: {base_url}",
        "",
        "import { test, expect } from '@playwright/test';",
        "",
    ]

    # Import POM classes
    imported: set[str] = set()
    for pom in pom_map.values():
        if pom.class_name not in imported:
            kebab = re.sub(r"(?<!^)(?=[A-Z])", "-", pom.class_name).lower()
            lines.append(f"import {{ {pom.class_name} }} from './pages/{kebab}';")
            imported.add(pom.class_name)

    if imported:
        lines.append("")

    # Group scenarios
    priority_order = {"critical": 0, "important": 1, "nice-to-have": 2}
    sorted_scenarios = sorted(
        site_model.test_scenarios,
        key=lambda s: priority_order.get(
            (
                s.priority
                if isinstance(s, FlowScenario)
                else s.get("priority", "important")
            ),
            1,
        ),
    )

    template_groups: dict[str, list[Any]] = {}
    for scenario in sorted_scenarios:
        if isinstance(scenario, FlowScenario):
            template = scenario.template or "general"
        else:
            template = scenario.get("template", "general")
        template_groups.setdefault(template, []).append(scenario)

    for template, scenarios in template_groups.items():
        lines.append(f"test.describe('{template}', () => {{")
        lines.append("")

        for scenario in scenarios:
            sc = (
                scenario
                if isinstance(scenario, FlowScenario)
                else FlowScenario.model_validate(scenario)
            )

            lines.append(f"  test('{sc.name}', async ({{ page }}) => {{")
            _generate_ts_steps(lines, sc, pom_map, pt_map, base_url)
            lines.append("  });")
            lines.append("")

        lines.append("});")
        lines.append("")

    return "\n".join(lines)


def _generate_ts_steps(
    lines: list[str],
    scenario: FlowScenario,
    pom_map: dict[str, _PomInfo],
    pt_map: dict[str, Any],
    base_url: str,
) -> None:
    """Generate TypeScript step code."""
    instantiated: set[str] = set()

    # Pre-compute property maps for all page types referenced by this scenario
    prop_maps: dict[str, dict[ZoneType, list[tuple[CatalogEntry, str]]]] = {}
    for step in scenario.steps:
        pt = pt_map.get(step.page_type)
        if pt and hasattr(pt, "catalog") and step.page_type not in prop_maps:
            prop_maps[step.page_type] = _catalog_property_map(pt.catalog)

    template = scenario.template or "general"

    for step in scenario.steps:
        pom = pom_map.get(step.page_type)
        pt = pt_map.get(step.page_type)

        if step.action_type == "navigate" and pom:
            if pom.var_name not in instantiated:
                lines.append(f"    const {pom.var_name} = new {pom.class_name}(page);")
                instantiated.add(pom.var_name)
            lines.append(f"    await {pom.var_name}.navigate();")

        elif step.action_type == "fill" and step.target_selector:
            if pom and "search" in step.action_description.lower():
                if pom.var_name not in instantiated:
                    lines.append(
                        f"    const {pom.var_name} = new {pom.class_name}(page);"
                    )
                    instantiated.add(pom.var_name)
                value = step.input_value or "test query"
                lines.append(f"    await {pom.var_name}.search('{value}');")
            else:
                sel = step.target_selector.replace("'", "\\'")
                value = step.input_value or "test input"
                lines.append(f"    await page.fill('{sel}', '{value}');")

        elif step.action_type == "click" and pom:
            if pom.var_name not in instantiated:
                lines.append(f"    const {pom.var_name} = new {pom.class_name}(page);")
                instantiated.add(pom.var_name)
            if step.target_selector:
                sel = step.target_selector.replace("'", "\\'")
                lines.append(f"    await page.click('{sel}');")
            elif (
                "item" in step.action_description.lower()
                or "detail" in step.action_description.lower()
            ):
                lines.append(f"    await {pom.var_name}.selectItem(0);")
            else:
                lines.append(f"    // {step.action_description}")

        elif step.action_type == "submit_form":
            lines.append("    await page.keyboard.press('Enter');")

        elif step.action_type is None and step.expected_outcome:
            # Verification step — ensure POM is instantiated if needed
            if pom and pom.var_name not in instantiated:
                lines.append(f"    const {pom.var_name} = new {pom.class_name}(page);")
                instantiated.add(pom.var_name)
            prop_map = prop_maps.get(step.page_type, {})
            _emit_ts_verification(
                lines,
                template,
                pom,
                pt,
                prop_map,
                indent="    ",
            )
        else:
            lines.append(f"    // {step.action_description}")

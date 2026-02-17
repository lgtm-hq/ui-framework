"""Playwright Python (pytest) POM adapter."""

from __future__ import annotations

from datetime import datetime, timezone

from flowscout.codegen.adapters.base import POMAdapter
from flowscout.codegen.pom_model import (
    MethodKind,
    POMClass,
    POMMethod,
    PropertyKind,
)
from flowscout.codegen.primitives import to_snake_case


class PlaywrightPythonAdapter(POMAdapter):
    """Renders POM models as Python Playwright sync API classes."""

    def file_extension(self) -> str:
        return ".py"

    def base_page_filename(self) -> str:
        return "base_page.py"

    def class_to_filename(self, class_name: str) -> str:
        return to_snake_case(class_name) + ".py"

    # ------------------------------------------------------------------
    # Render methods
    # ------------------------------------------------------------------

    def render_base_page(self, pom_class: POMClass) -> str:
        """Render a Python BasePage class."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        imports = ["from playwright.sync_api import Page"]
        for prop in pom_class.properties:
            if prop.kind == PropertyKind.COMPONENT:
                module = to_snake_case(prop.component_class_name)
                imports.append(
                    f"from pages.components.{module} import {prop.component_class_name}"
                )

        lines: list[str] = [
            '"""',
            "Auto-generated Base Page Object.",
            "",
            f"Generated: {timestamp}",
            '"""',
            "",
            *imports,
            "",
            "",
            "class BasePage:",
            '    """Base page with shared components and navigation helpers."""',
            "",
            "    def __init__(self, page: Page) -> None:",
            "        self.page = page",
        ]

        component_props = [
            p for p in pom_class.properties if p.kind == PropertyKind.COMPONENT
        ]
        if component_props:
            lines.append("        # High-frequency shared components")
            for prop in component_props:
                lines.append(
                    f"        self.{prop.name} = {prop.component_class_name}(page)"
                )

        lines.extend(
            [
                "",
                "    def navigate(self, path: str) -> None:",
                "        self.page.goto(path)",
                '        self.page.wait_for_load_state("networkidle")',
                "",
            ]
        )
        return "\n".join(lines)

    def render_component(self, pom_class: POMClass) -> str:
        """Render a Python shared component class."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines: list[str] = [
            '"""',
            f"Auto-generated Shared Component — {pom_class.class_name}.",
            "",
            f"Component: {pom_class.component_name}",
            f"Zone: {pom_class.component_zone.value}",
            f"Generated: {timestamp}",
            '"""',
            "",
            "from playwright.sync_api import Locator, Page, expect",
            "",
            "",
            f"class {pom_class.class_name}:",
            f'    """Reusable component: {pom_class.component_name}."""',
            "",
            "    def __init__(self, page: Page) -> None:",
            "        self.page = page",
        ]

        for prop in pom_class.properties:
            selector = prop.selector.replace('"', '\\"')
            lines.append(f'        self.{prop.name} = page.locator("{selector}")')
        lines.append("")

        for method in pom_class.methods:
            lines.extend(self._render_method(method))

        return "\n".join(lines)

    def render_page(self, pom_class: POMClass) -> str:
        """Render a Python page object class."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        archetype = pom_class.archetype.value if pom_class.archetype else "unknown"
        url_pattern = pom_class.url_pattern or "*"
        has_base = bool(pom_class.parent_class)

        imports = ["from playwright.sync_api import Locator, Page, expect"]
        if has_base:
            imports.append("from pages.base_page import BasePage")
        for prop in pom_class.properties:
            if prop.kind == PropertyKind.COMPONENT:
                module = to_snake_case(prop.component_class_name)
                imports.append(
                    f"from pages.components.{module} import {prop.component_class_name}"
                )

        class_def = (
            f"class {pom_class.class_name}(BasePage):"
            if has_base
            else f"class {pom_class.class_name}:"
        )

        lines: list[str] = [
            '"""',
            f"Auto-generated Page Object Model — {pom_class.class_name}.",
            "",
            f"Archetype: {archetype}",
            f"URL pattern: {url_pattern}",
            f"Generated: {timestamp}",
            '"""',
            "",
            *imports,
            "",
            "",
            class_def,
            f'    """Page object for: {archetype} page.',
            f"    URL pattern: {url_pattern}",
            '    """',
            "",
        ]

        if pom_class.base_url:
            lines.append(f'    URL = "{pom_class.base_url}"')
            lines.append("")

        # Constructor
        lines.append("    def __init__(self, page: Page) -> None:")
        if has_base:
            lines.append("        super().__init__(page)")
        else:
            lines.append("        self.page = page")

        # Component properties
        component_props = [
            p for p in pom_class.properties if p.kind == PropertyKind.COMPONENT
        ]
        if component_props:
            lines.append("        # Shared components")
            for prop in component_props:
                lines.append(
                    f"        self.{prop.name} = {prop.component_class_name}(page)"
                )

        # Locator properties grouped by zone
        current_zone_label = ""
        for prop in pom_class.properties:
            if prop.kind != PropertyKind.LOCATOR:
                continue
            if prop.zone_label and prop.zone_label != current_zone_label:
                current_zone_label = prop.zone_label
                lines.append(f"        # {current_zone_label}")
            selector = prop.selector.replace('"', '\\"')
            lines.append(f'        self.{prop.name} = page.locator("{selector}")')

        lines.append("")

        # Methods
        for method in pom_class.methods:
            lines.extend(self._render_page_method(method, pom_class=pom_class))

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Method rendering
    # ------------------------------------------------------------------

    def _render_method(self, method: POMMethod) -> list[str]:
        """Render a component method."""
        match method.kind:
            case MethodKind.ASSERT_VISIBLE:
                return [
                    "    def assert_visible(self) -> None:",
                    f"        expect(self.{method.target_property}).to_be_visible()",
                    "",
                ]
            case MethodKind.FILL:
                return [
                    f"    def {method.name}(self, value: str) -> None:",
                    f"        self.{method.target_property}.fill(value)",
                    "",
                ]
            case MethodKind.CLICK:
                return [
                    f"    def {method.name}(self) -> None:",
                    f"        self.{method.target_property}.click()",
                    "",
                ]
            case MethodKind.OPEN:
                return [
                    "    def open(self) -> None:",
                    f"        self.{method.target_property}.click()",
                    "",
                ]
            case MethodKind.CLOSE:
                return [
                    "    def close(self) -> None:",
                    "        self.page.keyboard.press('Escape')",
                    "",
                ]
            case MethodKind.SELECT_OPTION:
                return [
                    "    def select(self, value: str) -> None:",
                    "        self.open()",
                    "        self.page.get_by_role('option', name=value).click()",
                    "",
                ]
            case MethodKind.SWITCH_TAB:
                return [
                    "    def switch_to(self, tab_name: str) -> None:",
                    "        self.page.get_by_role('tab', name=tab_name).click()",
                    "",
                ]
            case MethodKind.SEARCH:
                return [
                    "    def search(self, query: str) -> None:",
                    f"        self.{method.target_property}.fill(query)",
                    f"        self.{method.target_property}.press('Enter')",
                    "",
                ]
            case MethodKind.FILL_AND_SUBMIT:
                return [
                    "    def fill_and_submit(self, **fields: str) -> None:",
                    "        for name, value in fields.items():",
                    "            self.page.locator(f\"[name='{name}']\").fill(value)",
                    "        submit_selector = (",
                    "            \"button[type='submit'], input[type='submit']\"",
                    "        )",
                    "        self.page.locator(submit_selector).first.click()",
                    "",
                ]
            case MethodKind.NEXT_PAGE:
                return [
                    "    def next_page(self) -> None:",
                    "        self.page.get_by_role('link', name='Next').first.click()",
                    "",
                ]
            case MethodKind.PREVIOUS_PAGE:
                return [
                    "    def previous_page(self) -> None:",
                    "        self.page.get_by_role("
                    "'link', name='Previous'"
                    ").first.click()",
                    "",
                ]
            case MethodKind.TOGGLE:
                return [
                    "    def toggle(self, name: str) -> None:",
                    "        self.page.locator(f\"[name='{name}']\").click()",
                    "",
                ]
            case MethodKind.IS_CHECKED:
                return [
                    "    def is_checked(self, name: str) -> bool:",
                    "        toggle_locator = self.page.locator(f\"[name='{name}']\")",
                    "        return bool(toggle_locator.is_checked())",
                    "",
                ]
            case _:
                return []

    def _render_page_method(
        self,
        method: POMMethod,
        *,
        pom_class: POMClass,
    ) -> list[str]:
        """Render a page-level method."""
        has_base = bool(pom_class.parent_class)

        match method.kind:
            case MethodKind.NAVIGATE:
                lines = [
                    "    def navigate(self) -> None:",
                    (
                        "        super().navigate(self.URL)"
                        if has_base
                        else "        self.page.goto(self.URL)"
                    ),
                ]
                if not has_base:
                    lines.append('        self.page.wait_for_load_state("networkidle")')
                lines.append("")
                return lines
            case MethodKind.SEARCH:
                selector = method.selector.replace('"', '\\"')
                return [
                    "    def search(self, query: str) -> None:",
                    f'        self.page.fill("{selector}", query)',
                    f'        self.page.press("{selector}", "Enter")',
                    "",
                ]
            case MethodKind.SELECT_ITEM:
                selector = method.selector.replace('"', '\\"')
                return [
                    "    def select_item(self, index: int = 0) -> None:",
                    f'        self.page.locator("{selector}").nth(index).click()',
                    "",
                ]
            case _:
                return []

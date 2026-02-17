"""Playwright TypeScript POM adapter."""

from __future__ import annotations

from datetime import datetime, timezone

from flowscout.codegen.adapters.base import POMAdapter
from flowscout.codegen.pom_model import (
    MethodKind,
    POMClass,
    POMMethod,
    PropertyKind,
)
from flowscout.codegen.primitives import to_kebab_case


class PlaywrightTSAdapter(POMAdapter):
    """Renders POM models as TypeScript Playwright test classes."""

    def file_extension(self) -> str:
        return ".ts"

    def base_page_filename(self) -> str:
        return "base-page.ts"

    def class_to_filename(self, class_name: str) -> str:
        return to_kebab_case(class_name) + ".ts"

    # ------------------------------------------------------------------
    # Render methods
    # ------------------------------------------------------------------

    def render_base_page(self, pom_class: POMClass) -> str:
        """Render a TypeScript BasePage class."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines: list[str] = [
            "// Auto-generated Base Page Object.",
            f"// Generated: {timestamp}",
            "",
            "import { type Page } from '@playwright/test';",
        ]
        for prop in pom_class.properties:
            if prop.kind == PropertyKind.COMPONENT:
                module = to_kebab_case(prop.component_class_name)
                lines.append(
                    f"import {{ {prop.component_class_name} }}"
                    f" from './components/{module}';"
                )

        lines.extend(["", "export class BasePage {"])

        component_props = [
            p for p in pom_class.properties if p.kind == PropertyKind.COMPONENT
        ]
        for prop in component_props:
            lines.append(f"  readonly {prop.name}: {prop.component_class_name};")

        lines.extend(
            [
                "",
                "  constructor(public readonly page: Page) {",
            ]
        )
        for prop in component_props:
            lines.append(
                f"    this.{prop.name} = new {prop.component_class_name}(page);"
            )

        lines.extend(
            [
                "  }",
                "",
                "  async navigate(path: string) {",
                "    await this.page.goto(path);",
                "    await this.page.waitForLoadState('networkidle');",
                "  }",
                "}",
                "",
            ]
        )
        return "\n".join(lines)

    def render_component(self, pom_class: POMClass) -> str:
        """Render a TypeScript shared component class."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines: list[str] = [
            f"// Auto-generated Shared Component — {pom_class.class_name}",
            f"// Component: {pom_class.component_name}",
            f"// Zone: {pom_class.component_zone.value}",
            f"// Generated: {timestamp}",
            "",
            "import { type Locator, type Page, expect } from '@playwright/test';",
            "",
            f"export class {pom_class.class_name} {{",
        ]

        for prop in pom_class.properties:
            lines.append(f"  readonly {prop.name}: Locator;")
        lines.append("")

        lines.append("  constructor(public readonly page: Page) {")
        for prop in pom_class.properties:
            selector = prop.selector.replace("'", "\\'")
            lines.append(f"    this.{prop.name} = page.locator('{selector}');")
        lines.append("  }")
        lines.append("")

        for method in pom_class.methods:
            lines.extend(self._render_method(method))

        lines.append("}")
        lines.append("")
        return "\n".join(lines)

    def render_page(self, pom_class: POMClass) -> str:
        """Render a TypeScript page object class."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        archetype = pom_class.archetype.value if pom_class.archetype else "unknown"
        url_pattern = pom_class.url_pattern or "*"
        has_base = bool(pom_class.parent_class)

        lines: list[str] = [
            f"// Auto-generated Page Object Model — {pom_class.class_name}",
            f"// Archetype: {archetype}",
            f"// URL pattern: {url_pattern}",
            f"// Generated: {timestamp}",
            "",
            "import { type Locator, type Page } from '@playwright/test';",
        ]
        if has_base:
            lines.append("import { BasePage } from './base-page';")
        for prop in pom_class.properties:
            if prop.kind == PropertyKind.COMPONENT:
                module = to_kebab_case(prop.component_class_name)
                lines.append(
                    f"import {{ {prop.component_class_name} }}"
                    f" from './components/{module}';"
                )

        class_def = (
            f"export class {pom_class.class_name} extends BasePage {{"
            if has_base
            else f"export class {pom_class.class_name} {{"
        )
        lines.extend(["", class_def])

        if pom_class.base_url:
            lines.append(f"  static readonly URL = '{pom_class.base_url}';")
            lines.append("")

        # Component property declarations
        for prop in pom_class.properties:
            if prop.kind == PropertyKind.COMPONENT:
                lines.append(f"  readonly {prop.name}: {prop.component_class_name};")

        # Locator property declarations
        current_zone_label = ""
        for prop in pom_class.properties:
            if prop.kind != PropertyKind.LOCATOR:
                continue
            if prop.zone_label and prop.zone_label != current_zone_label:
                current_zone_label = prop.zone_label
                lines.append(f"  // {current_zone_label}")
            lines.append(f"  readonly {prop.name}: Locator;")

        lines.append("")

        # Constructor
        lines.append("  constructor(public readonly page: Page) {")
        if has_base:
            lines.append("    super(page);")

        for prop in pom_class.properties:
            if prop.kind == PropertyKind.COMPONENT:
                lines.append(
                    f"    this.{prop.name} = new {prop.component_class_name}(page);"
                )

        for prop in pom_class.properties:
            if prop.kind != PropertyKind.LOCATOR:
                continue
            selector = prop.selector.replace("'", "\\'")
            lines.append(f"    this.{prop.name} = page.locator('{selector}');")

        lines.append("  }")
        lines.append("")

        # Methods
        for method in pom_class.methods:
            lines.extend(self._render_page_method(method, pom_class=pom_class))

        lines.append("}")
        lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Method rendering
    # ------------------------------------------------------------------

    def _render_method(
        self,
        method: POMMethod,
    ) -> list[str]:
        """Render a component method."""
        match method.kind:
            case MethodKind.ASSERT_VISIBLE:
                return [
                    "  async assertVisible() {",
                    f"    await expect(this.{method.target_property}).toBeVisible();",
                    "  }",
                    "",
                ]
            case MethodKind.FILL:
                prop = method.target_property
                method_suffix = prop.title().replace("_", "")
                return [
                    f"  async fill{method_suffix}(value: string) {{",
                    f"    await this.{prop}.fill(value);",
                    "  }",
                    "",
                ]
            case MethodKind.CLICK:
                prop = method.target_property
                method_suffix = prop.title().replace("_", "")
                return [
                    f"  async click{method_suffix}() {{",
                    f"    await this.{prop}.click();",
                    "  }",
                    "",
                ]
            case MethodKind.OPEN:
                return [
                    "  async open() {",
                    f"    await this.{method.target_property}.click();",
                    "  }",
                    "",
                ]
            case MethodKind.CLOSE:
                return [
                    "  async close() {",
                    "    await this.page.keyboard.press('Escape');",
                    "  }",
                    "",
                ]
            case MethodKind.SELECT_OPTION:
                return [
                    "  async select(value: string) {",
                    "    await this.open();",
                    "    await this.page.getByRole('option', { name: value }).click();",
                    "  }",
                    "",
                ]
            case MethodKind.SWITCH_TAB:
                return [
                    "  async switchTo(tabName: string) {",
                    "    await this.page.getByRole('tab', { name: tabName }).click();",
                    "  }",
                    "",
                ]
            case MethodKind.SEARCH:
                return [
                    "  async search(query: string) {",
                    f"    await this.{method.target_property}.fill(query);",
                    f"    await this.{method.target_property}.press('Enter');",
                    "  }",
                    "",
                ]
            case MethodKind.FILL_AND_SUBMIT:
                return [
                    "  async fillAndSubmit(fields: Record<string, string>) {",
                    "    for (const [name, value] of Object.entries(fields)) {",
                    "      await this.page.locator(`[name='${name}']`).fill(value);",
                    "    }",
                    "    await this.page",
                    "      .locator(\"button[type='submit'], input[type='submit']\")",
                    "      .first()",
                    "      .click();",
                    "  }",
                    "",
                ]
            case MethodKind.NEXT_PAGE:
                return [
                    "  async nextPage() {",
                    "    const nextLink = this.page"
                    ".getByRole('link', { name: 'Next' });",
                    "    await nextLink.first().click();",
                    "  }",
                    "",
                ]
            case MethodKind.PREVIOUS_PAGE:
                return [
                    "  async previousPage() {",
                    "    const previousLink = this.page.getByRole(",
                    "      'link',",
                    "      { name: 'Previous' },",
                    "    );",
                    "    await previousLink.first().click();",
                    "  }",
                    "",
                ]
            case MethodKind.TOGGLE:
                return [
                    "  async toggle(name: string) {",
                    "    await this.page.locator(`[name='${name}']`).click();",
                    "  }",
                    "",
                ]
            case MethodKind.IS_CHECKED:
                return [
                    "  async isChecked(name: string) {",
                    "    return await this.page"
                    ".locator(`[name='${name}']`)"
                    ".isChecked();",
                    "  }",
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
                    "  async navigate() {",
                    (
                        f"    await super.navigate({pom_class.class_name}.URL);"
                        if has_base
                        else f"    await this.page.goto({pom_class.class_name}.URL);"
                    ),
                ]
                if not has_base:
                    lines.append("    await this.page.waitForLoadState('networkidle');")
                lines.extend(["  }", ""])
                return lines
            case MethodKind.SEARCH:
                selector = method.selector.replace("'", "\\'")
                return [
                    "  async search(query: string) {",
                    f"    await this.page.fill('{selector}', query);",
                    f"    await this.page.press('{selector}', 'Enter');",
                    "  }",
                    "",
                ]
            case MethodKind.SELECT_ITEM:
                selector = method.selector.replace("'", "\\'")
                return [
                    "  async selectItem(index: number = 0) {",
                    f"    await this.page.locator('{selector}').nth(index).click();",
                    "  }",
                    "",
                ]
            case _:
                return []

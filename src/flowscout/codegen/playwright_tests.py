"""Generate executable Playwright test scripts from discovered flows."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType


def generate_test_suite(
    result: ExplorationResult,
    output_path: str,
    *,
    framework: str = "pytest",
) -> str:
    """Generate a complete test suite from exploration results.

    Args:
        result: The exploration result to generate tests from.
        output_path: Where to write the test file.
        framework: Test framework — "pytest" (default) or "playwright".

    Returns:
        Path to the generated test file.
    """
    if framework == "pytest":
        content = _generate_pytest_suite(result)
    else:
        content = _generate_playwright_suite(result)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return str(path)


def _generate_pytest_suite(result: ExplorationResult) -> str:
    """Generate a pytest + playwright test suite."""
    _used_names.clear()
    start_url = result.config.get("start_url", "https://example.com")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = [
        '"""',
        "Auto-generated Playwright tests from flowscout exploration.",
        "",
        f"Source: {start_url}",
        f"Generated: {timestamp}",
        f"States discovered: {len(result.states)}",
        f"Flows identified: {len(result.flows)}",
        "",
        "These tests replay the discovered navigation flows and verify",
        "that each action produces the expected outcome.",
        '"""',
        "",
        "import re",
        "",
        "import pytest",
        "from playwright.sync_api import Page, expect",
        "",
        "",
        f'BASE_URL = "{start_url}"',
        "",
        "",
    ]

    # Generate a test for each flow
    for flow in result.flows:
        test_func = _generate_flow_test(flow, result, start_url)
        lines.extend(test_func)
        lines.append("")

    # Generate individual action tests for actions that had interesting outcomes
    nav_results = [r for r in result.results if r.outcome == OutcomeType.NAVIGATION]
    seen_actions: set[str] = set()
    for r in nav_results:
        action = result.actions.get(r.action_id)
        if not action or action.action_id in seen_actions:
            continue
        seen_actions.add(action.action_id)
        test_func = _generate_action_test(action, r, result, start_url)
        lines.extend(test_func)
        lines.append("")

    # Generate negative tests for actions that timed out or errored
    error_results = [
        r
        for r in result.results
        if r.outcome in (OutcomeType.TIMEOUT, OutcomeType.EXCEPTION)
    ]
    seen_errors: set[str] = set()
    for r in error_results:
        action = result.actions.get(r.action_id)
        if not action or action.action_id in seen_errors:
            continue
        seen_errors.add(action.action_id)
        test_func = _generate_negative_test(action, r, result, start_url)
        lines.extend(test_func)
        lines.append("")

    return "\n".join(lines)


def _generate_flow_test(
    flow: Flow,
    result: ExplorationResult,
    start_url: str,
) -> list[str]:
    """Generate a test function for a single flow."""
    func_name = _to_test_name(flow.name, flow.description)
    lines: list[str] = []

    # Docstring
    lines.append(f"def {func_name}(page: Page) -> None:")
    lines.append(f'    """Flow: {flow.name}')
    lines.append("")
    lines.append(f"    {flow.description}")
    if flow.is_cycle:
        lines.append(f"    Type: Cycle ({flow.depth} steps)")
    else:
        lines.append(f"    Type: Linear ({flow.depth} steps)")
    lines.append('    """')

    # Navigate to start
    lines.append(f'    page.goto("{start_url}")')

    # Replay each step
    for i, action_id in enumerate(flow.action_ids):
        action = result.actions.get(action_id)
        if not action:
            continue

        # Find the corresponding result for this step
        expected_outcome = flow.outcomes[i] if i < len(flow.outcomes) else None
        matching_result = _find_result_for_step(
            action_id,
            flow.state_ids[i] if i < len(flow.state_ids) else "",
            result,
        )

        lines.append("")
        lines.append(f"    # Step {i + 1}: {action.label}")

        # Verdict comment
        if matching_result and matching_result.verdict:
            lines.append(
                f"    # Expected: {matching_result.expected or 'N/A'} | Actual: {matching_result.actual or 'N/A'} | Verdict: {matching_result.verdict.upper()}"
            )

        # Visibility check before interaction
        if action.action_type in (
            ActionType.CLICK,
            ActionType.FILL,
            ActionType.CHECK,
            ActionType.UNCHECK,
        ):
            sel_escaped = action.target_selector.replace('"', '\\"')
            lines.append(f'    expect(page.locator("{sel_escaped}")).to_be_visible()')

        # Generate the action
        action_lines = _action_to_playwright(action)
        for line in action_lines:
            lines.append(f"    {line}")

        # Wait for load after navigation actions
        if expected_outcome == OutcomeType.NAVIGATION:
            lines.append('    page.wait_for_load_state("networkidle")')

        # Generate the assertion
        if expected_outcome == OutcomeType.NAVIGATION and matching_result:
            lines.append(
                f'    expect(page).to_have_url(re.compile(r".*{_url_pattern(matching_result.url_after)}"))'
            )
        elif expected_outcome == OutcomeType.DOM_CHANGE:
            lines.append("    # Verify DOM changed (page content updated)")
            # If we know the target state, assert on its title
            target_sid = (
                flow.state_ids[i + 1] if (i + 1) < len(flow.state_ids) else None
            )
            if target_sid and target_sid in result.states:
                target_state = result.states[target_sid]
                if target_state.title:
                    lines.append(
                        f'    expect(page).to_have_title(re.compile(r".*{re.escape(target_state.title)}.*"))'
                    )

    lines.append("")
    return lines


def _generate_action_test(
    action: Action,
    r: ActionResult,
    result: ExplorationResult,
    start_url: str,
) -> list[str]:
    """Generate a test for a single successful navigation action."""
    func_name = _to_test_name("nav", action.label)
    source_state = result.states.get(r.source_state_id)
    target_state = result.states.get(r.target_state_id)

    lines = [
        f"def {func_name}(page: Page) -> None:",
        f'    """Verify: {action.label}',
        "",
        f"    From: {source_state.url if source_state else 'unknown'}",
        f"    To: {target_state.url if target_state else 'unknown'}",
        f"    Expected: {r.outcome.value}",
        '    """',
    ]

    # Navigate to source state
    nav_url = source_state.url if source_state else start_url
    lines.append(f'    page.goto("{nav_url}")')
    lines.append('    page.wait_for_load_state("networkidle")')
    lines.append("")

    # Verdict comment
    if r.verdict:
        lines.append(
            f"    # Expected: {r.expected or 'N/A'} | Actual: {r.actual or 'N/A'} | Verdict: {r.verdict.upper()}"
        )

    # Visibility check
    if action.action_type in (
        ActionType.CLICK,
        ActionType.FILL,
        ActionType.CHECK,
        ActionType.UNCHECK,
    ):
        sel_escaped = action.target_selector.replace('"', '\\"')
        lines.append(f'    expect(page.locator("{sel_escaped}")).to_be_visible()')

    # Perform action
    action_lines = _action_to_playwright(action)
    for line in action_lines:
        lines.append(f"    {line}")

    # Assert outcome
    if r.outcome == OutcomeType.NAVIGATION and target_state:
        lines.append("")
        lines.append(
            f'    expect(page).to_have_url(re.compile(r".*{_url_pattern(target_state.url)}"))'
        )
        if target_state.title:
            lines.append(
                f'    expect(page).to_have_title(re.compile(r".*{re.escape(target_state.title)}.*"))'
            )

    lines.append("")
    return lines


def _generate_negative_test(
    action: Action,
    r: ActionResult,
    result: ExplorationResult,
    start_url: str,
) -> list[str]:
    """Generate a test documenting an action that failed/timed out.

    These are marked as xfail — they document known issues.
    """
    func_name = _to_test_name("fail", action.label)
    source_state = result.states.get(r.source_state_id)

    lines = [
        f'@pytest.mark.xfail(reason="Element not interactable — {r.outcome.value}")',
        f"def {func_name}(page: Page) -> None:",
        f'    """Known issue: {action.label}',
        "",
        f"    Outcome: {r.outcome.value}",
        f"    {r.message[:100] if r.message else 'Element may be hidden or not clickable'}",
        '    """',
    ]

    nav_url = source_state.url if source_state else start_url
    lines.append(f'    page.goto("{nav_url}")')
    lines.append("")

    action_lines = _action_to_playwright(action, timeout=3000)
    for line in action_lines:
        lines.append(f"    {line}")

    lines.append("")
    return lines


def _action_to_playwright(action: Action, *, timeout: int = 5000) -> list[str]:
    """Convert an Action to Playwright API calls."""
    sel = action.target_selector.replace('"', '\\"')
    lines: list[str] = []

    match action.action_type:
        case ActionType.CLICK:
            if "requires_open" in action.metadata:
                trigger = action.metadata["requires_open"].replace('"', '\\"')
                lines.append(f'page.click("{trigger}", timeout={timeout})')
                lines.append("page.wait_for_timeout(300)")
            lines.append(f'page.click("{sel}", timeout={timeout})')

        case ActionType.FILL:
            value = (action.value or "").replace('"', '\\"')
            lines.append(f'page.fill("{sel}", "{value}", timeout={timeout})')

        case ActionType.SELECT_OPTION:
            value = (action.value or "").replace('"', '\\"')
            lines.append(f'page.select_option("{sel}", "{value}", timeout={timeout})')

        case ActionType.CHECK:
            lines.append(f'page.check("{sel}", timeout={timeout})')

        case ActionType.UNCHECK:
            lines.append(f'page.uncheck("{sel}", timeout={timeout})')

        case ActionType.PRESS_KEY:
            key = (action.value or "").replace('"', '\\"')
            lines.append(f'page.keyboard.press("{key}")')

        case ActionType.SUBMIT_FORM:
            field_values = json.loads(action.metadata.get("field_values_json", "{}"))
            for field_sel, value in field_values.items():
                escaped_sel = field_sel.replace('"', '\\"')
                escaped_val = value.replace('"', '\\"')
                lines.append(
                    f'page.fill("{escaped_sel}", "{escaped_val}", timeout={timeout})'
                )
            lines.append(f'page.click("{sel}", timeout={timeout})')

        case ActionType.HOVER:
            lines.append(f'page.hover("{sel}", timeout={timeout})')

        case ActionType.NAVIGATE:
            url = (action.value or "").replace('"', '\\"')
            lines.append(f'page.goto("{url}")')

    return lines


def _generate_playwright_suite(result: ExplorationResult) -> str:
    """Generate a Playwright Test (JS/TS style) suite."""
    start_url = result.config.get("start_url", "https://example.com")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "// Auto-generated Playwright tests from flowscout exploration",
        f"// Source: {start_url}",
        f"// Generated: {timestamp}",
        "",
        "import { test, expect } from '@playwright/test';",
        "",
        f"const BASE_URL = '{start_url}';",
        "",
    ]

    for flow in result.flows:
        test_name = flow.name.replace("'", "\\'")
        desc = flow.description[:50].replace("'", "\\'")
        lines.append(f"test.describe('{test_name}', () => {{")
        lines.append(f"  test('{desc}', async ({{ page }}) => {{")
        lines.append("    await page.goto(BASE_URL);")
        lines.append("    await page.waitForLoadState('networkidle');")

        for i, action_id in enumerate(flow.action_ids):
            action = result.actions.get(action_id)
            if not action:
                continue

            matching_result = _find_result_for_step(
                action_id,
                flow.state_ids[i] if i < len(flow.state_ids) else "",
                result,
            )

            lines.append("")
            lines.append(f"    // Step {i + 1}: {action.label}")

            # Verdict comment
            if matching_result and matching_result.verdict:
                lines.append(
                    f"    // Expected: {matching_result.expected or 'N/A'} | Actual: {matching_result.actual or 'N/A'} | Verdict: {matching_result.verdict.upper()}"
                )

            sel = action.target_selector.replace("'", "\\'")

            # Visibility check
            if action.action_type in (
                ActionType.CLICK,
                ActionType.FILL,
                ActionType.CHECK,
                ActionType.UNCHECK,
            ):
                lines.append(f"    await expect(page.locator('{sel}')).toBeVisible();")

            match action.action_type:
                case ActionType.CLICK:
                    lines.append(f"    await page.click('{sel}');")
                case ActionType.FILL:
                    val = (action.value or "").replace("'", "\\'")
                    lines.append(f"    await page.fill('{sel}', '{val}');")
                case ActionType.SELECT_OPTION:
                    val = (action.value or "").replace("'", "\\'")
                    lines.append(f"    await page.selectOption('{sel}', '{val}');")
                case ActionType.CHECK:
                    lines.append(f"    await page.check('{sel}');")
                case ActionType.UNCHECK:
                    lines.append(f"    await page.uncheck('{sel}');")
                case ActionType.SUBMIT_FORM:
                    field_values = json.loads(
                        action.metadata.get("field_values_json", "{}")
                    )
                    for field_sel, value in field_values.items():
                        fs = field_sel.replace("'", "\\'")
                        fv = value.replace("'", "\\'")
                        lines.append(f"    await page.fill('{fs}', '{fv}');")
                    lines.append(f"    await page.click('{sel}');")
                case ActionType.HOVER:
                    lines.append(f"    await page.hover('{sel}');")
                case ActionType.NAVIGATE:
                    url = (action.value or "").replace("'", "\\'")
                    lines.append(f"    await page.goto('{url}');")
                case _:
                    lines.append(f"    // TODO: Implement {action.action_type.value}")

            # Add assertion for navigation
            expected_outcome = flow.outcomes[i] if i < len(flow.outcomes) else None
            if expected_outcome == OutcomeType.NAVIGATION:
                lines.append("    await page.waitForLoadState('networkidle');")
                if matching_result:
                    lines.append(
                        f"    await expect(page).toHaveURL(/{_url_pattern(matching_result.url_after)}/);"
                    )

            # Invalid scenario assertion
            if (
                action.metadata.get("scenario") == "invalid"
                and expected_outcome == OutcomeType.VALIDATION_ERROR
            ):
                lines.append(
                    "    await expect(page.locator('.error, .validation-error, [aria-invalid=\"true\"]')).toBeVisible();"
                )

        lines.append("  });")
        lines.append("});")
        lines.append("")

    return "\n".join(lines)


def _find_result_for_step(
    action_id: str,
    source_state_id: str,
    result: ExplorationResult,
) -> ActionResult | None:
    """Find the ActionResult for a specific action from a specific state."""
    for r in result.results:
        if r.action_id == action_id and r.source_state_id == source_state_id:
            return r
    # Fallback: any result for this action
    for r in result.results:
        if r.action_id == action_id:
            return r
    return None


_used_names: set[str] = set()


def _to_test_name(prefix: str, text: str) -> str:
    """Convert a label to a valid Python test function name."""
    # Combine prefix and text, sanitize together
    raw = f"{prefix}_{text}".lower()
    # Remove special chars, convert spaces/arrows to underscores
    clean = re.sub(r"[^\w\s]", "", raw)
    clean = re.sub(r"\s+", "_", clean.strip())
    clean = re.sub(r"_+", "_", clean)
    # Truncate
    if len(clean) > 60:
        clean = clean[:60].rstrip("_")
    name = f"test_{clean}"
    # Deduplicate
    if name in _used_names:
        i = 2
        while f"{name}_{i}" in _used_names:
            i += 1
        name = f"{name}_{i}"
    _used_names.add(name)
    return name


def _url_pattern(url: str) -> str:
    """Extract a regex-friendly URL pattern from a full URL."""
    # Strip protocol and domain, keep path
    if "://" in url:
        path = url.split("://", 1)[1].split("/", 1)
        if len(path) > 1:
            return re.escape("/" + path[1])
    return re.escape(url)

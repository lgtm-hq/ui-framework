"""Tests for BrowserManager and StabilityWaiter."""

from __future__ import annotations

import json
import time
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from flowscout.core.browser import BrowserManager, StabilityWaiter
from flowscout.core.state import ExplorerConfig
from flowscout.discovery.actions import Action, ActionType, OutcomeType

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _config(**overrides: Any) -> ExplorerConfig:
    defaults = {
        "start_url": "https://example.com",
        "headless": True,
    }
    defaults.update(overrides)
    return ExplorerConfig(**defaults)


def _mock_page(
    *,
    url: str = "https://example.com",
    title: str = "Example",
    dom_skeleton: str = "<html></html>",
    visible_text: str = "Hello",
    form_state: str = "{}",
    signals: dict[str, Any] | None = None,
) -> MagicMock:
    """Build a mock Playwright Page."""
    page = MagicMock()
    page.url = url

    async def _title():
        return title

    page.title = _title

    eval_returns = {
        "dom_structure": dom_skeleton,
        "visible_text": visible_text,
        "form_state": form_state,
        "signals": signals or {},
        "page_analysis": {},
    }

    async def _evaluate(script, *args, **kwargs):
        # Return based on which script is being run (we match by identity)
        for key, value in eval_returns.items():
            if key in str(id(script)):
                return value
        return dom_skeleton

    page.evaluate = AsyncMock(side_effect=_evaluate)
    page.wait_for_load_state = AsyncMock()
    page.goto = AsyncMock()
    page.click = AsyncMock()
    page.fill = AsyncMock()
    page.select_option = AsyncMock()
    page.check = AsyncMock()
    page.uncheck = AsyncMock()
    page.hover = AsyncMock()
    page.press = AsyncMock()
    page.screenshot = AsyncMock()
    page.on = MagicMock()
    page.remove_listener = MagicMock()

    keyboard = MagicMock()
    keyboard.press = AsyncMock()
    page.keyboard = keyboard

    locator_mock = MagicMock()
    locator_mock.fill = AsyncMock()
    locator_mock.click = AsyncMock()
    locator_mock.first = locator_mock
    locator_mock.wait_for = AsyncMock()
    locator_mock.is_visible = AsyncMock(return_value=False)
    page.locator = MagicMock(return_value=locator_mock)

    accessibility = MagicMock()
    accessibility.snapshot = AsyncMock(return_value=None)
    page.accessibility = accessibility

    return page


def _make_action(
    action_type: ActionType = ActionType.CLICK,
    selector: str = "button#submit",
    value: str | None = None,
    metadata: dict[str, str] | None = None,
) -> Action:
    return Action(
        action_id="act-test",
        action_type=action_type,
        target_selector=selector,
        label="Test Action",
        value=value,
        metadata=metadata or {},
    )


# ---------------------------------------------------------------------------
# StabilityWaiter tests
# ---------------------------------------------------------------------------


class TestStabilityWaiter:
    """Tests for the extracted StabilityWaiter."""

    @pytest.mark.asyncio
    async def test_returns_immediately_when_dom_stable(self):
        """DOM doesn't change between polls → returns quickly."""
        waiter = StabilityWaiter(poll_interval_s=0.01)
        call_count = 0

        async def constant_hash():
            nonlocal call_count
            call_count += 1
            return "stable_hash"

        start = time.monotonic()
        await waiter.wait(constant_hash, timeout_ms=5000)
        elapsed = time.monotonic() - start

        assert elapsed < 1.0
        assert call_count == 2  # initial + one poll

    @pytest.mark.asyncio
    async def test_waits_until_stabilized(self):
        """DOM changes a few times then stabilizes."""
        waiter = StabilityWaiter(poll_interval_s=0.01)
        hashes = iter(["h1", "h2", "h3", "h3"])

        async def changing_hash():
            return next(hashes, "h3")

        await waiter.wait(changing_hash, timeout_ms=5000)
        # Should complete without timeout

    @pytest.mark.asyncio
    async def test_timeout_when_dom_keeps_changing(self):
        """DOM never stabilizes → exits after timeout."""
        waiter = StabilityWaiter(poll_interval_s=0.01)
        counter = 0

        async def always_changing():
            nonlocal counter
            counter += 1
            return f"hash_{counter}"

        start = time.monotonic()
        await waiter.wait(always_changing, timeout_ms=100)
        elapsed = time.monotonic() - start

        # Should complete around 100ms, not hang
        assert elapsed < 1.0

    @pytest.mark.asyncio
    async def test_configurable_poll_interval(self):
        """Poll interval affects wait behavior."""
        waiter = StabilityWaiter(poll_interval_s=0.05)
        call_count = 0

        async def stable_hash():
            nonlocal call_count
            call_count += 1
            return "stable"

        await waiter.wait(stable_hash, timeout_ms=5000)
        assert call_count == 2


# ---------------------------------------------------------------------------
# BrowserManager constructor tests
# ---------------------------------------------------------------------------


class TestBrowserManagerInit:
    """Tests for BrowserManager initialization."""

    def test_default_detector_created(self) -> None:
        bm = BrowserManager(_config())
        assert bm._detector is not None

    def test_custom_detector_injected(self) -> None:
        detector = MagicMock()
        bm = BrowserManager(_config(), detector=detector)
        assert bm._detector is detector

    def test_custom_stability_waiter_injected(self) -> None:
        waiter = StabilityWaiter(poll_interval_s=0.5)
        bm = BrowserManager(_config(), stability_waiter=waiter)
        assert bm._stability_waiter is waiter
        assert bm._stability_waiter.poll_interval_s == 0.5

    def test_page_raises_before_launch(self) -> None:
        bm = BrowserManager(_config())
        with pytest.raises(RuntimeError, match="Browser not launched"):
            _ = bm.page


# ---------------------------------------------------------------------------
# BrowserManager.execute_action tests
# ---------------------------------------------------------------------------


class TestExecuteAction:
    """Tests for action execution paths."""

    @pytest.mark.asyncio
    async def test_click_action(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page

        # Make evaluate return consistent hashes for stability/dom_hash
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NO_CHANGE)

        action = _make_action(ActionType.CLICK, "button#go")
        result = await bm.execute_action(action)

        page.click.assert_called_once_with(
            "button#go", timeout=bm.config.action_timeout_ms
        )
        assert result.outcome == OutcomeType.NO_CHANGE

    @pytest.mark.asyncio
    async def test_fill_action(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NO_CHANGE)

        action = _make_action(ActionType.FILL, "input#name", value="John")
        result = await bm.execute_action(action)

        page.fill.assert_called_once_with(
            "input#name",
            "John",
            timeout=bm.config.action_timeout_ms,
        )
        assert result.outcome == OutcomeType.NO_CHANGE

    @pytest.mark.asyncio
    async def test_select_option_action(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NO_CHANGE)

        action = _make_action(ActionType.SELECT_OPTION, "select#country", value="US")
        result = await bm.execute_action(action)

        page.select_option.assert_called_once_with(
            "select#country",
            "US",
            timeout=bm.config.action_timeout_ms,
        )
        assert result.outcome == OutcomeType.NO_CHANGE

    @pytest.mark.asyncio
    async def test_check_action(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NO_CHANGE)

        action = _make_action(ActionType.CHECK, "input#agree")
        result = await bm.execute_action(action)

        page.check.assert_called_once_with(
            "input#agree",
            timeout=bm.config.action_timeout_ms,
        )
        assert result.outcome == OutcomeType.NO_CHANGE

    @pytest.mark.asyncio
    async def test_uncheck_action(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NO_CHANGE)

        action = _make_action(ActionType.UNCHECK, "input#agree")
        result = await bm.execute_action(action)

        page.uncheck.assert_called_once_with(
            "input#agree",
            timeout=bm.config.action_timeout_ms,
        )
        assert result.outcome == OutcomeType.NO_CHANGE

    @pytest.mark.asyncio
    async def test_hover_action(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NO_CHANGE)

        action = _make_action(ActionType.HOVER, "div.tooltip-trigger")
        result = await bm.execute_action(action)

        page.hover.assert_called_once_with(
            "div.tooltip-trigger",
            timeout=bm.config.action_timeout_ms,
        )
        assert result.outcome == OutcomeType.NO_CHANGE

    @pytest.mark.asyncio
    async def test_press_key_action(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NO_CHANGE)

        action = _make_action(ActionType.PRESS_KEY, "", value="Enter")
        result = await bm.execute_action(action)

        page.keyboard.press.assert_called_once_with("Enter")
        assert result.outcome == OutcomeType.NO_CHANGE

    @pytest.mark.asyncio
    async def test_navigate_action(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NAVIGATION)

        action = _make_action(
            ActionType.NAVIGATE, "", value="https://example.com/page2"
        )
        await bm.execute_action(action)

        page.goto.assert_called_once_with(
            "https://example.com/page2",
            timeout=bm.config.timeout_ms,
        )

    @pytest.mark.asyncio
    async def test_submit_form_fills_fields_then_clicks(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        bm._detector = MagicMock()
        bm._detector.find_error_messages = AsyncMock(return_value=[])
        bm._detector.classify = MagicMock(return_value=OutcomeType.NO_CHANGE)

        field_values = {"input#name": "John", "input#email": "john@test.com"}
        action = _make_action(
            ActionType.SUBMIT_FORM,
            "button#submit",
            metadata={"field_values_json": json.dumps(field_values)},
        )
        await bm.execute_action(action)

        # Should fill each field
        assert page.fill.call_count == 2
        # Then click submit
        page.click.assert_called_once_with(
            "button#submit",
            timeout=bm.config.action_timeout_ms,
        )


# ---------------------------------------------------------------------------
# BrowserManager timeout/exception handling tests
# ---------------------------------------------------------------------------


class TestActionErrorHandling:
    """Tests for timeout and exception handling during action execution."""

    @pytest.mark.asyncio
    async def test_timeout_produces_timeout_outcome(self):
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError

        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        page.click = AsyncMock(side_effect=PlaywrightTimeoutError("click timeout"))

        action = _make_action(ActionType.CLICK, "button#slow")
        result = await bm.execute_action(action)

        assert result.outcome == OutcomeType.TIMEOUT
        assert "click timeout" in result.message

    @pytest.mark.asyncio
    async def test_playwright_error_produces_exception_outcome(self):
        from playwright.async_api import Error as PlaywrightError

        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page
        page.evaluate = AsyncMock(return_value="<html></html>")
        page.click = AsyncMock(side_effect=PlaywrightError("detached"))

        action = _make_action(ActionType.CLICK, "button#gone")
        result = await bm.execute_action(action)

        assert result.outcome == OutcomeType.EXCEPTION
        assert "detached" in result.message


# ---------------------------------------------------------------------------
# BrowserManager.capture_state tests
# ---------------------------------------------------------------------------


class TestCaptureState:
    """Tests for page state capture."""

    @pytest.mark.asyncio
    async def test_capture_state_returns_page_state(self):
        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page

        # All evaluate calls return strings (except signals which is a list)
        page.evaluate = AsyncMock(
            side_effect=[
                # DOM structure
                "<html><body></body></html>",
                # Visible text
                "Hello World",
                # Form state
                "{}",
                # Signals (list of strings)
                [],
            ]
        )

        state = await bm.capture_state(depth=1)

        assert state.url == "https://example.com"
        assert state.depth == 1
        assert state.state_id is not None
        assert state.fingerprint is not None

    @pytest.mark.asyncio
    async def test_capture_state_retries_on_load_failure(self):
        from playwright.async_api import Error as PlaywrightError

        bm = BrowserManager(_config())
        page = _mock_page()
        bm._page = page

        # First load wait fails, second succeeds
        page.wait_for_load_state = AsyncMock(
            side_effect=[PlaywrightError("navigation"), None, None],
        )
        page.evaluate = AsyncMock(
            side_effect=[
                "<html></html>",
                "text",
                "{}",
                [],
            ]
        )

        state = await bm.capture_state(depth=0)
        assert state is not None
        assert page.wait_for_load_state.call_count >= 2


# ---------------------------------------------------------------------------
# BrowserManager screenshot tests
# ---------------------------------------------------------------------------


class TestScreenshots:
    """Tests for screenshot capture."""

    @pytest.mark.asyncio
    async def test_screenshot_disabled_returns_none(self):
        bm = BrowserManager(_config(take_screenshots=False))
        page = _mock_page()
        bm._page = page

        action = _make_action()
        result = await bm._capture_action_screenshot(action)
        assert result is None

    @pytest.mark.asyncio
    async def test_screenshot_no_evidence_dir_returns_none(self):
        bm = BrowserManager(_config(take_screenshots=True))
        # evidence_dir defaults to None
        page = _mock_page()
        bm._page = page

        action = _make_action()
        result = await bm._capture_action_screenshot(action)
        assert result is None

"""Tests for BrowserManager and StabilityWaiter."""

from __future__ import annotations

import json
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

import flowscout.core.browser as browser_module
from flowscout.core.browser import BrowserManager, StabilityWaiter
from flowscout.core.state import ExplorerConfig
from flowscout.discovery.actions import Action, ActionType, OutcomeType

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _config(**overrides: Any) -> ExplorerConfig:
    defaults: dict[str, Any] = {
        "start_url": "https://example.com",
        "headless": True,
    }
    defaults.update(overrides)
    return ExplorerConfig.model_validate(defaults)


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


def _install_playwright_mocks(
    *,
    monkeypatch: pytest.MonkeyPatch,
    chromium: Any,
) -> Any:
    playwright = SimpleNamespace(
        chromium=chromium,
        stop=AsyncMock(),
    )

    class _FakeAsyncPlaywright:
        async def start(self) -> Any:
            return playwright

    monkeypatch.setattr(browser_module, "async_playwright", _FakeAsyncPlaywright)
    return playwright


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
# BrowserManager launch/context tests
# ---------------------------------------------------------------------------


class TestBrowserManagerLaunchContext:
    """Tests for launch modes, stealth defaults, and context persistence."""

    @pytest.mark.asyncio
    async def test_launch_applies_stealth_defaults(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        page = MagicMock()
        context = MagicMock()
        context.pages = []
        context.new_page = AsyncMock(return_value=page)
        context.add_init_script = AsyncMock()
        context.add_cookies = AsyncMock()
        context.close = AsyncMock()

        browser = MagicMock()
        browser.version = "124.0.6367.91"
        browser.contexts = []
        browser.new_context = AsyncMock(return_value=context)
        browser.close = AsyncMock()

        chromium = MagicMock()
        chromium.launch = AsyncMock(return_value=browser)
        chromium.connect_over_cdp = AsyncMock()
        playwright = _install_playwright_mocks(
            monkeypatch=monkeypatch,
            chromium=chromium,
        )

        bm = BrowserManager(_config(stealth=True))
        await bm.launch()

        launch_kwargs = chromium.launch.await_args.kwargs
        assert "--disable-blink-features=AutomationControlled" in launch_kwargs["args"]

        context_kwargs = browser.new_context.await_args.kwargs
        assert "Chrome/124.0.6367.91" in context_kwargs["user_agent"]
        assert context.add_init_script.await_count == 1
        assert "webdriver" in context.add_init_script.await_args.args[0]

        await bm.close()
        browser.close.assert_awaited_once()
        playwright.stop.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_no_stealth_disables_patches(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        page = MagicMock()
        context = MagicMock()
        context.pages = []
        context.new_page = AsyncMock(return_value=page)
        context.add_init_script = AsyncMock()
        context.add_cookies = AsyncMock()
        context.close = AsyncMock()

        browser = MagicMock()
        browser.version = "124.0.6367.91"
        browser.contexts = []
        browser.new_context = AsyncMock(return_value=context)
        browser.close = AsyncMock()

        chromium = MagicMock()
        chromium.launch = AsyncMock(return_value=browser)
        chromium.connect_over_cdp = AsyncMock()
        _install_playwright_mocks(monkeypatch=monkeypatch, chromium=chromium)

        bm = BrowserManager(_config(stealth=False))
        await bm.launch()

        launch_kwargs = chromium.launch.await_args.kwargs
        assert launch_kwargs["args"] == []
        context_kwargs = browser.new_context.await_args.kwargs
        assert "user_agent" not in context_kwargs
        context.add_init_script.assert_not_awaited()

        await bm.close()

    @pytest.mark.asyncio
    async def test_launch_loads_context_and_restores_session_storage(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        context_file = tmp_path / "ctx.json"
        context_file.write_text(
            json.dumps(
                {
                    "cookies": [
                        {
                            "name": "sid",
                            "value": "abc",
                            "domain": "example.com",
                            "path": "/",
                        }
                    ],
                    "origins": [
                        {
                            "origin": "https://example.com",
                            "localStorage": [{"name": "theme", "value": "light"}],
                        }
                    ],
                    "sessionStorage": {
                        "https://example.com": {"csrf": "token-1"},
                    },
                },
            ),
        )

        page = MagicMock()
        context = MagicMock()
        context.pages = []
        context.new_page = AsyncMock(return_value=page)
        context.add_init_script = AsyncMock()
        context.add_cookies = AsyncMock()
        context.close = AsyncMock()

        browser = MagicMock()
        browser.version = "124.0.6367.91"
        browser.contexts = []
        browser.new_context = AsyncMock(return_value=context)
        browser.close = AsyncMock()

        chromium = MagicMock()
        chromium.launch = AsyncMock(return_value=browser)
        chromium.connect_over_cdp = AsyncMock()
        _install_playwright_mocks(monkeypatch=monkeypatch, chromium=chromium)

        bm = BrowserManager(
            _config(
                stealth=False,
                load_context_path=str(context_file),
            )
        )
        await bm.launch()

        storage_state = browser.new_context.await_args.kwargs["storage_state"]
        assert storage_state["cookies"][0]["name"] == "sid"
        assert storage_state["origins"][0]["origin"] == "https://example.com"
        assert context.add_init_script.await_count == 1
        assert "sessionStorageByOrigin" in context.add_init_script.await_args.args[0]

        await bm.close()

    @pytest.mark.asyncio
    async def test_save_and_load_context_round_trip(
        self,
        tmp_path: Path,
    ) -> None:
        context_file = tmp_path / "ctx" / "session.json"
        bm = BrowserManager(_config(save_context_path=str(context_file)))
        bm._context = MagicMock()
        bm._context.storage_state = AsyncMock(
            return_value={
                "cookies": [
                    {
                        "name": "sid",
                        "value": "abc",
                        "domain": "example.com",
                        "path": "/",
                    }
                ],
                "origins": [
                    {
                        "origin": "https://example.com",
                        "localStorage": [{"name": "theme", "value": "light"}],
                    }
                ],
            },
        )
        bm._page = MagicMock()
        bm._page.url = "https://example.com/dashboard"
        bm._page.evaluate = AsyncMock(return_value={"csrf": "token-1"})

        saved = await bm.save_context()
        assert saved == str(context_file)
        payload = json.loads(context_file.read_text())
        assert payload["cookies"][0]["name"] == "sid"
        assert payload["origins"][0]["origin"] == "https://example.com"
        assert payload["localStorage"]["https://example.com"]["theme"] == "light"
        assert payload["sessionStorage"]["https://example.com"]["csrf"] == "token-1"

        reloaded = BrowserManager(_config(load_context_path=str(context_file)))
        loaded_payload = reloaded.load_context()
        assert loaded_payload["storage_state"]["cookies"][0]["name"] == "sid"
        assert (
            loaded_payload["session_storage_by_origin"]["https://example.com"]["csrf"]
            == "token-1"
        )

    @pytest.mark.asyncio
    async def test_cdp_uses_existing_browser_and_does_not_close_it(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        existing_page = MagicMock()
        existing_context = MagicMock()
        existing_context.pages = [existing_page]
        existing_context.new_page = AsyncMock(return_value=existing_page)
        existing_context.add_init_script = AsyncMock()
        existing_context.add_cookies = AsyncMock()

        browser = MagicMock()
        browser.version = "124.0.6367.91"
        browser.contexts = [existing_context]
        browser.new_context = AsyncMock()
        browser.close = AsyncMock()

        chromium = MagicMock()
        chromium.connect_over_cdp = AsyncMock(return_value=browser)
        chromium.launch = AsyncMock()
        playwright = _install_playwright_mocks(
            monkeypatch=monkeypatch,
            chromium=chromium,
        )

        endpoint = "ws://localhost:9222/devtools/browser/abc123"
        bm = BrowserManager(
            _config(
                stealth=False,
                cdp_endpoint=endpoint,
            )
        )
        await bm.launch()

        chromium.connect_over_cdp.assert_awaited_once_with(endpoint)
        chromium.launch.assert_not_called()
        assert bm.using_cdp is True
        assert bm.page is existing_page

        await bm.close()
        browser.close.assert_not_awaited()
        playwright.stop.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_cdp_connection_error_is_clear(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        from playwright.async_api import Error as PlaywrightError

        chromium = MagicMock()
        chromium.connect_over_cdp = AsyncMock(side_effect=PlaywrightError("boom"))
        chromium.launch = AsyncMock()
        _install_playwright_mocks(monkeypatch=monkeypatch, chromium=chromium)

        endpoint = "ws://localhost:9222/devtools/browser/abc123"
        bm = BrowserManager(_config(cdp_endpoint=endpoint))
        with pytest.raises(RuntimeError, match="Could not connect to CDP endpoint"):
            await bm.launch()


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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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
        bm._detector.describe_transition = MagicMock(
            return_value=("no_change", "No user-visible change was detected.")
        )

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

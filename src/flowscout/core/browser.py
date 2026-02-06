"""Async Playwright browser wrapper with action execution."""

from __future__ import annotations

import asyncio
import json
import time
from hashlib import sha256

from playwright.async_api import Page, async_playwright, Browser, BrowserContext

from flowscout.core.state import (
    ExplorerConfig,
    FingerprintConfig,
    PageState,
    build_fingerprint,
    make_state_id,
)
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.analysis.detector import OutcomeDetector
from flowscout.js import load_script

DOM_STRUCTURE_JS = load_script("dom_structure")
VISIBLE_TEXT_JS = load_script("visible_text")
FORM_STATE_JS = load_script("form_state")
SIGNALS_JS = load_script("signals")


class BrowserManager:
    """Manages Playwright browser lifecycle and action execution."""

    def __init__(self, config: ExplorerConfig) -> None:
        self.config = config
        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._detector = OutcomeDetector()
        self._fingerprint_config = FingerprintConfig()

    @property
    def page(self) -> Page:
        if self._page is None:
            msg = "Browser not launched. Call launch() first."
            raise RuntimeError(msg)
        return self._page

    async def launch(self) -> None:
        """Launch the browser."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self.config.headless,
        )
        self._context = await self._browser.new_context(
            viewport={"width": 1280, "height": 720},
        )
        self._page = await self._context.new_page()

    async def close(self) -> None:
        """Close the browser and clean up."""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def navigate(self, url: str) -> None:
        """Navigate to a URL and wait for load."""
        await self.page.goto(
            url, timeout=self.config.timeout_ms, wait_until="domcontentloaded"
        )
        await self._wait_for_stability()

    async def take_screenshot(self, path: str) -> None:
        """Take a screenshot of the current page."""
        await self.page.screenshot(path=path, full_page=False)

    async def capture_state(self, depth: int) -> PageState:
        """Capture the current page state with fingerprinting."""
        # Wait for any in-flight navigation to finish
        for _ in range(3):
            try:
                await self.page.wait_for_load_state("domcontentloaded", timeout=3000)
                break
            except Exception:
                await asyncio.sleep(0.3)

        url = self.page.url
        title = await self.page.title()

        # Compute the three hash components
        dom_skeleton = await self.page.evaluate(DOM_STRUCTURE_JS)
        dom_hash = sha256(dom_skeleton.encode()).hexdigest()

        visible_text = await self.page.evaluate(VISIBLE_TEXT_JS)
        text_hash = sha256(visible_text.encode()).hexdigest()

        form_state = await self.page.evaluate(FORM_STATE_JS)
        form_hash = sha256(form_state.encode()).hexdigest()

        signals = await self.page.evaluate(SIGNALS_JS)

        fp = build_fingerprint(
            url=url,
            title=title,
            dom_structure_hash=dom_hash,
            visible_text_hash=text_hash,
            form_state_hash=form_hash,
            config=self._fingerprint_config,
        )

        return PageState(
            state_id=make_state_id(fp),
            url=url,
            title=title,
            fingerprint=fp,
            depth=depth,
            dom_structure_hash=dom_hash,
            visible_text_hash=text_hash,
            form_state_hash=form_hash,
            signals=signals,
        )

    async def get_dom_hash(self) -> str:
        """Get the current DOM structure hash."""
        skeleton = await self.page.evaluate(DOM_STRUCTURE_JS)
        return sha256(skeleton.encode()).hexdigest()

    async def execute_action(self, action: Action) -> ActionResult:
        """Execute an action and observe the result."""
        page = self.page
        url_before = page.url
        dom_hash_before = await self.get_dom_hash()

        console_errors: list[str] = []
        network_errors: list[dict[str, str]] = []

        def on_console(msg):
            if msg.type == "error":
                console_errors.append(msg.text)

        def on_response(resp):
            if resp.status >= 400:
                network_errors.append({"url": resp.url, "status": str(resp.status)})

        page.on("console", on_console)
        page.on("response", on_response)

        start = time.monotonic()
        outcome = OutcomeType.NO_CHANGE
        message = ""

        try:
            await self._perform_action(action)
            await self._wait_for_stability()
        except Exception as exc:
            duration_ms = (time.monotonic() - start) * 1000
            error_name = type(exc).__name__
            if "timeout" in error_name.lower() or "Timeout" in str(exc):
                outcome = OutcomeType.TIMEOUT
            else:
                outcome = OutcomeType.EXCEPTION
            message = str(exc)

            page.remove_listener("console", on_console)
            page.remove_listener("response", on_response)

            return ActionResult(
                action_id=action.action_id,
                outcome=outcome,
                duration_ms=duration_ms,
                message=message,
                url_before=url_before,
                url_after=page.url,
            )

        duration_ms = (time.monotonic() - start) * 1000
        url_after = page.url
        dom_hash_after = await self.get_dom_hash()

        # Scan for error messages
        error_messages = await self._detector.find_error_messages(page)

        # Classify outcome
        outcome = self._detector.classify(
            url_before=url_before,
            url_after=url_after,
            dom_hash_before=dom_hash_before,
            dom_hash_after=dom_hash_after,
            error_messages=error_messages,
            console_errors=console_errors,
            network_errors=network_errors,
        )

        page.remove_listener("console", on_console)
        page.remove_listener("response", on_response)

        return ActionResult(
            action_id=action.action_id,
            outcome=outcome,
            duration_ms=duration_ms,
            message=message,
            url_before=url_before,
            url_after=url_after,
            error_messages=error_messages,
            console_errors=console_errors,
        )

    async def _perform_action(self, action: Action) -> None:
        """Execute the actual browser action."""
        page = self.page
        timeout = 5000

        match action.action_type:
            case ActionType.CLICK:
                # If this option requires opening a dropdown first
                if "requires_open" in action.metadata:
                    await page.click(action.metadata["requires_open"], timeout=timeout)
                    await asyncio.sleep(0.3)
                await page.click(action.target_selector, timeout=timeout)

            case ActionType.FILL:
                await page.fill(
                    action.target_selector, action.value or "", timeout=timeout
                )

            case ActionType.SELECT_OPTION:
                await page.select_option(
                    action.target_selector, action.value, timeout=timeout
                )

            case ActionType.CHECK:
                await page.check(action.target_selector, timeout=timeout)

            case ActionType.UNCHECK:
                await page.uncheck(action.target_selector, timeout=timeout)

            case ActionType.PRESS_KEY:
                await page.keyboard.press(action.value or "")

            case ActionType.SUBMIT_FORM:
                # Fill all fields first, then click submit
                field_values = json.loads(
                    action.metadata.get("field_values_json", "{}")
                )
                for selector, value in field_values.items():
                    try:
                        await page.fill(selector, value, timeout=3000)
                    except Exception:
                        pass  # Field may not be fillable
                await page.click(action.target_selector, timeout=timeout)

            case ActionType.HOVER:
                await page.hover(action.target_selector, timeout=timeout)

            case ActionType.NAVIGATE:
                await page.goto(action.value or "", timeout=self.config.timeout_ms)

    async def _wait_for_stability(self, timeout_ms: int = 2000) -> None:
        """Wait for the DOM to stabilize after an action."""
        deadline = time.monotonic() + (timeout_ms / 1000)
        prev_hash = await self.get_dom_hash()

        while time.monotonic() < deadline:
            await asyncio.sleep(0.2)
            current_hash = await self.get_dom_hash()
            if current_hash == prev_hash:
                return
            prev_hash = current_hash

        # Timeout — DOM is still changing, proceed anyway

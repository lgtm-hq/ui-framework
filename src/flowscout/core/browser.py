"""Async Playwright browser wrapper with action execution."""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from collections.abc import Awaitable, Callable
from hashlib import sha256
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from playwright.async_api import (
    Page,
    Playwright,
    async_playwright,
    Browser,
    BrowserContext,
)
from playwright.async_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
)

from flowscout.analysis.detector import OutcomeDetector
from flowscout.core.auth import AuthBootstrap
from flowscout.core.constants import DEFAULT_BROWSER, BrowserDefaults
from flowscout.core.state import (
    ExplorerConfig,
    FingerprintConfig,
    PageState,
    build_fingerprint,
    build_context_key,
    build_route_key,
    build_view_key,
    extract_context_markers,
    extract_primary_heading,
    make_state_id,
)
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.js import load_script

logger = logging.getLogger(__name__)

DOM_STRUCTURE_JS = load_script("dom_structure")
VISIBLE_TEXT_JS = load_script("visible_text")
FORM_STATE_JS = load_script("form_state")
SIGNALS_JS = load_script("signals")
PAGE_ANALYSIS_JS = load_script("page_analysis")
STEALTH_PATCH_JS = """
() => {
  const override = (obj, prop, value) => {
    try {
      Object.defineProperty(obj, prop, {
        configurable: true,
        get: () => value,
      });
    } catch (_err) {
      // Best effort.
    }
  };

  override(Navigator.prototype, 'webdriver', undefined);
  override(Navigator.prototype, 'platform', 'Win32');
  override(Navigator.prototype, 'language', 'en-US');
  override(Navigator.prototype, 'languages', ['en-US', 'en']);

  const fakePlugins = [
    { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
    { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
    { name: 'Native Client', filename: 'internal-nacl-plugin' },
  ];
  override(Navigator.prototype, 'plugins', fakePlugins);
  override(
    Navigator.prototype,
    'mimeTypes',
    [{ type: 'application/pdf', suffixes: 'pdf', description: 'PDF' }],
  );

  if (!window.chrome) {
    Object.defineProperty(window, 'chrome', {
      configurable: true,
      value: { runtime: {} },
    });
  } else if (!window.chrome.runtime) {
    Object.defineProperty(window.chrome, 'runtime', {
      configurable: true,
      value: {},
    });
  }

  const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
  WebGLRenderingContext.prototype.getParameter = function (parameter) {
    // UNMASKED_VENDOR_WEBGL / UNMASKED_RENDERER_WEBGL
    if (parameter === 0x9245) return 'Intel Inc.';
    if (parameter === 0x9246) return 'Intel Iris OpenGL Engine';
    return originalGetParameter.call(this, parameter);
  };
}
"""


def _build_stealth_user_agent(*, browser_version: str) -> str:
    """Build a realistic Chrome User-Agent based on Chromium version."""
    version_match = re.search(r"\d+(?:\.\d+){0,3}", browser_version or "")
    chrome_version = version_match.group(0) if version_match else "120.0.0.0"
    return (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome_version} Safari/537.36"
    )


def _coerce_session_storage(
    payload: object,
) -> dict[str, dict[str, str]]:
    """Normalize persisted session storage payload to mapping form."""
    if not isinstance(payload, dict):
        return {}
    normalized: dict[str, dict[str, str]] = {}
    for origin, storage in payload.items():
        if not isinstance(origin, str) or not isinstance(storage, dict):
            continue
        normalized[origin] = {str(key): str(value) for key, value in storage.items()}
    return normalized


def _build_session_storage_restore_script(
    *,
    session_storage_by_origin: dict[str, dict[str, str]],
) -> str:
    """Build an init script that restores sessionStorage per origin."""
    payload = json.dumps(session_storage_by_origin, separators=(",", ":"))
    return (
        "() => {\n"
        f"  const sessionStorageByOrigin = {payload};\n"
        "  const origin = window.location.origin;\n"
        "  const rows = sessionStorageByOrigin?.[origin];\n"
        "  if (!rows || typeof rows !== 'object') {\n"
        "    return;\n"
        "  }\n"
        "  for (const [key, value] of Object.entries(rows)) {\n"
        "    try {\n"
        "      window.sessionStorage.setItem(String(key), String(value));\n"
        "    } catch (_err) {\n"
        "      // Ignore storage restoration errors for restricted origins.\n"
        "    }\n"
        "  }\n"
        "}\n"
    )


class StabilityWaiter:
    """Waits for the DOM to stabilize by polling hash changes."""

    def __init__(
        self,
        *,
        poll_interval_s: float = 0.2,
    ) -> None:
        self.poll_interval_s = poll_interval_s

    async def wait(
        self,
        get_hash: Callable[[], Awaitable[str]],
        timeout_ms: int,
    ) -> None:
        """Poll ``get_hash`` until two consecutive calls return the same value.

        ``get_hash`` must be an async callable returning a string hash.
        """
        deadline = time.monotonic() + (timeout_ms / 1000)
        prev_hash = await get_hash()

        while time.monotonic() < deadline:
            await asyncio.sleep(self.poll_interval_s)
            current_hash = await get_hash()
            if current_hash == prev_hash:
                return
            prev_hash = current_hash

        # Timeout — DOM is still changing, proceed anyway


class BrowserManager:
    """Manages Playwright browser lifecycle and action execution."""

    def __init__(
        self,
        config: ExplorerConfig,
        *,
        detector: OutcomeDetector | None = None,
        stability_waiter: StabilityWaiter | None = None,
        browser_defaults: BrowserDefaults | None = None,
    ) -> None:
        self.config = config
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._detector = detector or OutcomeDetector()
        self._browser_defaults = browser_defaults or DEFAULT_BROWSER
        self._stability_waiter = stability_waiter or StabilityWaiter(
            poll_interval_s=self._browser_defaults.stability_poll_interval_s,
        )
        self._fingerprint_config = FingerprintConfig()
        self._last_navigation_status: int | None = None
        self._using_cdp = False
        self._context_owned = True
        self._session_storage_by_origin: dict[str, dict[str, str]] = {}

    @property
    def page(self) -> Page:
        if self._page is None:
            msg = "Browser not launched. Call launch() first."
            raise RuntimeError(msg)
        return self._page

    @property
    def last_navigation_status(self) -> int | None:
        """Most recent top-level document navigation status code, if available."""
        return self._last_navigation_status

    @property
    def using_cdp(self) -> bool:
        """Whether this browser manager is connected via CDP."""
        return self._using_cdp

    async def launch(self) -> None:
        """Launch the browser."""
        self._playwright = await async_playwright().start()
        loaded_context = self.load_context()
        self._session_storage_by_origin = loaded_context.get(
            "session_storage_by_origin",
            {},
        )

        if self.config.cdp_endpoint:
            self._using_cdp = True
            try:
                self._browser = await self._playwright.chromium.connect_over_cdp(
                    self.config.cdp_endpoint,
                )
            except PlaywrightError as exc:
                msg = (
                    "Could not connect to CDP endpoint "
                    f"{self.config.cdp_endpoint}: {exc}"
                )
                raise RuntimeError(msg) from exc
        else:
            launch_args: list[str] = []
            if self.config.stealth:
                launch_args.append("--disable-blink-features=AutomationControlled")
            self._browser = await self._playwright.chromium.launch(
                headless=self.config.headless,
                args=launch_args,
            )

        user_agent = ""
        if self.config.stealth:
            user_agent = _build_stealth_user_agent(
                browser_version=self._browser.version if self._browser else "",
            )

        storage_state: dict[str, Any] | None = loaded_context.get("storage_state")
        existing_context = (
            self._browser.contexts[0]
            if self._browser and self._browser.contexts
            else None
        )
        if existing_context is not None:
            self._context = existing_context
            self._context_owned = False
        else:
            context_kwargs: dict[str, Any] = {
                "viewport": {
                    "width": self._browser_defaults.viewport_width,
                    "height": self._browser_defaults.viewport_height,
                },
            }
            if storage_state:
                context_kwargs["storage_state"] = storage_state
            if user_agent:
                context_kwargs["user_agent"] = user_agent

            self._context = await self._browser.new_context(**context_kwargs)
            self._context_owned = True

        if self._context is None:
            msg = "Browser context was not created."
            raise RuntimeError(msg)

        if self.config.stealth:
            await self._context.add_init_script(STEALTH_PATCH_JS)
        if self._session_storage_by_origin:
            session_storage_script = _build_session_storage_restore_script(
                session_storage_by_origin=self._session_storage_by_origin,
            )
            await self._context.add_init_script(
                session_storage_script,
            )
        if loaded_context.get("cookies") and (
            existing_context is not None or not storage_state
        ):
            await self._context.add_cookies(loaded_context["cookies"])

        if self._context.pages:
            self._page = self._context.pages[0]
        else:
            self._page = await self._context.new_page()

    async def close(self) -> None:
        """Close the browser and clean up."""
        if self._context and self._context_owned and not self._using_cdp:
            await self._context.close()
        if self._browser and not self._using_cdp:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    def load_context(self) -> dict[str, Any]:
        """Load persisted browser context payload from disk."""
        load_path = self.config.load_context_path or self.config.context_path
        if not load_path:
            return {}

        path = Path(load_path).expanduser()
        if not path.exists():
            msg = f"Context file not found: {path}"
            raise RuntimeError(msg)

        try:
            raw_payload = json.loads(path.read_text())
        except OSError as exc:
            msg = f"Could not read context file {path}: {exc}"
            raise RuntimeError(msg) from exc
        except json.JSONDecodeError as exc:
            msg = f"Invalid context JSON in {path}: {exc}"
            raise RuntimeError(msg) from exc

        if not isinstance(raw_payload, dict):
            msg = f"Invalid context JSON in {path}: root must be an object."
            raise RuntimeError(msg)

        storage_state = raw_payload.get("storage_state")
        if not isinstance(storage_state, dict):
            storage_state = {
                "cookies": raw_payload.get("cookies", []),
                "origins": raw_payload.get("origins", []),
            }
        cookies = storage_state.get("cookies", [])
        if not isinstance(cookies, list):
            cookies = []

        session_storage_raw = raw_payload.get("sessionStorage", {})
        if not session_storage_raw:
            session_storage_raw = raw_payload.get("session_storage_by_origin", {})

        return {
            "storage_state": storage_state,
            "cookies": cookies,
            "session_storage_by_origin": _coerce_session_storage(session_storage_raw),
        }

    async def save_context(self) -> str | None:
        """Save current browser context to disk if configured."""
        save_path = self.config.save_context_path or self.config.context_path
        if not save_path:
            return None
        if self._context is None:
            msg = "Browser context is not available; cannot save context."
            raise RuntimeError(msg)

        storage_state = await self._context.storage_state()
        origins = storage_state.get("origins", [])
        local_storage_by_origin: dict[str, dict[str, str]] = {}
        for entry in origins:
            if not isinstance(entry, dict):
                continue
            origin = entry.get("origin")
            local_storage = entry.get("localStorage")
            if not isinstance(origin, str) or not isinstance(local_storage, list):
                continue
            normalized_local_storage: dict[str, str] = {}
            for item in local_storage:
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                value = item.get("value")
                if isinstance(name, str) and isinstance(value, str):
                    normalized_local_storage[name] = value
            if normalized_local_storage:
                local_storage_by_origin[origin] = normalized_local_storage

        session_storage_by_origin = dict(self._session_storage_by_origin)
        if self._page is not None and self._page.url:
            parsed = urlparse(self._page.url)
            if parsed.scheme and parsed.netloc:
                origin = f"{parsed.scheme}://{parsed.netloc}"
                try:
                    session_rows = await self._page.evaluate(
                        """
                        () => {
                          const out = {};
                          for (let idx = 0; idx < window.sessionStorage.length; idx++) {
                            const key = window.sessionStorage.key(idx);
                            if (!key) {
                              continue;
                            }
                            out[key] = window.sessionStorage.getItem(key) ?? '';
                          }
                          return out;
                        }
                        """,
                    )
                except PlaywrightError:
                    logger.debug("Could not snapshot sessionStorage", exc_info=True)
                else:
                    if isinstance(session_rows, dict):
                        session_storage_by_origin[origin] = {
                            str(key): str(value) for key, value in session_rows.items()
                        }

        payload = {
            "storage_state": storage_state,
            "cookies": storage_state.get("cookies", []),
            "origins": storage_state.get("origins", []),
            "localStorage": local_storage_by_origin,
            "sessionStorage": session_storage_by_origin,
        }

        path = Path(save_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2))
        return str(path)

    async def navigate(self, url: str) -> None:
        """Navigate to a URL and wait for load."""
        response = await self.page.goto(
            url, timeout=self.config.timeout_ms, wait_until="domcontentloaded"
        )
        self._last_navigation_status = response.status if response else None
        await self._wait_for_stability()

    async def apply_auth_bootstrap(self, auth: AuthBootstrap) -> None:
        """Execute deterministic login bootstrap before exploration."""
        target_url = auth.login_url or self.config.start_url
        await self.navigate(target_url)

        await self.page.locator(auth.username_selector).fill(
            auth.username,
            timeout=self.config.action_timeout_ms,
        )
        await self.page.locator(auth.password_selector).fill(
            auth.password,
            timeout=self.config.action_timeout_ms,
        )

        if auth.submit_selector:
            await self.page.locator(auth.submit_selector).click(
                timeout=self.config.action_timeout_ms,
            )
        else:
            await self.page.keyboard.press("Enter")

        await self._wait_for_stability()
        if auth.post_login_wait_ms:
            await self.page.wait_for_timeout(auth.post_login_wait_ms)

        if auth.success_selector:
            await self.page.locator(auth.success_selector).first.wait_for(
                timeout=self.config.timeout_ms,
            )

        if auth.success_url_pattern and not re.search(
            auth.success_url_pattern,
            self.page.url,
        ):
            msg = (
                "Auth bootstrap finished but URL did not match success_url_pattern: "
                f"{auth.success_url_pattern}"
            )
            raise RuntimeError(msg)

    async def take_screenshot(self, path: str) -> None:
        """Take a screenshot of the current page."""
        await self.page.screenshot(path=path, full_page=False)

    async def capture_state(self, depth: int) -> PageState:
        """Capture the current page state with fingerprinting."""
        # Wait for any in-flight navigation to finish
        for _ in range(3):
            try:
                await self.page.wait_for_load_state(
                    "domcontentloaded",
                    timeout=self.config.load_wait_timeout_ms,
                )
                break
            except PlaywrightError:
                logger.debug("DOM load wait failed, retrying", exc_info=True)
                await asyncio.sleep(self._browser_defaults.post_click_delay_s)

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
        primary_heading = extract_primary_heading(signals=signals, title=title)
        route_key = build_route_key(url, config=self._fingerprint_config)
        view_key = build_view_key(
            route_key=route_key,
            dom_structure_hash=dom_hash,
            primary_heading=primary_heading,
        )
        context_markers = extract_context_markers(
            signals=signals,
            form_state_hash=form_hash,
        )
        context_key = build_context_key(
            view_key=view_key,
            context_markers=context_markers,
        )

        fp = build_fingerprint(
            url=url,
            title=title,
            dom_structure_hash=dom_hash,
            visible_text_hash=text_hash,
            form_state_hash=form_hash,
            route_key=route_key,
            view_key=view_key,
            context_key=context_key,
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
            route_key=route_key,
            view_key=view_key,
            context_key=context_key,
            primary_heading=primary_heading,
            context_markers=context_markers,
            signals=signals,
        )

    async def analyze_page_structure(self) -> dict[str, Any]:
        """Run in-page structural analysis for smart mode."""
        result: dict[str, Any] = await self.page.evaluate(PAGE_ANALYSIS_JS)
        return result

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

        def on_console(msg: Any) -> None:
            if msg.type == "error":
                console_errors.append(msg.text)

        def on_response(resp: Any) -> None:
            if resp.status >= 400:
                network_errors.append({"url": resp.url, "status": str(resp.status)})
            try:
                request = resp.request
                resource_type = str(request.resource_type)
                if resource_type == "document":
                    self._last_navigation_status = int(resp.status)
            except (AttributeError, TypeError, ValueError):
                logger.debug("Could not infer response resource type", exc_info=True)

        page.on("console", on_console)
        page.on("response", on_response)

        start = time.monotonic()
        outcome = OutcomeType.NO_CHANGE
        message = ""

        try:
            await self._perform_action(action)
            await self._wait_for_stability()
        except PlaywrightTimeoutError as exc:
            duration_ms = (time.monotonic() - start) * 1000
            outcome = OutcomeType.TIMEOUT
            message = str(exc)
            screenshot_path = await self._capture_action_screenshot(action)

            page.remove_listener("console", on_console)
            page.remove_listener("response", on_response)

            return ActionResult(
                action_id=action.action_id,
                outcome=outcome,
                duration_ms=duration_ms,
                message=message,
                url_before=url_before,
                url_after=page.url,
                error_messages=[],
                console_errors=console_errors,
                screenshot_path=screenshot_path,
            )
        except (PlaywrightError, OSError) as exc:
            duration_ms = (time.monotonic() - start) * 1000
            outcome = OutcomeType.EXCEPTION
            message = str(exc)
            screenshot_path = await self._capture_action_screenshot(action)

            page.remove_listener("console", on_console)
            page.remove_listener("response", on_response)

            return ActionResult(
                action_id=action.action_id,
                outcome=outcome,
                duration_ms=duration_ms,
                message=message,
                url_before=url_before,
                url_after=page.url,
                screenshot_path=screenshot_path,
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
        screenshot_path = await self._capture_action_screenshot(action)

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
            screenshot_path=screenshot_path,
        )

    async def _capture_action_screenshot(self, action: Action) -> str | None:
        """Capture action evidence screenshot with highlighted target selector."""
        if not self.config.take_screenshots or not self.config.evidence_dir:
            return None

        evidence_dir = Path(self.config.evidence_dir)
        evidence_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = (
            evidence_dir / f"{int(time.time() * 1000)}_{action.action_id}.png"
        )
        overlay_id = f"flowscout-highlight-{action.action_id}"

        try:
            await self._render_highlight_overlay(
                selector=action.target_selector,
                overlay_id=overlay_id,
            )
            await self.page.screenshot(path=str(screenshot_path), full_page=False)
        except (PlaywrightError, OSError):
            logger.debug("Could not capture action screenshot", exc_info=True)
            return None
        finally:
            await self._clear_highlight_overlay(overlay_id=overlay_id)

        return str(screenshot_path)

    async def _render_highlight_overlay(
        self,
        *,
        selector: str,
        overlay_id: str,
    ) -> None:
        """Draw temporary highlight boxes around interacted target elements."""
        script = """
        ({ selector, overlayId }) => {
          const existing = document.getElementById(overlayId);
          if (existing) {
            existing.remove();
          }

          let elements = [];
          try {
            elements = Array.from(document.querySelectorAll(selector)).slice(0, 3);
          } catch (err) {
            elements = [];
          }
          if (!elements.length) {
            return;
          }

          const layer = document.createElement('div');
          layer.id = overlayId;
          layer.style.position = 'fixed';
          layer.style.inset = '0';
          layer.style.pointerEvents = 'none';
          layer.style.zIndex = '2147483647';

          elements.forEach((element, index) => {
            const rect = element.getBoundingClientRect();
            if (rect.width <= 0 || rect.height <= 0) {
              return;
            }

            const box = document.createElement('div');
            box.style.position = 'fixed';
            box.style.left = `${Math.max(rect.left - 2, 0)}px`;
            box.style.top = `${Math.max(rect.top - 2, 0)}px`;
            box.style.width = `${rect.width + 4}px`;
            box.style.height = `${rect.height + 4}px`;
            box.style.border = '3px solid #ff4757';
            box.style.background = 'rgba(255, 71, 87, 0.16)';
            box.style.boxShadow = '0 0 0 2px rgba(255,255,255,.4),'
              + ' 0 0 24px rgba(255,71,87,.6)';
            box.style.borderRadius = '4px';

            const tag = document.createElement('div');
            tag.textContent = `target ${index + 1}`;
            tag.style.position = 'absolute';
            tag.style.left = '-1px';
            tag.style.top = '-22px';
            tag.style.font = '700 10px/1 sans-serif';
            tag.style.letterSpacing = '0.05em';
            tag.style.textTransform = 'uppercase';
            tag.style.color = '#ffffff';
            tag.style.background = '#ff4757';
            tag.style.borderRadius = '3px';
            tag.style.padding = '3px 5px';

            box.appendChild(tag);
            layer.appendChild(box);
          });

          if (layer.childNodes.length > 0) {
            document.body.appendChild(layer);
          }
        }
        """
        await self.page.evaluate(
            script,
            {
                "selector": selector,
                "overlayId": overlay_id,
            },
        )

    async def _clear_highlight_overlay(self, *, overlay_id: str) -> None:
        """Remove temporary screenshot highlight overlay."""
        script = """
        ({ overlayId }) => {
          const node = document.getElementById(overlayId);
          if (node) {
            node.remove();
          }
        }
        """
        try:
            await self.page.evaluate(script, {"overlayId": overlay_id})
        except PlaywrightError:
            logger.debug("Could not clear screenshot overlay", exc_info=True)

    async def _perform_action(self, action: Action) -> None:
        """Execute the actual browser action."""
        page = self.page
        timeout = self.config.action_timeout_ms

        match action.action_type:
            case ActionType.CLICK:
                # If this option requires opening a dropdown first
                meta = action.meta
                if meta.requires_open:
                    await page.click(meta.requires_open, timeout=timeout)
                    await asyncio.sleep(self._browser_defaults.post_click_delay_s)
                await page.click(action.target_selector, timeout=timeout)

                # Search triggers: click reveals hidden inputs — find, fill, submit
                if meta.is_search:
                    await asyncio.sleep(self._browser_defaults.post_click_delay_s)
                    selectors = [
                        "input[type='search']:visible",
                        "input[placeholder*='earch']:visible",
                        "input[aria-label*='earch']:visible",
                    ]
                    for sel in selectors:
                        try:
                            inp = page.locator(sel).first
                            if await inp.is_visible(timeout=1000):
                                await inp.fill("test query")
                                await inp.press("Enter")
                                break
                        except PlaywrightError:
                            logger.debug(
                                "Search input %s not found", sel, exc_info=True
                            )
                            continue

            case ActionType.FILL:
                await page.fill(
                    action.target_selector, action.value or "", timeout=timeout
                )
                # Search inputs need Enter to trigger the search
                if action.meta.element_type == "input_search":
                    await page.press(action.target_selector, "Enter")

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
                field_values = action.meta.field_values
                for selector, value in field_values.items():
                    try:
                        await page.fill(
                            selector,
                            value,
                            timeout=self.config.load_wait_timeout_ms,
                        )
                    except PlaywrightError:
                        logger.debug("Could not fill field %s", selector, exc_info=True)
                await page.click(action.target_selector, timeout=timeout)

            case ActionType.HOVER:
                await page.hover(action.target_selector, timeout=timeout)

            case ActionType.NAVIGATE:
                await page.goto(action.value or "", timeout=self.config.timeout_ms)

    async def _wait_for_stability(self, timeout_ms: int | None = None) -> None:
        """Wait for the DOM to stabilize after an action."""
        if timeout_ms is None:
            timeout_ms = self.config.stability_timeout_ms
        await self._stability_waiter.wait(self.get_dom_hash, timeout_ms)

"""Integration test — full exploration of a local HTML fixture."""

import pytest

from flowscout.analysis.graph import ExplorationGraph
from flowscout.core.browser import BrowserManager
from flowscout.core.navigator import Navigator
from flowscout.core.state import ExplorerConfig
from flowscout.reporting.terminal import TerminalReporter

INDEX_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head><title>Home</title></head>
<body>
  <nav>
    <a href="/about">About</a>
    <a href="/form">Form</a>
  </nav>
  <h1>Welcome</h1>
  <p>This is the home page.</p>
</body>
</html>
"""

ABOUT_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head><title>About</title></head>
<body>
  <nav><a href="/">Home</a></nav>
  <h1>About Us</h1>
  <p>Details about our company.</p>
</body>
</html>
"""

FORM_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head><title>Contact</title></head>
<body>
  <nav><a href="/">Home</a></nav>
  <h1>Contact Form</h1>
  <form id="contact">
    <label for="email">Email</label>
    <input id="email" type="email" name="email" required />
    <label for="message">Message</label>
    <textarea id="message" name="message"></textarea>
    <button type="submit">Send</button>
  </form>
</body>
</html>
"""

INDEX_WITH_BLOCKED_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head><title>Home</title></head>
<body>
  <nav>
    <a href="/about">About</a>
    <a href="/blocked">Blocked</a>
  </nav>
  <h1>Welcome</h1>
</body>
</html>
"""

BLOCKED_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head><title>Forbidden</title></head>
<body>
  <h1>Access Denied</h1>
  <p>You are not authorized to access this page.</p>
</body>
</html>
"""


def _make_config(base_url: str) -> ExplorerConfig:
    return ExplorerConfig(
        start_url=base_url,
        max_depth=2,
        max_states=10,
        max_actions_per_state=10,
        headless=True,
        timeout_ms=10000,
        take_screenshots=False,
        smart_mode=False,
    )


def _setup_server(httpserver):
    httpserver.expect_request("/").respond_with_data(
        INDEX_HTML,
        content_type="text/html",
    )
    httpserver.expect_request("/about").respond_with_data(
        ABOUT_HTML,
        content_type="text/html",
    )
    httpserver.expect_request("/form").respond_with_data(
        FORM_HTML,
        content_type="text/html",
    )


class TestFullExploration:
    @pytest.mark.asyncio
    async def test_discovers_states_and_flows(self, httpserver):
        _setup_server(httpserver)
        base_url = httpserver.url_for("/")
        config = _make_config(base_url)

        browser = BrowserManager(config)
        try:
            await browser.launch()
            graph = ExplorationGraph()
            terminal = TerminalReporter(verbose=False)
            navigator = Navigator(browser, graph, config, terminal)
            result = await navigator.explore(base_url)

            n_states = len(result.states)
            n_results = len(result.results)
            n_flows = len(result.flows)
            assert n_states >= 2, f"Expected >=2 states, got {n_states}"
            assert n_results >= 1, f"Expected >=1 results, got {n_results}"
            assert n_flows >= 1, f"Expected >=1 flows, got {n_flows}"
        finally:
            await browser.close()

    @pytest.mark.asyncio
    async def test_blocked_page_does_not_stop_remaining_frontier_exploration(
        self,
        httpserver,
    ):
        httpserver.expect_request("/").respond_with_data(
            INDEX_WITH_BLOCKED_HTML,
            content_type="text/html",
        )
        httpserver.expect_request("/about").respond_with_data(
            ABOUT_HTML,
            content_type="text/html",
        )
        httpserver.expect_request("/blocked").respond_with_data(
            BLOCKED_HTML,
            status=403,
            content_type="text/html",
        )
        base_url = httpserver.url_for("/")
        config = _make_config(base_url)

        browser = BrowserManager(config)
        try:
            await browser.launch()
            graph = ExplorationGraph()
            terminal = TerminalReporter(verbose=False)
            navigator = Navigator(browser, graph, config, terminal)
            result = await navigator.explore(base_url)
        finally:
            await browser.close()

        by_url = {state.url: state for state in result.states.values()}
        assert any("/about" in url for url in by_url), "Expected About page to be found"

        blocked_states = [
            state
            for state in result.states.values()
            if state.block_reason.value == "access_denied"
        ]
        assert blocked_states, "Expected blocked page to be classified as ACCESS_DENIED"

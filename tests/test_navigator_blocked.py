"""Tests for blocked-page handling in Navigator."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from flowscout.analysis.graph import ExplorationGraph
import flowscout.core.navigator as navigator_module
from flowscout.core.navigator import Navigator
from flowscout.core.protocols import ITerminalReporter
from flowscout.core.state import ExplorerConfig, PageBlockReason, PageState
from flowscout.discovery.actions import Action, ActionResult


class _LocalTerminal(ITerminalReporter):
    """Minimal terminal reporter stub used for navigator tests."""

    def __init__(self) -> None:
        self.messages: list[str] = []
        self.warnings: list[str] = []

    def print_banner(self, url: str, config: ExplorerConfig) -> None:
        self.messages.append(f"banner:{url}")

    def log_state_discovered(self, state: PageState, *, is_new: bool) -> None:
        self.messages.append(f"state:{state.state_id}:{is_new}")

    def log_action_start(self, action: Action, state_id: str) -> None:
        self.messages.append(f"action-start:{state_id}:{action.action_id}")

    def log_action_result(
        self,
        action: Action,
        result: ActionResult,
        is_new_state: bool,
    ) -> None:
        self.messages.append(f"action-result:{action.action_id}:{is_new_state}")

    def log_info(self, message: str) -> None:
        self.messages.append(message)

    def log_warning(self, message: str) -> None:
        self.warnings.append(message)

    def log_archetype(
        self,
        state_id: str,
        archetype: str,
        confidence: float,
        is_novel: bool,
    ) -> None:
        self.messages.append(f"archetype:{state_id}:{archetype}")

    def log_expectation_result(self, result: Any) -> None:
        self.messages.append("expectation")

    def print_summary(self, result: Any) -> None:
        self.messages.append("summary")


def _make_config(tmp_path: Any, **overrides: Any) -> ExplorerConfig:
    values: dict[str, Any] = {
        "start_url": "https://example.com",
        "max_depth": 2,
        "max_states": 10,
        "max_actions_per_state": 10,
        "take_screenshots": True,
        "evidence_dir": str(tmp_path / "evidence"),
        "smart_mode": False,
    }
    values.update(overrides)
    return ExplorerConfig.model_validate(values)


def _make_state(**overrides: Any) -> PageState:
    values: dict[str, Any] = {
        "state_id": "state-1",
        "url": "https://example.com/blocked",
        "title": "Blocked",
        "fingerprint": "a" * 64,
        "depth": 0,
        "dom_structure_hash": "dom-1",
        "visible_text_hash": "text-1",
        "form_state_hash": "form-1",
    }
    values.update(overrides)
    return PageState.model_validate(values)


class _StubBrowser:
    def __init__(self, *, status_code: int | None = None) -> None:
        self.page = SimpleNamespace()
        self.last_navigation_status = status_code
        self.take_screenshot = AsyncMock()


@pytest.mark.asyncio
async def test_discovery_is_skipped_for_blocked_states(
    tmp_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _make_config(tmp_path)
    browser = _StubBrowser(status_code=403)
    graph = ExplorationGraph()
    terminal = _LocalTerminal()
    navigator = Navigator(
        browser=browser,  # type: ignore[arg-type]
        graph=graph,
        config=config,
        terminal=terminal,
    )
    blocked_state = _make_state(
        block_reason=PageBlockReason.ACCESS_DENIED,
        block_detail="Forbidden page",
    )

    async def _fail_if_called(*args: Any, **kwargs: Any) -> list[Any]:
        msg = "discover_elements should not be called for blocked states"
        raise AssertionError(msg)

    monkeypatch.setattr(navigator_module, "discover_elements", _fail_if_called)
    await navigator._discover_and_enqueue(blocked_state)

    assert navigator._frontier.size == 0
    assert any("Skipping element discovery" in message for message in terminal.messages)


@pytest.mark.asyncio
async def test_blocked_state_gets_screenshot_annotation(tmp_path: Any) -> None:
    config = _make_config(tmp_path)
    browser = _StubBrowser(status_code=403)
    graph = ExplorationGraph()
    terminal = _LocalTerminal()
    navigator = Navigator(
        browser=browser,  # type: ignore[arg-type]
        graph=graph,
        config=config,
        terminal=terminal,
    )
    state = _make_state()

    await navigator._annotate_blocked_state(state)

    assert state.block_reason == PageBlockReason.ACCESS_DENIED
    assert "HTTP 403" in state.block_detail
    assert state.screenshot_path is not None
    browser.take_screenshot.assert_awaited_once()

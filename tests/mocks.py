"""Shared mock implementations for testing against protocol interfaces."""

from __future__ import annotations

from typing import Any

from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType


class MockBrowser:
    """In-memory browser mock implementing IBrowser."""

    def __init__(
        self,
        *,
        states: dict[str, PageState] | None = None,
        action_results: dict[str, ActionResult] | None = None,
        dom_hash: str = "abc123",
    ) -> None:
        self._states = states or {}
        self._action_results = action_results or {}
        self._dom_hash = dom_hash
        self._current_url = "https://example.com"
        self._launched = False
        self._closed = False
        self._navigations: list[str] = []
        self._executed_actions: list[Action] = []
        self._screenshots: list[str] = []
        self._depth_counter = 0

    async def launch(self) -> None:
        self._launched = True

    async def close(self) -> None:
        self._closed = True

    async def navigate(self, url: str) -> None:
        self._current_url = url
        self._navigations.append(url)

    async def capture_state(self, depth: int) -> PageState:
        if self._current_url in self._states:
            return self._states[self._current_url]
        self._depth_counter += 1
        return PageState(
            state_id=f"state-{self._depth_counter}",
            url=self._current_url,
            title=f"Page at {self._current_url}",
            fingerprint=f"fp-{self._depth_counter}",
            depth=depth,
            dom_structure_hash=f"dom-{self._depth_counter}",
            visible_text_hash=f"text-{self._depth_counter}",
            form_state_hash=f"form-{self._depth_counter}",
        )

    async def execute_action(self, action: Action) -> ActionResult:
        self._executed_actions.append(action)
        if action.action_id in self._action_results:
            return self._action_results[action.action_id]
        return ActionResult(
            action_id=action.action_id,
            outcome=OutcomeType.NO_CHANGE,
            duration_ms=50.0,
            url_before=self._current_url,
            url_after=self._current_url,
        )

    async def get_dom_hash(self) -> str:
        return self._dom_hash

    async def take_screenshot(self, path: str) -> None:
        self._screenshots.append(path)

    async def analyze_page_structure(self) -> dict[str, Any]:
        return {}


class MockStorage:
    """In-memory storage mock implementing IStorage."""

    def __init__(self) -> None:
        self._runs: list[dict[str, Any]] = []
        self._closed = False

    def save_run(self, result: object) -> str:
        run_id = f"mock-run-{len(self._runs) + 1}"
        self._runs.append({"run_id": run_id, "result": result})
        return run_id

    def list_runs(
        self,
        *,
        start_url: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self._runs[:limit]

    def get_flaky_actions(
        self,
        start_url: str,
        min_runs: int = 2,
    ) -> list[dict[str, Any]]:
        return []

    def close(self) -> None:
        self._closed = True


class MockReporter:
    """In-memory reporter mock implementing IReporter."""

    def __init__(self) -> None:
        self.generated: list[tuple[object, str]] = []

    def generate(self, result: object, output_path: str) -> None:
        self.generated.append((result, output_path))


class MockTerminal:
    """In-memory terminal reporter mock implementing ITerminalReporter."""

    def __init__(self) -> None:
        self.messages: list[str] = []
        self.warnings: list[str] = []
        self.banner_count = 0
        self.state_logs: list[dict[str, Any]] = []
        self.action_starts: list[dict[str, Any]] = []
        self.action_results: list[dict[str, Any]] = []

    def print_banner(self, url: str, config: object) -> None:
        self.banner_count += 1

    def log_state_discovered(self, state: object, *, is_new: bool) -> None:
        self.state_logs.append({"state": state, "is_new": is_new})

    def log_action_start(self, action: object, state_id: str) -> None:
        self.action_starts.append({"action": action, "state_id": state_id})

    def log_action_result(
        self,
        action: object,
        result: object,
        is_new_state: bool,
    ) -> None:
        self.action_results.append(
            {
                "action": action,
                "result": result,
                "is_new_state": is_new_state,
            }
        )

    def log_info(self, message: str) -> None:
        self.messages.append(message)

    def log_warning(self, message: str) -> None:
        self.warnings.append(message)

    def print_summary(self, result: object) -> None:
        self.messages.append("__summary__")


def make_action(
    action_id: str = "act-1",
    action_type: ActionType = ActionType.CLICK,
    selector: str = "button#submit",
    label: str = "Submit",
    value: str | None = None,
    metadata: dict[str, str] | None = None,
    priority: int = 50,
) -> Action:
    """Create an Action with sensible defaults for testing."""
    return Action(
        action_id=action_id,
        action_type=action_type,
        target_selector=selector,
        label=label,
        value=value,
        metadata=metadata or {},
        priority=priority,
    )


def make_state(
    state_id: str = "s1",
    url: str = "https://example.com",
    title: str = "Example",
    fingerprint: str = "fp-1",
    depth: int = 0,
    dom_structure_hash: str = "dom-hash-1",
    visible_text_hash: str = "text-hash-1",
    form_state_hash: str = "form-hash-1",
) -> PageState:
    """Create a PageState with sensible defaults for testing."""
    return PageState(
        state_id=state_id,
        url=url,
        title=title,
        fingerprint=fingerprint,
        depth=depth,
        dom_structure_hash=dom_structure_hash,
        visible_text_hash=visible_text_hash,
        form_state_hash=form_state_hash,
    )


def make_result(
    action_id: str = "act-1",
    outcome: OutcomeType = OutcomeType.NO_CHANGE,
    source_state_id: str = "s1",
    target_state_id: str = "s1",
    duration_ms: float = 100.0,
    url_before: str = "https://example.com",
    url_after: str = "https://example.com",
) -> ActionResult:
    """Create an ActionResult with sensible defaults for testing."""
    return ActionResult(
        action_id=action_id,
        source_state_id=source_state_id,
        target_state_id=target_state_id,
        outcome=outcome,
        duration_ms=duration_ms,
        url_before=url_before,
        url_after=url_after,
    )

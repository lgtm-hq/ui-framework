"""Protocol interfaces for dependency inversion."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flowscout.analysis.expectations import ExpectationResult
    from flowscout.analysis.graph import ExplorationResult
    from flowscout.core.state import ExplorerConfig, PageState
    from flowscout.discovery.actions import Action, ActionResult, OutcomeType
    from flowscout.discovery.elements import InteractiveElement


@runtime_checkable
class IBrowser(Protocol):
    """Abstraction over browser automation."""

    async def launch(self) -> None: ...

    async def close(self) -> None: ...

    async def navigate(self, url: str) -> None: ...

    async def capture_state(self, depth: int) -> PageState: ...

    async def execute_action(self, action: Action) -> ActionResult: ...

    async def get_dom_hash(self) -> str: ...

    async def take_screenshot(self, path: str) -> None: ...

    async def analyze_page_structure(self) -> dict[str, Any]: ...


@runtime_checkable
class IOutcomeDetector(Protocol):
    """Abstraction over outcome classification."""

    def classify(
        self,
        *,
        url_before: str,
        url_after: str,
        dom_hash_before: str,
        dom_hash_after: str,
        error_messages: list[str],
        console_errors: list[str],
        network_errors: list[dict[str, str]],
    ) -> OutcomeType: ...

    async def find_error_messages(self, page: object) -> list[str]: ...


@runtime_checkable
class IStorage(Protocol):
    """Abstraction over persistence."""

    def save_run(self, result: ExplorationResult) -> str: ...

    def list_runs(
        self,
        *,
        start_url: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]: ...

    def get_flaky_actions(
        self,
        start_url: str,
        min_runs: int = 2,
    ) -> list[dict[str, Any]]: ...

    def close(self) -> None: ...


@runtime_checkable
class IReporter(Protocol):
    """Abstraction over report generation."""

    def generate(self, result: ExplorationResult, output_path: str) -> None: ...


@runtime_checkable
class ITerminalReporter(Protocol):
    """Abstraction over terminal output during exploration."""

    def print_banner(self, url: str, config: ExplorerConfig) -> None: ...

    def log_state_discovered(
        self,
        state: PageState,
        *,
        is_new: bool,
    ) -> None: ...

    def log_action_start(self, action: Action, state_id: str) -> None: ...

    def log_action_result(
        self,
        action: Action,
        result: ActionResult,
        is_new_state: bool,
    ) -> None: ...

    def log_info(self, message: str) -> None: ...

    def log_warning(self, message: str) -> None: ...

    def log_archetype(
        self,
        state_id: str,
        archetype: str,
        confidence: float,
        is_novel: bool,
    ) -> None: ...

    def log_expectation_result(self, result: ExpectationResult) -> None: ...

    def print_summary(self, result: ExplorationResult) -> None: ...


@runtime_checkable
class IElementDiscoverer(Protocol):
    """Abstraction over element discovery."""

    async def discover(self, page: object) -> list[InteractiveElement]: ...

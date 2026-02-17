"""POM adapter registry."""

from __future__ import annotations

from flowscout.codegen.adapters.base import POMAdapter
from flowscout.codegen.adapters.playwright_python import PlaywrightPythonAdapter
from flowscout.codegen.adapters.playwright_ts import PlaywrightTSAdapter

ADAPTERS: dict[str, type[POMAdapter]] = {
    "pytest": PlaywrightPythonAdapter,
    "playwright": PlaywrightTSAdapter,
}


def get_adapter(framework: str) -> POMAdapter:
    """Get adapter by framework name. Raises KeyError if unknown."""
    cls = ADAPTERS.get(framework)
    if cls is None:
        raise KeyError(
            f"Unknown framework '{framework}'. Available: {', '.join(ADAPTERS)}"
        )
    return cls()


__all__ = [
    "ADAPTERS",
    "POMAdapter",
    "PlaywrightPythonAdapter",
    "PlaywrightTSAdapter",
    "get_adapter",
]

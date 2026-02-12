"""Plugin registry for reporters, detectors, and discoverers."""

from __future__ import annotations

import importlib.metadata
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flowscout.core.protocols import IElementDiscoverer, IOutcomeDetector, IReporter

logger = logging.getLogger(__name__)

_ENTRY_POINT_GROUPS = {
    "reporters": "flowscout.reporters",
    "detectors": "flowscout.detectors",
    "discoverers": "flowscout.discoverers",
}


class PluginRegistry:
    """Central registry for flowscout extension points.

    Plugins can be registered programmatically via ``register_*`` methods
    or discovered automatically from Python entry points via
    ``load_from_entry_points()``.
    """

    def __init__(self) -> None:
        self._reporters: dict[str, type[IReporter]] = {}
        self._detectors: dict[str, type[IOutcomeDetector]] = {}
        self._discoverers: dict[str, type[IElementDiscoverer]] = {}

    # ── Reporters ──

    def register_reporter(self, name: str, cls: type[IReporter]) -> None:
        """Register a reporter class under the given name."""
        self._reporters[name] = cls

    def get_reporter(self, name: str) -> type[IReporter] | None:
        """Return the reporter class registered under *name*, or ``None``."""
        return self._reporters.get(name)

    def list_reporters(self) -> list[str]:
        """Return sorted list of registered reporter names."""
        return sorted(self._reporters)

    # ── Detectors ──

    def register_detector(self, name: str, cls: type[IOutcomeDetector]) -> None:
        """Register an outcome detector class under the given name."""
        self._detectors[name] = cls

    def get_detector(self, name: str) -> type[IOutcomeDetector] | None:
        """Return the detector class registered under *name*, or ``None``."""
        return self._detectors.get(name)

    def list_detectors(self) -> list[str]:
        """Return sorted list of registered detector names."""
        return sorted(self._detectors)

    # ── Discoverers ──

    def register_discoverer(self, name: str, cls: type[IElementDiscoverer]) -> None:
        """Register an element discoverer class under the given name."""
        self._discoverers[name] = cls

    def get_discoverer(self, name: str) -> type[IElementDiscoverer] | None:
        """Return the discoverer class registered under *name*, or ``None``."""
        return self._discoverers.get(name)

    def list_discoverers(self) -> list[str]:
        """Return sorted list of registered discoverer names."""
        return sorted(self._discoverers)

    # ── Entry point loading ──

    def load_from_entry_points(self) -> None:
        """Discover and load plugins from installed Python entry points.

        Entry point groups:
        - ``flowscout.reporters`` — reporter plugins
        - ``flowscout.detectors`` — outcome detector plugins
        - ``flowscout.discoverers`` — element discoverer plugins
        """
        for attr, group in _ENTRY_POINT_GROUPS.items():
            registry = getattr(self, f"_{attr}")
            eps = importlib.metadata.entry_points(group=group)
            for ep in eps:
                try:
                    cls = ep.load()
                    registry[ep.name] = cls
                    logger.debug("Loaded plugin %s from %s", ep.name, group)
                except Exception:
                    logger.warning(
                        "Failed to load plugin %s from %s",
                        ep.name,
                        group,
                        exc_info=True,
                    )

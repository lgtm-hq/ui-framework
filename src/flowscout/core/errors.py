"""Structured exception hierarchy for flowscout.

Replaces bare ``except Exception`` blocks with specific, catchable types
so callers can distinguish actionable errors from unexpected crashes.
"""

from __future__ import annotations


class FlowscoutError(Exception):
    """Base class for all flowscout-specific errors."""


# ── Browser errors ───────────────────────────────────────────────────

class BrowserError(FlowscoutError):
    """A Playwright browser operation failed."""


class NavigationError(BrowserError):
    """Failed to navigate to a URL."""


class ActionExecutionError(BrowserError):
    """Failed to execute a user-facing action (click, fill, etc.)."""


class ActionTimeoutError(ActionExecutionError):
    """An action timed out waiting for the element or DOM stability."""


class StateCaptureFailed(BrowserError):
    """Could not capture the current page state."""


class BacktrackFailed(BrowserError):
    """Failed to return to a previously visited state."""


# ── Storage errors ───────────────────────────────────────────────────

class StorageError(FlowscoutError):
    """A persistence operation failed."""


class MigrationError(StorageError):
    """A schema migration could not be applied."""


# ── Discovery errors ─────────────────────────────────────────────────

class DiscoveryError(FlowscoutError):
    """Element discovery or classification failed."""


# ── Configuration errors ─────────────────────────────────────────────

class ConfigError(FlowscoutError):
    """Invalid or missing configuration."""

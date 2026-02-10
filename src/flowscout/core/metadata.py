"""Typed accessor for Action.metadata — replaces bare .get() calls."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flowscout.discovery.actions import Action


class ActionMetadata:
    """Typed wrapper around the raw ``dict[str, str]`` stored on an Action.

    Every metadata key used anywhere in the codebase is exposed as a
    read-only property so that callers get IDE completion and grep-ability
    instead of magic-string ``.get()`` calls.
    """

    __slots__ = ("_raw",)

    def __init__(self, action: Action) -> None:
        self._raw: dict[str, str] = action.metadata or {}

    # -- Element identity (written by _element_identity_metadata) ----------

    @property
    def selector(self) -> str:
        return self._raw.get("selector", "")

    @property
    def dom_id(self) -> str:
        return self._raw.get("dom_id", "")

    @property
    def name(self) -> str:
        return self._raw.get("name", "")

    @property
    def aria_label(self) -> str:
        return self._raw.get("aria_label", "")

    # -- Click metadata ----------------------------------------------------

    @property
    def href(self) -> str:
        return self._raw.get("href", "")

    @property
    def is_search(self) -> bool:
        return self._raw.get("is_search") == "true"

    # -- Fill metadata -----------------------------------------------------

    @property
    def element_type(self) -> str:
        return self._raw.get("element_type", "")

    @property
    def input_source(self) -> str:
        return self._raw.get("input_source", "")

    @property
    def input_profile(self) -> str:
        return self._raw.get("input_profile", "")

    # -- Dropdown metadata -------------------------------------------------

    @property
    def requires_open(self) -> str:
        """CSS selector of the trigger that must be clicked before this option."""
        return self._raw.get("requires_open", "")

    # -- Form submission metadata ------------------------------------------

    @property
    def field_values(self) -> dict[str, str]:
        """Parsed field-values map (selector → value)."""
        raw = self._raw.get("field_values_json", "{}")
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}

    @property
    def field_sources(self) -> dict[str, str]:
        """Parsed field-sources map (selector → source label)."""
        raw = self._raw.get("field_sources_json", "{}")
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}

    @property
    def form_selector(self) -> str:
        return self._raw.get("form_selector", "")

    @property
    def scenario(self) -> str:
        return self._raw.get("scenario", "")

    @property
    def expected_outcome(self) -> str:
        return self._raw.get("expected_outcome", "")

    # -- Policy helpers (used by policy.py) --------------------------------

    @property
    def url(self) -> str:
        return self._raw.get("url", "")

    # -- Convenience -------------------------------------------------------

    @property
    def is_invalid_scenario(self) -> bool:
        return self.scenario == "invalid"

    @property
    def is_dropdown_option(self) -> bool:
        return bool(self.requires_open)

    def get(self, key: str, default: str = "") -> str:
        """Escape-hatch for any key not yet exposed as a property."""
        return self._raw.get(key, default)

    def __contains__(self, key: str) -> bool:
        return key in self._raw

    def __repr__(self) -> str:
        return f"ActionMetadata({self._raw!r})"

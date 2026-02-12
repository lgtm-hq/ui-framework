"""Context store for page-extracted data used in smart input generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flowscout.core.archetypes import PageAnalysis


class ContextStore:
    """Stores extracted entity names from page analysis for use as contextual inputs.

    Maintains a rotating queue of entity names so each search query is unique.
    """

    def __init__(self) -> None:
        self._entities: list[str] = []
        self._used_entities: set[str] = set()
        self._entity_index: int = 0
        self._listing_entities: list[str] = []
        self._tried_filter_values: set[str] = set()

    def extract_from(self, analysis: PageAnalysis) -> None:
        """Pull entities from a page analysis result."""
        from flowscout.core.archetypes import PageArchetype

        for entity in analysis.extracted_entities:
            normalized = entity.strip()
            if normalized and normalized.lower() not in {
                e.lower() for e in self._entities
            }:
                self._entities.append(normalized)

        # Track listing-page entities separately for higher priority
        if analysis.archetype == PageArchetype.LISTING:
            for entity in analysis.extracted_entities:
                normalized = entity.strip()
                if normalized and normalized.lower() not in {
                    e.lower() for e in self._listing_entities
                }:
                    self._listing_entities.append(normalized)

    def get_search_query(self) -> str:
        """Return an extracted entity name for search, rotating through them.

        Prefers entities from listing pages. Falls back to "test query".
        """
        # Try listing entities first
        query = self._next_unused(self._listing_entities)
        if query:
            return query

        # Try all entities
        query = self._next_unused(self._entities)
        if query:
            return query

        # Fallback
        return "test query"

    def _next_unused(self, pool: list[str]) -> str | None:
        """Get the next unused entity from a pool."""
        for entity in pool:
            if entity not in self._used_entities:
                self._used_entities.add(entity)
                return entity
        return None

    def get_filter_value(self, options: list[str]) -> str | None:
        """Return an untried filter option value."""
        for option in options:
            if option not in self._tried_filter_values:
                self._tried_filter_values.add(option)
                return option
        return None

    @property
    def entity_count(self) -> int:
        """Total number of unique entities stored."""
        return len(self._entities)

    @property
    def has_entities(self) -> bool:
        """Whether any entities have been extracted."""
        return len(self._entities) > 0

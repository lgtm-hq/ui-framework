"""Tests for the contextual input generation store."""

from __future__ import annotations


from flowscout.core.archetypes import PageAnalysis, PageArchetype
from flowscout.discovery.context import ContextStore


def _make_analysis(
    archetype: PageArchetype = PageArchetype.LISTING,
    entities: list[str] | None = None,
) -> PageAnalysis:
    return PageAnalysis(
        archetype=archetype,
        archetype_confidence=0.9,
        structural_signature="abc123",
        extracted_entities=entities or [],
    )


class TestContextStore:
    """Context store entity management."""

    def test_extract_entities(self) -> None:
        store = ContextStore()
        analysis = _make_analysis(entities=["Movie A", "Movie B", "Movie C"])
        store.extract_from(analysis)
        assert store.entity_count == 3

    def test_deduplication(self) -> None:
        store = ContextStore()
        analysis = _make_analysis(entities=["Movie A", "Movie A", "movie a"])
        store.extract_from(analysis)
        assert store.entity_count == 1

    def test_dedup_across_extractions(self) -> None:
        store = ContextStore()
        store.extract_from(_make_analysis(entities=["Movie A", "Movie B"]))
        store.extract_from(_make_analysis(entities=["Movie B", "Movie C"]))
        assert store.entity_count == 3

    def test_has_entities(self) -> None:
        store = ContextStore()
        assert store.has_entities is False
        store.extract_from(_make_analysis(entities=["X"]))
        assert store.has_entities is True


class TestSearchQuery:
    """Search query generation with rotation."""

    def test_returns_entity(self) -> None:
        store = ContextStore()
        store.extract_from(_make_analysis(entities=["Inception", "Matrix"]))
        query = store.get_search_query()
        assert query in ("Inception", "Matrix")

    def test_rotation_no_repeats(self) -> None:
        store = ContextStore()
        store.extract_from(_make_analysis(entities=["A", "B", "C"]))
        seen = set()
        for _ in range(3):
            q = store.get_search_query()
            assert q not in seen
            seen.add(q)
        assert seen == {"A", "B", "C"}

    def test_fallback_when_exhausted(self) -> None:
        store = ContextStore()
        store.extract_from(_make_analysis(entities=["X"]))
        store.get_search_query()  # Consumes "X"
        assert store.get_search_query() == "test query"

    def test_fallback_when_empty(self) -> None:
        store = ContextStore()
        assert store.get_search_query() == "test query"

    def test_prefers_listing_entities(self) -> None:
        store = ContextStore()
        # Add non-listing entities first
        store.extract_from(
            _make_analysis(archetype=PageArchetype.DETAIL, entities=["Detail Entity"])
        )
        # Add listing entities
        store.extract_from(
            _make_analysis(archetype=PageArchetype.LISTING, entities=["Listing Entity"])
        )
        query = store.get_search_query()
        assert query == "Listing Entity"


class TestFilterValue:
    """Filter value selection."""

    def test_returns_untried_option(self) -> None:
        store = ContextStore()
        val = store.get_filter_value(["Action", "Comedy", "Drama"])
        assert val == "Action"

    def test_skips_tried_options(self) -> None:
        store = ContextStore()
        store.get_filter_value(["Action", "Comedy"])
        val = store.get_filter_value(["Action", "Comedy", "Drama"])
        assert val == "Comedy"

    def test_returns_none_when_all_tried(self) -> None:
        store = ContextStore()
        store.get_filter_value(["A", "B"])
        store.get_filter_value(["A", "B"])
        assert store.get_filter_value(["A", "B"]) is None

    def test_empty_options(self) -> None:
        store = ContextStore()
        assert store.get_filter_value([]) is None

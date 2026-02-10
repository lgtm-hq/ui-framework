"""Tests for content expectation checking."""

from __future__ import annotations


from flowscout.analysis.archetype import (
    ContentDensity,
    PageAnalysis,
    PageArchetype,
    RepeatedStructure,
)
from flowscout.analysis.expectations import ExpectationChecker


def _make_analysis(
    archetype: PageArchetype,
    *,
    heading_count: int = 0,
    text_length: int = 0,
    image_count: int = 0,
    form_input_count: int = 0,
    repeated: list[RepeatedStructure] | None = None,
    has_search: bool = False,
) -> PageAnalysis:
    return PageAnalysis(
        archetype=archetype,
        archetype_confidence=0.8,
        structural_signature="test",
        content_density=ContentDensity(
            total_text_length=text_length,
            heading_count=heading_count,
            image_count=image_count,
            form_input_count=form_input_count,
            interactive_count=5,
        ),
        repeated_structures=repeated or [],
        has_search=has_search,
    )


class TestDetailExpectations:
    """Detail page expectations."""

    def test_full_detail_page(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.DETAIL,
            heading_count=2,
            text_length=1000,
            image_count=1,
        )
        result = checker.check(analysis)
        assert result.pass_count == 3
        assert result.total_count == 3

    def test_detail_missing_image(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.DETAIL,
            heading_count=1,
            text_length=500,
            image_count=0,
        )
        result = checker.check(analysis)
        assert result.pass_count == 2
        assert result.total_count == 3

    def test_detail_no_content(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(PageArchetype.DETAIL)
        result = checker.check(analysis)
        assert result.pass_count == 0

    def test_detail_short_text(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.DETAIL,
            heading_count=1,
            text_length=100,
            image_count=1,
        )
        result = checker.check(analysis)
        # heading met, text not met (<200), image met
        assert result.pass_count == 2


class TestListingExpectations:
    """Listing page expectations."""

    def test_listing_with_items(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.LISTING,
            repeated=[
                RepeatedStructure(
                    container_selector=".grid",
                    item_count=10,
                    tag_signature="div>a>h3",
                ),
            ],
        )
        result = checker.check(analysis)
        assert result.pass_count == 2
        assert result.total_count == 2

    def test_listing_no_items(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(PageArchetype.LISTING)
        result = checker.check(analysis)
        assert result.pass_count == 0


class TestSearchResultsExpectations:
    """Search results page expectations."""

    def test_search_with_results(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.SEARCH_RESULTS,
            has_search=True,
            repeated=[
                RepeatedStructure(
                    container_selector=".results",
                    item_count=5,
                    tag_signature="div>h3+p",
                ),
            ],
        )
        result = checker.check(analysis)
        assert result.pass_count == 2

    def test_search_no_results(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.SEARCH_RESULTS,
            has_search=True,
        )
        result = checker.check(analysis)
        assert result.pass_count == 1  # Only search input met


class TestFormExpectations:
    """Form page expectations."""

    def test_form_with_inputs(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.FORM,
            form_input_count=4,
            heading_count=1,
        )
        result = checker.check(analysis)
        assert result.pass_count == 2

    def test_form_no_heading(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.FORM,
            form_input_count=3,
            heading_count=0,
        )
        result = checker.check(analysis)
        assert result.pass_count == 1


class TestUnknownArchetype:
    """Unknown archetype has no expectations."""

    def test_unknown_no_expectations(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(PageArchetype.UNKNOWN)
        result = checker.check(analysis)
        assert result.total_count == 0
        assert "No expectations" in result.summary


class TestSummary:
    """Summary string generation."""

    def test_summary_format(self) -> None:
        checker = ExpectationChecker()
        analysis = _make_analysis(
            PageArchetype.DETAIL,
            heading_count=1,
            text_length=300,
            image_count=1,
        )
        result = checker.check(analysis)
        assert "3/3" in result.summary
        assert "detail" in result.summary

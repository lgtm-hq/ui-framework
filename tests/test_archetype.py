"""Tests for page archetype classification, structural signatures, and registry."""

from __future__ import annotations

from typing import Any

import pytest

from flowscout.core.archetypes import (
    ArchetypeRegistry,
    PageAnalysis,
    PageArchetype,
    ZoneType,
    build_page_analysis,
    classify_archetype,
    compute_structural_signature,
    _generate_semantic_name,
)

# ---------------------------------------------------------------------------
# Helpers — mock raw dicts
# ---------------------------------------------------------------------------


def _listing_raw(
    item_count: int = 12, has_pagination: bool = True, has_filters: bool = False
) -> dict[str, Any]:
    return {
        "repeated_groups": [
            {
                "parent_selector": ".grid",
                "count": item_count,
                "tag_signature": "div>a>img+div>h3+p",
                "item_texts": [f"Item {i}" for i in range(min(item_count, 10))],
                "item_selectors": [
                    f".grid > div:nth-of-type({i})" for i in range(1, 4)
                ],
            }
        ],
        "content_metrics": {
            "total_text_length": 3000,
            "heading_count": 2,
            "h1_texts": ["All Products"],
            "h2_texts": [],
            "image_count": item_count,
            "link_count": item_count + 5,
            "form_input_count": 0,
            "interactive_count": item_count + 10,
        },
        "zone_hints": {
            "has_nav": True,
            "has_search_input": False,
            "has_pagination": has_pagination,
            "has_filters": has_filters,
            "has_hero": False,
            "has_single_heading_focus": False,
        },
        "structural_skeleton": "main(div(div,div,div,div),nav)",
        "extracted_entities": [f"Item {i}" for i in range(10)],
        "element_catalog": [],
    }


def _detail_raw() -> dict[str, Any]:
    return {
        "repeated_groups": [],
        "content_metrics": {
            "total_text_length": 2000,
            "heading_count": 3,
            "h1_texts": ["The Shawshank Redemption"],
            "h2_texts": ["Synopsis", "Cast"],
            "image_count": 2,
            "link_count": 5,
            "form_input_count": 0,
            "interactive_count": 8,
        },
        "zone_hints": {
            "has_nav": True,
            "has_search_input": False,
            "has_pagination": False,
            "has_filters": False,
            "has_hero": False,
            "has_single_heading_focus": True,
        },
        "structural_skeleton": "main(article(h1,img,div(p,p)),aside(h2,ul))",
        "extracted_entities": ["Synopsis", "Cast"],
        "element_catalog": [],
    }


def _form_raw(input_count: int = 5) -> dict[str, Any]:
    return {
        "repeated_groups": [],
        "content_metrics": {
            "total_text_length": 300,
            "heading_count": 1,
            "h1_texts": ["Register"],
            "h2_texts": [],
            "image_count": 0,
            "link_count": 2,
            "form_input_count": input_count,
            "interactive_count": input_count + 2,
        },
        "zone_hints": {
            "has_nav": True,
            "has_search_input": False,
            "has_pagination": False,
            "has_filters": False,
            "has_hero": False,
            "has_single_heading_focus": False,
        },
        "structural_skeleton": "main(form(div,div,div,button))",
        "extracted_entities": [],
        "element_catalog": [],
    }


def _search_results_raw() -> dict[str, Any]:
    return {
        "repeated_groups": [
            {
                "parent_selector": ".results",
                "count": 8,
                "tag_signature": "div>a>h3+p",
                "item_texts": [f"Result {i}" for i in range(8)],
                "item_selectors": [".results > div:nth-of-type(1)"],
            }
        ],
        "content_metrics": {
            "total_text_length": 2500,
            "heading_count": 9,
            "h1_texts": ["Search Results"],
            "h2_texts": [],
            "image_count": 0,
            "link_count": 15,
            "form_input_count": 1,
            "interactive_count": 20,
        },
        "zone_hints": {
            "has_nav": True,
            "has_search_input": True,
            "has_pagination": True,
            "has_filters": False,
            "has_hero": False,
            "has_single_heading_focus": False,
        },
        "structural_skeleton": "main(div(input),div(div,div,div,div),nav)",
        "extracted_entities": [f"Result {i}" for i in range(8)],
        "element_catalog": [],
    }


def _landing_raw() -> dict[str, Any]:
    return {
        "repeated_groups": [
            {
                "parent_selector": ".features",
                "count": 3,
                "tag_signature": "div>h3+p+a",
                "item_texts": ["Feature A", "Feature B", "Feature C"],
                "item_selectors": [".features > div:nth-of-type(1)"],
            }
        ],
        "content_metrics": {
            "total_text_length": 1500,
            "heading_count": 5,
            "h1_texts": ["Welcome to App"],
            "h2_texts": ["Features", "Pricing", "Testimonials"],
            "image_count": 4,
            "link_count": 10,
            "form_input_count": 0,
            "interactive_count": 12,
        },
        "zone_hints": {
            "has_nav": True,
            "has_search_input": False,
            "has_pagination": False,
            "has_filters": False,
            "has_hero": True,
            "has_single_heading_focus": True,
        },
        "structural_skeleton": "main(section(h1,p,a),section(div,div,div))",
        "extracted_entities": ["Feature A", "Feature B", "Feature C"],
        "element_catalog": [],
    }


def _error_raw() -> dict[str, Any]:
    return {
        "repeated_groups": [],
        "content_metrics": {
            "total_text_length": 100,
            "heading_count": 1,
            "h1_texts": ["404 Not Found"],
            "h2_texts": [],
            "image_count": 0,
            "link_count": 1,
            "form_input_count": 0,
            "interactive_count": 1,
        },
        "zone_hints": {
            "has_nav": False,
            "has_search_input": False,
            "has_pagination": False,
            "has_filters": False,
            "has_hero": False,
            "has_single_heading_focus": True,
        },
        "structural_skeleton": "main(h1,p,a)",
        "extracted_entities": [],
        "element_catalog": [],
    }


def _empty_raw() -> dict[str, Any]:
    return {
        "repeated_groups": [],
        "content_metrics": {
            "total_text_length": 0,
            "heading_count": 0,
            "h1_texts": [],
            "h2_texts": [],
            "image_count": 0,
            "link_count": 0,
            "form_input_count": 0,
            "interactive_count": 0,
        },
        "zone_hints": {
            "has_nav": False,
            "has_search_input": False,
            "has_pagination": False,
            "has_filters": False,
            "has_hero": False,
            "has_single_heading_focus": False,
        },
        "structural_skeleton": "",
        "extracted_entities": [],
        "element_catalog": [],
    }


# ---------------------------------------------------------------------------
# TestClassifyArchetype
# ---------------------------------------------------------------------------


class TestClassifyArchetype:
    """Parametrized archetype classification tests."""

    @pytest.mark.parametrize(
        "raw_factory,expected_archetype",
        [
            (_listing_raw, PageArchetype.LISTING),
            (_detail_raw, PageArchetype.DETAIL),
            (_form_raw, PageArchetype.FORM),
            (_search_results_raw, PageArchetype.SEARCH_RESULTS),
            (_error_raw, PageArchetype.ERROR),
        ],
    )
    def test_primary_archetype(
        self, raw_factory: Any, expected_archetype: PageArchetype
    ) -> None:
        raw = raw_factory()
        archetype, confidence = classify_archetype(raw)
        assert archetype == expected_archetype
        assert confidence > 0

    def test_listing_with_many_items(self) -> None:
        raw = _listing_raw(item_count=20, has_pagination=True, has_filters=True)
        archetype, confidence = classify_archetype(raw)
        assert archetype == PageArchetype.LISTING
        assert confidence > 0.3

    def test_listing_without_pagination(self) -> None:
        raw = _listing_raw(item_count=8, has_pagination=False)
        archetype, _ = classify_archetype(raw)
        assert archetype == PageArchetype.LISTING

    def test_form_with_many_inputs(self) -> None:
        raw = _form_raw(input_count=8)
        archetype, confidence = classify_archetype(raw)
        assert archetype == PageArchetype.FORM
        assert confidence > 0.3

    def test_empty_page_is_unknown(self) -> None:
        raw = _empty_raw()
        archetype, confidence = classify_archetype(raw)
        assert archetype == PageArchetype.UNKNOWN
        assert confidence == 0.0

    def test_confidence_is_normalized(self) -> None:
        raw = _listing_raw()
        _, confidence = classify_archetype(raw)
        assert 0.0 <= confidence <= 1.0

    def test_detail_with_long_text(self) -> None:
        raw = _detail_raw()
        raw["content_metrics"]["total_text_length"] = 5000
        archetype, _ = classify_archetype(raw)
        assert archetype == PageArchetype.DETAIL

    def test_search_results_with_search_and_results(self) -> None:
        raw = _search_results_raw()
        archetype, _ = classify_archetype(raw)
        assert archetype == PageArchetype.SEARCH_RESULTS

    def test_landing_with_hero(self) -> None:
        raw = _landing_raw()
        archetype, _ = classify_archetype(raw)
        assert archetype == PageArchetype.LANDING


# ---------------------------------------------------------------------------
# TestStructuralSignature
# ---------------------------------------------------------------------------


class TestStructuralSignature:
    """Structural signature computation."""

    def test_same_structure_same_sig(self) -> None:
        skeleton_a = "main(div(h1,img,p),aside(h2,ul))"
        skeleton_b = "main(div(h1,img,p),aside(h2,ul))"
        assert compute_structural_signature(skeleton_a) == compute_structural_signature(
            skeleton_b
        )

    def test_different_structure_different_sig(self) -> None:
        skeleton_a = "main(div(h1,img,p),aside(h2,ul))"
        skeleton_b = "main(section(h1,p),div(div,div))"
        assert compute_structural_signature(skeleton_a) != compute_structural_signature(
            skeleton_b
        )

    def test_signature_is_16_hex_chars(self) -> None:
        sig = compute_structural_signature("main(div(h1,p))")
        assert len(sig) == 16
        assert all(c in "0123456789abcdef" for c in sig)

    def test_empty_skeleton(self) -> None:
        sig = compute_structural_signature("")
        assert len(sig) == 16


# ---------------------------------------------------------------------------
# TestArchetypeRegistry
# ---------------------------------------------------------------------------


class TestArchetypeRegistry:
    """Registry tracking and saturation."""

    def _make_analysis(self, skeleton: str = "main(div)") -> PageAnalysis:
        return PageAnalysis(
            archetype=PageArchetype.LISTING,
            archetype_confidence=0.8,
            structural_signature=compute_structural_signature(skeleton),
        )

    def test_first_instance_is_novel(self) -> None:
        reg = ArchetypeRegistry()
        analysis = self._make_analysis()
        assert reg.register("s1", analysis) is True

    def test_second_instance_is_not_novel(self) -> None:
        reg = ArchetypeRegistry()
        analysis = self._make_analysis()
        reg.register("s1", analysis)
        assert reg.register("s2", analysis) is False

    def test_saturation_at_threshold(self) -> None:
        reg = ArchetypeRegistry(saturation_threshold=3)
        analysis = self._make_analysis()
        sig = analysis.structural_signature
        reg.register("s1", analysis)
        reg.register("s2", analysis)
        assert reg.is_saturated(sig) is False
        reg.register("s3", analysis)
        assert reg.is_saturated(sig) is True

    def test_instance_count(self) -> None:
        reg = ArchetypeRegistry()
        analysis = self._make_analysis()
        sig = analysis.structural_signature
        assert reg.instance_count(sig) == 0
        reg.register("s1", analysis)
        assert reg.instance_count(sig) == 1
        reg.register("s2", analysis)
        assert reg.instance_count(sig) == 2

    def test_different_signatures_independent(self) -> None:
        reg = ArchetypeRegistry(saturation_threshold=2)
        a1 = self._make_analysis("main(div)")
        a2 = self._make_analysis("main(section)")
        reg.register("s1", a1)
        reg.register("s2", a1)
        reg.register("s3", a2)
        assert reg.is_saturated(a1.structural_signature) is True
        assert reg.is_saturated(a2.structural_signature) is False

    def test_archetype_distribution(self) -> None:
        reg = ArchetypeRegistry()
        a1 = self._make_analysis("main(div)")
        reg.register("s1", a1)
        reg.register("s2", a1)
        dist = reg.archetype_distribution()
        assert dist["listing"] == 2

    def test_all_signatures(self) -> None:
        reg = ArchetypeRegistry()
        a1 = self._make_analysis("main(div)")
        a2 = self._make_analysis("main(section)")
        reg.register("s1", a1)
        reg.register("s2", a2)
        sigs = reg.all_signatures()
        assert len(sigs) == 2


# ---------------------------------------------------------------------------
# TestPageCatalog
# ---------------------------------------------------------------------------


class TestPageCatalog:
    """Catalog entry generation and zone grouping."""

    def test_catalog_from_raw_data(self) -> None:
        raw = _listing_raw()
        raw["element_catalog"] = [
            {
                "selector": "a[href='/home']",
                "dom_id": "home-link",
                "tag": "a",
                "label": "Home",
                "zone": "navigation",
                "element_type": "link",
                "aria_role": "",
                "input_type": "",
                "is_visible": True,
                "bounding_box": {"x": 0, "y": 0, "width": 100, "height": 30},
            },
            {
                "selector": "input[type='search']",
                "tag": "input",
                "label": "",
                "zone": "search",
                "element_type": "input_search",
                "aria_role": "",
                "input_type": "search",
                "is_visible": False,
                "bounding_box": None,
            },
            {
                "selector": ".movie-card:nth-of-type(1)",
                "tag": "div",
                "label": "Movie 1",
                "zone": "main_content",
                "element_type": "other",
                "aria_role": "",
                "input_type": "",
                "bounding_box": None,
            },
        ]

        analysis = build_page_analysis(raw)
        catalog = analysis.catalog

        assert catalog.archetype == PageArchetype.LISTING
        assert len(catalog.entries) == 3
        assert catalog.entries[0].dom_id == "home-link"
        assert catalog.entries[1].is_visible is False

        nav_entries = [e for e in catalog.entries if e.zone_type == ZoneType.NAVIGATION]
        assert len(nav_entries) == 1

        search_entries = [e for e in catalog.entries if e.zone_type == ZoneType.SEARCH]
        assert len(search_entries) == 1

    def test_semantic_name_from_label(self) -> None:
        name = _generate_semantic_name("a[href='/about']", "About Us", "a")
        assert name == "about_us"

    def test_semantic_name_from_aria_label(self) -> None:
        name = _generate_semantic_name("[aria-label='Search']", "", "button")
        assert name == "search"

    def test_semantic_name_fallback_to_tag(self) -> None:
        name = _generate_semantic_name("div:nth-of-type(3)", "", "div")
        assert name.startswith("div")

    def test_semantic_name_max_length(self) -> None:
        long_label = "A" * 100
        name = _generate_semantic_name("div", long_label, "div")
        assert len(name) <= 40


# ---------------------------------------------------------------------------
# TestBuildPageAnalysis
# ---------------------------------------------------------------------------


class TestBuildPageAnalysis:
    """Integration test for build_page_analysis."""

    def test_listing_analysis(self) -> None:
        raw = _listing_raw()
        analysis = build_page_analysis(raw)
        assert analysis.archetype == PageArchetype.LISTING
        assert analysis.archetype_confidence > 0
        assert len(analysis.structural_signature) == 16
        assert analysis.has_pagination is True
        assert len(analysis.repeated_structures) == 1
        assert analysis.repeated_structures[0].item_count == 12

    def test_detail_analysis(self) -> None:
        raw = _detail_raw()
        analysis = build_page_analysis(raw)
        assert analysis.archetype == PageArchetype.DETAIL
        assert len(analysis.heading_hierarchy) > 0

    def test_content_density(self) -> None:
        raw = _listing_raw()
        analysis = build_page_analysis(raw)
        assert analysis.content_density.total_text_length == 3000
        assert analysis.content_density.interactive_count > 0
        assert analysis.content_density.text_to_interactive_ratio > 0

    def test_extracted_entities(self) -> None:
        raw = _listing_raw()
        analysis = build_page_analysis(raw)
        assert len(analysis.extracted_entities) > 0
        assert "Item 0" in analysis.extracted_entities

    def test_zones_populated(self) -> None:
        raw = _listing_raw()
        raw["element_catalog"] = [
            {
                "selector": "a[href='/home']",
                "tag": "a",
                "label": "Home",
                "zone": "navigation",
                "element_type": "link",
                "aria_role": "",
                "input_type": "",
                "bounding_box": None,
            },
        ]
        analysis = build_page_analysis(raw)
        assert len(analysis.zones) > 0

    def test_empty_raw_data(self) -> None:
        raw = _empty_raw()
        analysis = build_page_analysis(raw)
        assert analysis.archetype == PageArchetype.UNKNOWN
        assert analysis.archetype_confidence == 0.0

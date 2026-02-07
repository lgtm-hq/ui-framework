"""Tests for the site model builder."""

from flowscout.analysis.archetype import (
    CatalogEntry,
    PageAnalysis,
    PageArchetype,
    PageCatalog,
    ZoneType,
)
from flowscout.analysis.graph import ExplorationResult
from flowscout.analysis.site_model import (
    SiteModel,
    SiteModelBuilder,
    _common_subject_from_titles,
    _infer_page_type_name,
    _infer_url_pattern,
    _url_to_template,
)
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state(
    state_id: str, url: str = "https://example.com", title: str = "",
) -> PageState:
    return PageState(
        state_id=state_id,
        url=url,
        title=title or f"Page {state_id}",
        fingerprint=state_id * 6,
        depth=0,
        dom_structure_hash="dom",
        visible_text_hash="text",
        form_state_hash="form",
    )


def _make_analysis(
    archetype: PageArchetype = PageArchetype.LISTING,
    signature: str = "sig_a",
    has_search: bool = False,
    has_pagination: bool = False,
    has_filters: bool = False,
) -> PageAnalysis:
    return PageAnalysis(
        archetype=archetype,
        archetype_confidence=0.8,
        structural_signature=signature,
        has_search=has_search,
        has_pagination=has_pagination,
        has_filters=has_filters,
        catalog=PageCatalog(
            archetype=archetype,
            url_pattern="",
            entries=[
                CatalogEntry(
                    selector="a.item",
                    tag="a",
                    label="Item link",
                    zone_type=ZoneType.MAIN_CONTENT,
                    element_type="link",
                    semantic_name="item_link",
                ),
            ],
        ),
    )


def _make_result(
    result: ExplorationResult | None = None,
    states: dict[str, PageState] | None = None,
    actions: dict[str, Action] | None = None,
    results: list[ActionResult] | None = None,
    smart_analyses: dict | None = None,
) -> ExplorationResult:
    return ExplorationResult(
        states=states or {},
        actions=actions or {},
        results=results or [],
        smart_analyses=smart_analyses or {},
    )


# ---------------------------------------------------------------------------
# Tests: page type grouping
# ---------------------------------------------------------------------------


class TestPageTypeGrouping:
    def test_states_with_same_signature_form_one_page_type(self):
        s1 = _make_state("s1", url="https://example.com/products?page=1", title="Products")
        s2 = _make_state("s2", url="https://example.com/products?page=2", title="Products")

        analyses = {
            "s1": _make_analysis(PageArchetype.LISTING, "sig_a"),
            "s2": _make_analysis(PageArchetype.LISTING, "sig_a"),
        }

        result = _make_result(states={"s1": s1, "s2": s2})
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        assert len(model.page_types) == 1
        assert model.page_types[0].instance_count == 2
        assert model.page_types[0].archetype == PageArchetype.LISTING

    def test_different_signatures_form_different_page_types(self):
        s1 = _make_state("s1", url="https://example.com/products")
        s2 = _make_state("s2", url="https://example.com/product/1")

        analyses = {
            "s1": _make_analysis(PageArchetype.LISTING, "sig_a"),
            "s2": _make_analysis(PageArchetype.DETAIL, "sig_b"),
        }

        result = _make_result(states={"s1": s1, "s2": s2})
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        assert len(model.page_types) == 2
        archetypes = {pt.archetype for pt in model.page_types}
        assert archetypes == {PageArchetype.LISTING, PageArchetype.DETAIL}

    def test_features_extracted_from_analysis(self):
        s1 = _make_state("s1")
        analyses = {
            "s1": _make_analysis(
                PageArchetype.LISTING,
                "sig_a",
                has_search=True,
                has_pagination=True,
            ),
        }

        result = _make_result(states={"s1": s1})
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        features = model.page_types[0].features
        assert "has_search" in features
        assert "has_pagination" in features

    def test_build_without_analyses_uses_url_fallback(self):
        s1 = _make_state("s1", url="https://example.com/products")
        s2 = _make_state("s2", url="https://example.com/about")

        result = _make_result(states={"s1": s1, "s2": s2})
        builder = SiteModelBuilder()
        model = builder.build(result, None)

        assert len(model.page_types) == 2


# ---------------------------------------------------------------------------
# Tests: navigation edges
# ---------------------------------------------------------------------------


class TestNavigationEdges:
    def test_cross_page_type_transition_creates_edge(self):
        s1 = _make_state("s1", url="https://example.com/products")
        s2 = _make_state("s2", url="https://example.com/product/1")
        action = Action(
            action_id="a1",
            action_type=ActionType.CLICK,
            target_selector="a.item",
            label="Click product",
        )
        action_result = ActionResult(
            action_id="a1",
            source_state_id="s1",
            target_state_id="s2",
            outcome=OutcomeType.NAVIGATION,
        )

        analyses = {
            "s1": _make_analysis(PageArchetype.LISTING, "sig_a"),
            "s2": _make_analysis(PageArchetype.DETAIL, "sig_b"),
        }

        result = _make_result(
            states={"s1": s1, "s2": s2},
            actions={"a1": action},
            results=[action_result],
        )
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        assert len(model.navigation_edges) == 1
        edge = model.navigation_edges[0]
        assert edge.from_page_type == "sig_a"
        assert edge.to_page_type == "sig_b"
        assert edge.trigger == "Click product"

    def test_same_page_type_transition_ignored(self):
        s1 = _make_state("s1", url="https://example.com/products?page=1")
        s2 = _make_state("s2", url="https://example.com/products?page=2")
        action = Action(
            action_id="a1",
            action_type=ActionType.CLICK,
            target_selector="a.next",
            label="Next page",
        )
        action_result = ActionResult(
            action_id="a1",
            source_state_id="s1",
            target_state_id="s2",
            outcome=OutcomeType.NAVIGATION,
        )

        analyses = {
            "s1": _make_analysis(PageArchetype.LISTING, "sig_a"),
            "s2": _make_analysis(PageArchetype.LISTING, "sig_a"),
        }

        result = _make_result(
            states={"s1": s1, "s2": s2},
            actions={"a1": action},
            results=[action_result],
        )
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        assert len(model.navigation_edges) == 0

    def test_edges_deduplicated_with_count(self):
        s1 = _make_state("s1")
        s2 = _make_state("s2")
        s3 = _make_state("s3")

        a1 = Action(action_id="a1", action_type=ActionType.CLICK, target_selector="a", label="Item 1")
        a2 = Action(action_id="a2", action_type=ActionType.CLICK, target_selector="a", label="Item 2")

        r1 = ActionResult(action_id="a1", source_state_id="s1", target_state_id="s2", outcome=OutcomeType.NAVIGATION)
        r2 = ActionResult(action_id="a2", source_state_id="s3", target_state_id="s2", outcome=OutcomeType.NAVIGATION)

        analyses = {
            "s1": _make_analysis(PageArchetype.LISTING, "sig_a"),
            "s2": _make_analysis(PageArchetype.DETAIL, "sig_b"),
            "s3": _make_analysis(PageArchetype.LISTING, "sig_a"),
        }

        result = _make_result(
            states={"s1": s1, "s2": s2, "s3": s3},
            actions={"a1": a1, "a2": a2},
            results=[r1, r2],
        )
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        click_edges = [e for e in model.navigation_edges if e.action_type == ActionType.CLICK]
        assert len(click_edges) == 1
        assert click_edges[0].occurrence_count == 2

    def test_timeout_results_filtered_out(self):
        s1 = _make_state("s1")
        s2 = _make_state("s2")
        action = Action(action_id="a1", action_type=ActionType.CLICK, target_selector="a", label="Click")
        action_result = ActionResult(
            action_id="a1", source_state_id="s1", target_state_id="s2", outcome=OutcomeType.TIMEOUT,
        )

        analyses = {
            "s1": _make_analysis(PageArchetype.LISTING, "sig_a"),
            "s2": _make_analysis(PageArchetype.DETAIL, "sig_b"),
        }

        result = _make_result(
            states={"s1": s1, "s2": s2},
            actions={"a1": action},
            results=[action_result],
        )
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        assert len(model.navigation_edges) == 0


# ---------------------------------------------------------------------------
# Tests: URL pattern inference
# ---------------------------------------------------------------------------


class TestUrlPatternInference:
    def test_single_url_uses_literal(self):
        pattern = _infer_url_pattern(["https://example.com/products"])
        assert "products" in pattern

    def test_varying_segment_becomes_wildcard(self):
        urls = [
            "https://example.com/products/1",
            "https://example.com/products/2",
            "https://example.com/products/3",
        ]
        pattern = _infer_url_pattern(urls)
        assert "[^/]+" in pattern
        assert "products" in pattern

    def test_common_prefix_preserved(self):
        urls = [
            "https://example.com/shop/items/a",
            "https://example.com/shop/items/b",
        ]
        pattern = _infer_url_pattern(urls)
        assert "shop" in pattern
        assert "items" in pattern

    def test_empty_urls(self):
        assert _infer_url_pattern([]) == ""


# ---------------------------------------------------------------------------
# Tests: name inference
# ---------------------------------------------------------------------------


class TestNameInference:
    def test_common_subject_from_titles(self):
        subject = _common_subject_from_titles(["Movies - Popular", "Movies - Top Rated"])
        assert subject.lower() == "movies"

    def test_fallback_to_archetype(self):
        name = _infer_page_type_name(
            PageArchetype.LISTING, [], [], [],
        )
        assert name == "Listing"

    def test_subject_from_url(self):
        name = _infer_page_type_name(
            PageArchetype.DETAIL,
            ["https://example.com/products/1"],
            [],
            [],
        )
        assert "Products" in name or "Detail" in name


# ---------------------------------------------------------------------------
# Tests: URL template (fallback mode)
# ---------------------------------------------------------------------------


class TestUrlTemplate:
    def test_numeric_id_replaced(self):
        template = _url_to_template("https://example.com/products/123")
        assert "{id}" in template
        assert "products" in template

    def test_static_path_preserved(self):
        template = _url_to_template("https://example.com/about")
        assert "about" in template
        assert "{id}" not in template


# ---------------------------------------------------------------------------
# Tests: summary
# ---------------------------------------------------------------------------


class TestSiteModelSummary:
    def test_summary_counts(self):
        s1 = _make_state("s1")
        s2 = _make_state("s2")
        analyses = {
            "s1": _make_analysis(PageArchetype.LISTING, "sig_a"),
            "s2": _make_analysis(PageArchetype.DETAIL, "sig_b"),
        }
        action = Action(action_id="a1", action_type=ActionType.CLICK, target_selector="a", label="Click")
        action_result = ActionResult(
            action_id="a1", source_state_id="s1", target_state_id="s2", outcome=OutcomeType.NAVIGATION,
        )
        result = _make_result(
            states={"s1": s1, "s2": s2},
            actions={"a1": action},
            results=[action_result],
        )
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        assert model.summary.total_page_types == 2
        assert model.summary.total_navigation_edges == 1
        assert model.summary.total_scenarios > 0


# ---------------------------------------------------------------------------
# Tests: serialization round-trip
# ---------------------------------------------------------------------------


class TestSiteModelSerialization:
    def test_round_trip_json(self):
        s1 = _make_state("s1")
        analyses = {"s1": _make_analysis(PageArchetype.LISTING, "sig_a")}
        result = _make_result(states={"s1": s1})

        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        json_str = model.model_dump_json()
        restored = SiteModel.model_validate_json(json_str)

        assert len(restored.page_types) == len(model.page_types)
        assert restored.summary.total_page_types == model.summary.total_page_types

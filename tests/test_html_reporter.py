"""Tests for HTML report helper utilities."""

import os
import re
from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.state import PageBlockReason, PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.reporting.html import (
    HTMLReporter,
    _build_blocked_states,
    _build_cross_run_comparison,
    _build_dashboard_top_issues,
    _build_diagnostics,
    _build_human_execution_rows,
    _build_timeline_sentence,
    _build_flow_instance_cards,
    _build_flow_template_cards,
    _build_graph_data,
    _build_page_object_cards,
    _build_quality_insights,
    _build_site_model,
    _build_site_structure_summary,
    _build_execution_rows,
    _build_flow_execution_map,
    _human_action_label,
    _human_outcome_label,
    _build_locator_quality_data,
    _build_mbt_coverage_data,
    _to_report_asset_href,
)
from flowscout.storage.db import FlowscoutDB


def test_to_report_asset_href_none() -> None:
    report_dir = Path("/tmp/reports/run")  # nosec B108 - test fixture path
    assert _to_report_asset_href(None, report_dir=report_dir) is None


def test_to_report_asset_href_relative_path() -> None:
    report_dir = Path("/tmp/reports/run")  # nosec B108 - test fixture path
    href = _to_report_asset_href("evidence/actions/a.png", report_dir=report_dir)
    assert href == "evidence/actions/a.png"


def test_to_report_asset_href_inside_report_dir() -> None:
    report_dir = Path("/tmp/reports/run")  # nosec B108 - test fixture path
    path = report_dir / "evidence" / "actions" / "shot.png"
    href = _to_report_asset_href(str(path), report_dir=report_dir)
    assert href == "evidence/actions/shot.png"


def test_to_report_asset_href_outside_report_dir() -> None:
    report_dir = Path("/tmp/reports/run")  # nosec B108 - test fixture path
    path = Path("/tmp/other/location/shot.png")  # nosec B108 - test fixture path
    href = _to_report_asset_href(str(path), report_dir=report_dir)
    assert href == path.as_uri()


def test_to_report_asset_href_cwd_relative_run_path(tmp_path: Path) -> None:
    run_dir = (
        tmp_path / "reports" / "site" / "baseline" / "runs" / "2026-02-09_00.00.00"
    )
    evidence = run_dir / "evidence" / "actions" / "shot.png"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text("fake")

    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        href = _to_report_asset_href(
            "reports/site/baseline/runs/2026-02-09_00.00.00/evidence/actions/shot.png",
            report_dir=run_dir,
        )
    finally:
        os.chdir(cwd)

    assert href == "evidence/actions/shot.png"


def test_build_blocked_states_rows_include_reason_detail_and_screenshot() -> None:
    report_dir = Path("/tmp/reports/run")  # nosec B108 - test fixture path
    blocked_state = PageState(
        state_id="state-blocked",
        url="https://example.com/secure",
        title="Access Denied",
        fingerprint="a" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
        block_reason=PageBlockReason.ACCESS_DENIED,
        block_detail="HTTP 403 response from page navigation",
        screenshot_path="/tmp/reports/run/evidence/actions/blocked.png",  # nosec B108
    )
    result = ExplorationResult(states={"state-blocked": blocked_state})

    rows = _build_blocked_states(result=result, report_dir=report_dir)

    assert len(rows) == 1
    assert rows[0]["reason"] == "access_denied"
    assert rows[0]["reason_label"] == "Access Denied"
    assert "403" in rows[0]["detail"]
    assert rows[0]["screenshot_link"] == "evidence/actions/blocked.png"


def test_build_flow_execution_map_assigns_rows_to_flow_steps() -> None:
    state_home = PageState(
        state_id="state-home",
        url="https://example.com/",
        title="Home",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
    )
    state_detail = PageState(
        state_id="state-detail",
        url="https://example.com/detail",
        title="Detail",
        fingerprint="e" * 64,
        depth=1,
        dom_structure_hash="dom2",
        visible_text_hash="text2",
        form_state_hash="form2",
    )
    action_open = Action(
        action_id="action-open",
        action_type=ActionType.CLICK,
        target_selector="a[href='/detail']",
        label="Open detail",
    )
    result_open = ActionResult(
        action_id="action-open",
        source_state_id="state-home",
        target_state_id="state-detail",
        outcome=OutcomeType.NAVIGATION,
        stability_score=0.95,
    )
    flow = Flow(
        flow_id="flow-1",
        name="Home to Detail",
        description="Open detail",
        state_ids=["state-home", "state-detail"],
        action_ids=["action-open"],
        outcomes=[OutcomeType.NAVIGATION],
        depth=1,
    )
    result = ExplorationResult(
        states={"state-home": state_home, "state-detail": state_detail},
        actions={"action-open": action_open},
        results=[result_open],
        flows=[flow],
    )

    execution_rows = _build_execution_rows(
        result=result,
        action_labels={"action-open": "Open detail"},
        action_selectors={"action-open": "a[href='/detail']"},
        action_metadata={"action-open": {}},
        screenshot_links=[None],
    )
    flow_execution_map, orphan_rows, step_map = _build_flow_execution_map(
        result=result,
        execution_rows=execution_rows,
    )

    assert "flow-1" in flow_execution_map
    assert len(flow_execution_map["flow-1"]) == 1
    assert flow_execution_map["flow-1"][0]["flow_step"] == 1
    assert flow_execution_map["flow-1"][0]["source_page"] == "Home"
    assert flow_execution_map["flow-1"][0]["target_page"] == "Detail"
    assert orphan_rows == []
    assert step_map == {
        1: {
            "flow_id": "flow-1",
            "flow_name": "Home to Detail",
            "flow_step": 1,
        }
    }


def test_build_locator_quality_data_uses_site_model_scoring() -> None:
    state_home = PageState(
        state_id="state-home",
        url="https://example.com/",
        title="Home",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
    )
    result = ExplorationResult(
        states={"state-home": state_home},
        smart_analyses={
            "state-home": {
                "archetype": "listing",
                "archetype_confidence": 0.8,
                "structural_signature": "sig-home",
                "zones": [],
                "repeated_structures": [],
                "content_density": {
                    "total_text_length": 0,
                    "heading_count": 0,
                    "image_count": 0,
                    "link_count": 0,
                    "form_input_count": 0,
                    "interactive_count": 0,
                    "text_to_interactive_ratio": 0.0,
                },
                "extracted_entities": [],
                "has_search": False,
                "has_pagination": False,
                "has_filters": False,
                "heading_hierarchy": [],
                "catalog": {
                    "archetype": "listing",
                    "url_pattern": "/",
                    "entries": [
                        {
                            "selector": "main > div:nth-of-type(2) > button",
                            "xpath": "/html/body/main/div[2]/button",
                            "tag": "button",
                            "label": "Open",
                            "zone_type": "main_content",
                            "element_type": "button",
                        }
                    ],
                },
            }
        },
    )

    rows, recommendations = _build_locator_quality_data(result=result)
    assert len(rows) == 1
    assert rows[0]["quality_text"] == "Locator Quality: 20% stable"
    assert recommendations


def test_human_outcome_label_uses_plain_english_copy() -> None:
    assert _human_outcome_label("navigation") == "Opened a new page"
    assert _human_outcome_label("dom_change") == "Updated this page"
    assert _human_outcome_label("no_change") == "No visible change"


def test_human_action_label_strips_technical_prefixes() -> None:
    assert _human_action_label("Click: Open movie") == "Open movie"
    assert _human_action_label("Fill: Search = 'foo'") == "Search = 'foo'"
    assert _human_action_label("Custom action") == "Custom action"


def test_build_timeline_sentence_is_human_readable() -> None:
    sentence = _build_timeline_sentence(
        source_page="Home",
        action_label="Click: Browse catalog",
        target_page="Catalog",
        outcome="navigation",
    )
    assert sentence == (
        "From Home, the crawler used 'Browse catalog' and reached Catalog "
        "(opened a new page)."
    )


def test_build_human_execution_rows_adds_display_payload() -> None:
    rows = _build_human_execution_rows(
        execution_rows=[
            {
                "index": 1,
                "source_page_display": "Home",
                "target_page_display": "Catalog",
                "action_display": "Open catalog",
                "outcome_display": "Opened a new page",
                "timeline_sentence": "From Home ...",
            }
        ]
    )
    assert rows[0]["display"] == {
        "source_page": "Home",
        "target_page": "Catalog",
        "action": "Open catalog",
        "outcome": "Opened a new page",
        "sentence": "From Home ...",
    }


def test_build_mbt_coverage_data_builds_matrix_and_uncovered_edges() -> None:
    """MBT coverage helper should expose matrix rows and uncovered edges."""
    state_home = PageState(
        state_id="state-home",
        url="https://example.com/",
        title="Home",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
    )
    state_catalog = PageState(
        state_id="state-catalog",
        url="https://example.com/catalog",
        title="Catalog",
        fingerprint="e" * 64,
        depth=1,
        dom_structure_hash="dom2",
        visible_text_hash="text2",
        form_state_hash="form2",
    )
    state_detail = PageState(
        state_id="state-detail",
        url="https://example.com/detail",
        title="Detail",
        fingerprint="d" * 64,
        depth=2,
        dom_structure_hash="dom3",
        visible_text_hash="text3",
        form_state_hash="form3",
    )
    action_open_catalog = Action(
        action_id="action-open-catalog",
        action_type=ActionType.CLICK,
        target_selector="a[href='/catalog']",
        label="Open catalog",
    )
    action_open_detail = Action(
        action_id="action-open-detail",
        action_type=ActionType.CLICK,
        target_selector="a[href='/detail']",
        label="Open detail",
    )
    result = ExplorationResult(
        states={
            "state-home": state_home,
            "state-catalog": state_catalog,
            "state-detail": state_detail,
        },
        actions={
            "action-open-catalog": action_open_catalog,
            "action-open-detail": action_open_detail,
        },
        results=[
            ActionResult(
                action_id="action-open-catalog",
                source_state_id="state-home",
                target_state_id="state-catalog",
                outcome=OutcomeType.NAVIGATION,
            ),
            ActionResult(
                action_id="action-open-detail",
                source_state_id="state-catalog",
                target_state_id="state-detail",
                outcome=OutcomeType.NAVIGATION,
            ),
        ],
    )

    data = _build_mbt_coverage_data(result=result)

    assert data["state"]["total"] == 3
    assert data["edge"]["total"] == 2
    assert data["edge"]["pct"] == 0.0
    assert len(data["matrix_rows"]) == 2
    assert data["edge"]["uncovered"][0]["action_type"] == "click"
    assert data["edge"]["uncovered"][0]["from_name"] != ""
    assert data["edge"]["uncovered"][0]["to_name"] != ""
    assert "guards" in data["edge"]["uncovered"][0]
    assert "inferred_from" in data["edge"]["uncovered"][0]


def test_build_page_object_cards_includes_code_preview_and_locator_rows() -> None:
    state_home = PageState(
        state_id="state-home",
        url="https://example.com/",
        title="Home",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
    )
    action_open = Action(
        action_id="action-open",
        action_type=ActionType.CLICK,
        target_selector="#open-card",
        label="Open card",
    )
    result = ExplorationResult(
        config={"start_url": "https://example.com"},
        states={"state-home": state_home},
        actions={"action-open": action_open},
        smart_analyses={
            "state-home": {
                "archetype": "listing",
                "archetype_confidence": 0.9,
                "structural_signature": "sig-home",
                "zones": [],
                "repeated_structures": [],
                "content_density": {
                    "total_text_length": 0,
                    "heading_count": 0,
                    "image_count": 0,
                    "link_count": 0,
                    "form_input_count": 0,
                    "interactive_count": 0,
                    "text_to_interactive_ratio": 0.0,
                },
                "extracted_entities": [],
                "has_search": False,
                "has_pagination": False,
                "has_filters": False,
                "heading_hierarchy": [],
                "catalog": {
                    "archetype": "listing",
                    "url_pattern": "/",
                    "entries": [
                        {
                            "selector": "#open-card",
                            "tag": "button",
                            "label": "Open",
                            "zone_type": "main_content",
                            "element_type": "button",
                        }
                    ],
                },
            }
        },
    )

    site_model = _build_site_model(result=result)
    assert site_model is not None

    cards = _build_page_object_cards(result=result, site_model=site_model)

    assert len(cards) == 1
    assert cards[0]["class_name"].endswith("Page")
    assert cards[0]["locator_rows"][0]["selector"] == "#open-card"
    assert cards[0]["locator_rows"][0]["exercised"] is True
    assert "class " in cards[0]["code_preview"]["python"]
    assert "export class " in cards[0]["code_preview"]["typescript"]


def test_build_graph_data_uses_site_model_page_types_and_edges() -> None:
    state_listing = PageState(
        state_id="state-listing",
        url="https://example.com/movies",
        title="Listing",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
    )
    state_detail = PageState(
        state_id="state-detail",
        url="https://example.com/movies/1",
        title="Detail",
        fingerprint="e" * 64,
        depth=1,
        dom_structure_hash="dom2",
        visible_text_hash="text2",
        form_state_hash="form2",
    )
    action_open = Action(
        action_id="action-open",
        action_type=ActionType.CLICK,
        target_selector="a[href='/movies/1']",
        label="Open detail",
    )
    result = ExplorationResult(
        config={"start_url": "https://example.com"},
        states={
            "state-listing": state_listing,
            "state-detail": state_detail,
        },
        actions={"action-open": action_open},
        results=[
            ActionResult(
                action_id="action-open",
                source_state_id="state-listing",
                target_state_id="state-detail",
                outcome=OutcomeType.NAVIGATION,
            )
        ],
        flows=[
            Flow(
                flow_id="flow-1",
                name="Listing to detail",
                description="Open detail",
                state_ids=["state-listing", "state-detail"],
                action_ids=["action-open"],
                outcomes=[OutcomeType.NAVIGATION],
            )
        ],
        smart_analyses={
            "state-listing": {"structural_signature": "listing_sig"},
            "state-detail": {"structural_signature": "detail_sig"},
        },
    )
    site_model = _build_site_model(result=result)
    assert site_model is not None

    page_object_cards = _build_page_object_cards(result=result, site_model=site_model)
    mbt_coverage = _build_mbt_coverage_data(result=result, site_model=site_model)
    graph = _build_graph_data(
        result=result,
        site_model=site_model,
        mbt_coverage=mbt_coverage,
        page_object_cards=page_object_cards,
    )

    assert len(graph["nodes"]) == 2
    assert graph["nodes"][0]["id"] != ""
    assert graph["nodes"][0]["anchor_id"] != ""
    assert len(graph["edges"]) == 1
    assert graph["edges"][0]["action_label"] == "Open detail"
    assert graph["edges"][0]["occurrence_count"] == 1
    assert "uncovered" in graph["edges"][0]


def test_build_flow_template_cards_include_instances_and_status_counts() -> None:
    state_listing = PageState(
        state_id="state-listing",
        url="https://example.com/movies",
        title="Listing",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
    )
    state_detail_1 = PageState(
        state_id="state-detail-1",
        url="https://example.com/movies/1",
        title="Detail 1",
        fingerprint="e" * 64,
        depth=1,
        dom_structure_hash="dom2",
        visible_text_hash="text2",
        form_state_hash="form2",
    )
    state_detail_2 = PageState(
        state_id="state-detail-2",
        url="https://example.com/movies/2",
        title="Detail 2",
        fingerprint="d" * 64,
        depth=1,
        dom_structure_hash="dom3",
        visible_text_hash="text3",
        form_state_hash="form3",
    )
    action_open_1 = Action(
        action_id="action-open-1",
        action_type=ActionType.CLICK,
        target_selector="a[href='/movies/1']",
        label="Open movie 1",
    )
    action_open_2 = Action(
        action_id="action-open-2",
        action_type=ActionType.CLICK,
        target_selector="a[href='/movies/2']",
        label="Open movie 2",
    )
    result = ExplorationResult(
        states={
            "state-listing": state_listing,
            "state-detail-1": state_detail_1,
            "state-detail-2": state_detail_2,
        },
        actions={
            "action-open-1": action_open_1,
            "action-open-2": action_open_2,
        },
        results=[
            ActionResult(
                action_id="action-open-1",
                source_state_id="state-listing",
                target_state_id="state-detail-1",
                outcome=OutcomeType.NAVIGATION,
                stability_score=0.95,
            ),
            ActionResult(
                action_id="action-open-2",
                source_state_id="state-listing",
                target_state_id="state-detail-2",
                outcome=OutcomeType.NAVIGATION,
                stability_score=0.35,
            ),
        ],
        flows=[
            Flow(
                flow_id="flow-1",
                name="Movie 1 detail",
                description="Open movie 1",
                state_ids=["state-listing", "state-detail-1"],
                action_ids=["action-open-1"],
                outcomes=[OutcomeType.NAVIGATION],
                stability_score=0.95,
                tags=["smoke"],
            ),
            Flow(
                flow_id="flow-2",
                name="Movie 2 detail",
                description="Open movie 2",
                state_ids=["state-listing", "state-detail-2"],
                action_ids=["action-open-2"],
                outcomes=[OutcomeType.EXCEPTION],
                stability_score=0.4,
                tags=["regression"],
            ),
        ],
        smart_analyses={
            "state-listing": {"structural_signature": "listing_sig"},
            "state-detail-1": {"structural_signature": "detail_sig"},
            "state-detail-2": {"structural_signature": "detail_sig"},
        },
    )
    site_model = _build_site_model(result=result)
    assert site_model is not None
    assert site_model.flow_templates

    execution_rows = _build_execution_rows(
        result=result,
        action_labels={
            "action-open-1": "Open movie 1",
            "action-open-2": "Open movie 2",
        },
        action_selectors={
            "action-open-1": "a[href='/movies/1']",
            "action-open-2": "a[href='/movies/2']",
        },
        action_metadata={
            "action-open-1": {},
            "action-open-2": {},
        },
        screenshot_links=[None, None],
    )
    flow_execution_map, _, _ = _build_flow_execution_map(
        result=result,
        execution_rows=execution_rows,
    )
    cards = _build_flow_template_cards(
        flow_templates=site_model.flow_templates,
        result=result,
        flow_execution_map=flow_execution_map,
        flow_status_map={"flow-1": "pass", "flow-2": "fail"},
    )

    assert len(cards) == 1
    assert cards[0]["occurrence_count"] == 2
    assert cards[0]["template_type"] == "click"
    assert cards[0]["stable_count"] == 1
    assert cards[0]["fail_count"] == 1
    assert cards[0]["warn_count"] == 0
    assert cards[0]["representative_rows"]
    assert len(cards[0]["instances"]) == 2


def test_build_flow_instance_cards_flattens_and_sorts_instances() -> None:
    cards = _build_flow_instance_cards(
        flow_template_cards=[
            {
                "template_id": "template-alpha",
                "name": "Browse Listing \u2192 Detail",
                "instances": [
                    {
                        "flow_id": "flow-pass",
                        "name": "Detail page pass path",
                        "status": "pass",
                        "stability_score": 0.9,
                        "depth": 2,
                        "tags": ["smoke"],
                    },
                    {
                        "flow_id": "flow-fail",
                        "name": "Detail page fail path",
                        "status": "fail",
                        "stability_score": 0.2,
                        "depth": 3,
                        "tags": ["regression"],
                    },
                ],
            }
        ]
    )

    assert len(cards) == 2
    assert cards[0]["status"] == "fail"
    assert cards[0]["flow_id"] == "flow-fail"
    assert cards[0]["stability_pct"] == 20
    assert (
        cards[0]["summary"] == "Detail page fail path takes 3 steps with 20% stability."
    )
    assert cards[1]["status"] == "pass"
    assert cards[1]["template_name"] == "Browse Listing \u2192 Detail"


def test_build_quality_insights_provides_actionable_links() -> None:
    state_listing = PageState(
        state_id="state-listing",
        url="https://example.com/movies",
        title="Listing",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
    )
    state_detail_1 = PageState(
        state_id="state-detail-1",
        url="https://example.com/movies/1",
        title="Detail 1",
        fingerprint="e" * 64,
        depth=1,
        dom_structure_hash="dom2",
        visible_text_hash="text2",
        form_state_hash="form2",
    )
    state_detail_2 = PageState(
        state_id="state-detail-2",
        url="https://example.com/movies/2",
        title="Detail 2",
        fingerprint="d" * 64,
        depth=1,
        dom_structure_hash="dom3",
        visible_text_hash="text3",
        form_state_hash="form3",
    )
    action_open = Action(
        action_id="action-open",
        action_type=ActionType.CLICK,
        target_selector="a[href='/movies/1']",
        label="Open detail",
    )
    result = ExplorationResult(
        states={
            "state-listing": state_listing,
            "state-detail-1": state_detail_1,
            "state-detail-2": state_detail_2,
        },
        actions={"action-open": action_open},
        results=[
            ActionResult(
                action_id="action-open",
                source_state_id="state-listing",
                target_state_id="state-detail-1",
                outcome=OutcomeType.NAVIGATION,
                stability_score=0.9,
            ),
            ActionResult(
                action_id="action-open",
                source_state_id="state-listing",
                target_state_id="state-detail-2",
                outcome=OutcomeType.EXCEPTION,
                stability_score=0.25,
                observation_notes="button not clickable",
            ),
        ],
        flows=[
            Flow(
                flow_id="flow-1",
                name="Detail 1 flow",
                description="Open detail 1",
                state_ids=["state-listing", "state-detail-1"],
                action_ids=["action-open"],
                outcomes=[OutcomeType.NAVIGATION],
                stability_score=0.9,
            ),
            Flow(
                flow_id="flow-2",
                name="Detail 2 flow",
                description="Open detail 2",
                state_ids=["state-listing", "state-detail-2"],
                action_ids=["action-open"],
                outcomes=[OutcomeType.EXCEPTION],
                stability_score=0.25,
            ),
        ],
        smart_analyses={
            "state-listing": {"structural_signature": "listing_sig"},
            "state-detail-1": {"structural_signature": "detail_sig"},
            "state-detail-2": {"structural_signature": "detail_sig"},
        },
    )
    site_model = _build_site_model(result=result)
    assert site_model is not None

    page_object_cards = _build_page_object_cards(result=result, site_model=site_model)
    execution_rows = _build_execution_rows(
        result=result,
        action_labels={"action-open": "Open detail"},
        action_selectors={"action-open": "a[href='/movies/1']"},
        action_metadata={"action-open": {}},
        screenshot_links=[None, None],
    )
    _, _, execution_step_map = _build_flow_execution_map(
        result=result,
        execution_rows=execution_rows,
    )
    diagnostics = _build_diagnostics(
        result=result,
        action_labels={"action-open": "Open detail"},
        action_selectors={"action-open": "a[href='/movies/1']"},
        screenshot_links=[None, None],
    )
    insights = _build_quality_insights(
        result=result,
        page_object_cards=page_object_cards,
        diagnostics=diagnostics,
        execution_step_map=execution_step_map,
        flow_templates=site_model.flow_templates,
    )

    assert insights["locator_health_rows"]
    assert insights["flaky_action_count"] == 1
    assert insights["low_stability_count"] == 1
    assert insights["recommendations"]
    assert any(
        item["link_kind"] == "page_object" for item in insights["recommendations"]
    )
    assert any(item["link_kind"] == "flow" for item in insights["recommendations"])
    assert any(item["link_kind"] == "step" for item in insights["recommendations"])


def test_build_site_structure_summary_counts_page_types_edges_and_templates() -> None:
    state_home = PageState(
        state_id="state-home",
        url="https://example.com/",
        title="Home",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
    )
    state_catalog = PageState(
        state_id="state-catalog",
        url="https://example.com/catalog",
        title="Catalog",
        fingerprint="e" * 64,
        depth=1,
        dom_structure_hash="dom2",
        visible_text_hash="text2",
        form_state_hash="form2",
    )
    action_open = Action(
        action_id="action-open",
        action_type=ActionType.CLICK,
        target_selector="a[href='/catalog']",
        label="Open catalog",
    )
    result = ExplorationResult(
        states={
            "state-home": state_home,
            "state-catalog": state_catalog,
        },
        actions={"action-open": action_open},
        results=[
            ActionResult(
                action_id="action-open",
                source_state_id="state-home",
                target_state_id="state-catalog",
                outcome=OutcomeType.NAVIGATION,
            )
        ],
        flows=[
            Flow(
                flow_id="flow-1",
                name="Home to catalog",
                description="Open catalog",
                state_ids=["state-home", "state-catalog"],
                action_ids=["action-open"],
            )
        ],
        smart_analyses={
            "state-home": {"structural_signature": "home_sig"},
            "state-catalog": {"structural_signature": "catalog_sig"},
        },
    )
    site_model = _build_site_model(result=result)
    assert site_model is not None

    summary = _build_site_structure_summary(
        site_model=site_model,
        flow_templates=site_model.flow_templates,
    )

    assert summary["page_type_count"] == 2
    assert summary["navigation_path_count"] == 1
    assert summary["flow_template_count"] == 1


def test_build_cross_run_comparison_reports_page_and_locator_diffs(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "history.db"
    db = FlowscoutDB(str(db_path))
    baseline_result = ExplorationResult(
        config={"start_url": "https://example.com"},
        started_at="2025-01-01T00:00:00Z",
        finished_at="2025-01-01T00:01:00Z",
        states={
            "state-home": PageState(
                state_id="state-home",
                url="https://example.com/",
                title="Home",
                fingerprint="fp-home",
                depth=0,
                dom_structure_hash="dom-home",
                visible_text_hash="text-home",
                form_state_hash="form-home",
            )
        },
        smart_analyses={
            "state-home": {
                "archetype": "listing",
                "structural_signature": "sig-home",
                "content_density": {},
                "catalog": {
                    "archetype": "listing",
                    "url_pattern": "/",
                    "entries": [
                        {
                            "selector": "a.old-card",
                            "tag": "a",
                            "label": "Old card",
                            "zone_type": "main_content",
                            "element_type": "link",
                        }
                    ],
                },
            }
        },
    )
    db.save_run(baseline_result)
    db.close()

    current_result = ExplorationResult(
        config={
            "start_url": "https://example.com",
            "db_path": str(db_path),
        },
        started_at="2025-01-02T00:00:00Z",
        finished_at="2025-01-02T00:01:00Z",
        states={
            "state-home": PageState(
                state_id="state-home",
                url="https://example.com/",
                title="Home",
                fingerprint="fp-home",
                depth=0,
                dom_structure_hash="dom-home",
                visible_text_hash="text-home",
                form_state_hash="form-home",
            ),
            "state-new": PageState(
                state_id="state-new",
                url="https://example.com/new",
                title="New",
                fingerprint="fp-new",
                depth=1,
                dom_structure_hash="dom-new",
                visible_text_hash="text-new",
                form_state_hash="form-new",
            ),
        },
        smart_analyses={
            "state-home": {
                "archetype": "listing",
                "structural_signature": "sig-home",
                "content_density": {},
                "catalog": {
                    "archetype": "listing",
                    "url_pattern": "/",
                    "entries": [
                        {
                            "selector": "a.new-card",
                            "tag": "a",
                            "label": "New card",
                            "zone_type": "main_content",
                            "element_type": "link",
                        }
                    ],
                },
            },
            "state-new": {
                "archetype": "listing",
                "structural_signature": "sig-home",
                "content_density": {},
                "catalog": {
                    "archetype": "listing",
                    "url_pattern": "/new",
                    "entries": [],
                },
            },
        },
    )
    site_model = _build_site_model(result=current_result)
    assert site_model is not None

    comparison = _build_cross_run_comparison(
        result=current_result,
        site_model=site_model,
    )

    assert comparison["has_previous_run"] is True
    assert comparison["new_pages"] == 1
    assert comparison["disappeared_pages"] == 0
    assert comparison["changed_locators"] == 2
    assert comparison["changed_page_type_ids"]


def test_build_page_object_cards_marks_changed_page_types() -> None:
    result = ExplorationResult(
        states={
            "state-home": PageState(
                state_id="state-home",
                url="https://example.com/",
                title="Home",
                fingerprint="fp-home",
                depth=0,
                dom_structure_hash="dom-home",
                visible_text_hash="text-home",
                form_state_hash="form-home",
            )
        },
        smart_analyses={
            "state-home": {
                "archetype": "listing",
                "structural_signature": "sig-home",
                "content_density": {},
                "catalog": {
                    "archetype": "listing",
                    "url_pattern": "/",
                    "entries": [
                        {
                            "selector": "a.card",
                            "tag": "a",
                            "label": "Card",
                            "zone_type": "main_content",
                            "element_type": "link",
                        }
                    ],
                },
            }
        },
    )
    site_model = _build_site_model(result=result)
    assert site_model is not None
    changed_id = site_model.page_types[0].page_type_id

    cards = _build_page_object_cards(
        result=result,
        site_model=site_model,
        changed_page_type_ids={changed_id},
    )

    assert cards
    assert cards[0]["is_changed"] is True


def test_build_dashboard_top_issues_limits_and_sorts_by_priority() -> None:
    top_issues = _build_dashboard_top_issues(
        quality_insights={
            "recommendations": [
                {
                    "priority": "medium",
                    "title": "Medium issue",
                    "detail": "m",
                    "link_kind": "step",
                    "link_value": "10",
                },
                {
                    "priority": "high",
                    "title": "High issue A",
                    "detail": "a",
                    "link_kind": "flow",
                    "link_value": "flow-a",
                },
                {
                    "priority": "low",
                    "title": "Low issue",
                    "detail": "l",
                    "link_kind": "page_object",
                    "link_value": "home",
                },
                {
                    "priority": "high",
                    "title": "High issue B",
                    "detail": "b",
                    "link_kind": "flow",
                    "link_value": "flow-b",
                },
                {
                    "priority": "medium",
                    "title": "Medium issue 2",
                    "detail": "m2",
                    "link_kind": "step",
                    "link_value": "11",
                },
                {
                    "priority": "low",
                    "title": "Low issue 2",
                    "detail": "l2",
                    "link_kind": "page_object",
                    "link_value": "catalog",
                },
            ]
        },
    )

    assert len(top_issues) == 5
    assert top_issues[0]["priority"] == "high"
    assert top_issues[1]["priority"] == "high"
    assert top_issues[2]["priority"] == "medium"


def _generate_zero_data_report(
    tmp_path: Path,
    *,
    blocked: bool = False,
) -> str:
    """Generate a report with 0 actions, 0 flows. Return HTML content."""
    output = tmp_path / "report.html"
    states: dict[str, PageState] = {
        "state-home": PageState(
            state_id="state-home",
            url="https://example.com/",
            title="Home",
            fingerprint="f" * 64,
            depth=0,
            dom_structure_hash="dom1",
            visible_text_hash="text1",
            form_state_hash="form1",
        ),
    }
    if blocked:
        states["state-blocked"] = PageState(
            state_id="state-blocked",
            url="https://example.com/admin",
            title="Admin",
            fingerprint="e" * 64,
            depth=0,
            dom_structure_hash="dom2",
            visible_text_hash="text2",
            form_state_hash="form2",
            block_reason=PageBlockReason.ACCESS_DENIED,
            block_detail="HTTP 403 Forbidden",
        )
    result = ExplorationResult(
        config={"start_url": "https://example.com", "strategy": "priority"},
        states=states,
    )
    HTMLReporter().generate(result, str(output))
    return output.read_text()


def test_default_landing_tab_is_dashboard(tmp_path: Path) -> None:
    html = _generate_zero_data_report(tmp_path)
    assert 'data-page="dashboard" onclick="setReportPage(\'dashboard\'' in html
    assert 'class="page-btn active" data-page="dashboard"' in html, (
        "Dashboard button should be active by default"
    )
    assert 'class="page-btn active" data-page="site-map"' not in html, (
        "Site Map button should not be active by default"
    )
    assert "setReportPage('dashboard')" in html


def test_page_hidden_css_is_global_not_scoped(tmp_path: Path) -> None:
    html = _generate_zero_data_report(tmp_path)
    assert ".page-hidden" in html
    assert "[data-report-page].page-hidden" not in html


def test_zero_data_report_shows_no_steps_message(tmp_path: Path) -> None:
    html = _generate_zero_data_report(tmp_path)
    assert "No interactive steps were captured" in html


def test_zero_data_blocked_report_explains_blocked(tmp_path: Path) -> None:
    html = _generate_zero_data_report(tmp_path, blocked=True)
    assert "blocked" in html.lower()
    assert "No interactive steps were captured" in html


def test_zero_data_report_hides_test_filters(tmp_path: Path) -> None:
    html = _generate_zero_data_report(tmp_path)
    assert "No test cases were generated" in html
    assert 'id="template-type-filter"' not in html
    assert 'id="template-stability-filter"' not in html
    assert 'id="template-tag-filter"' not in html


def test_zero_data_report_timeline_shows_empty_state(tmp_path: Path) -> None:
    html = _generate_zero_data_report(tmp_path)
    assert "No crawl steps" in html
    assert 'id="timeline-visibility-filter"' not in html


def test_zero_data_blocked_report_timeline_mentions_blocked(
    tmp_path: Path,
) -> None:
    html = _generate_zero_data_report(tmp_path, blocked=True)
    assert "blocked" in html.lower()
    assert "No crawl steps to display" in html


def _visible_text_without_scripts(html: str) -> str:
    """Return only visible text content from HTML source."""
    without_scripts = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S)
    without_styles = re.sub(
        r"<style[^>]*>.*?</style>", " ", without_scripts, flags=re.S
    )
    without_tags = re.sub(r"<[^>]+>", " ", without_styles)
    return " ".join(without_tags.split())


def test_report_hides_machine_ids_from_visible_text(tmp_path: Path) -> None:
    output = tmp_path / "report.html"
    result = ExplorationResult(
        config={"start_url": "https://example.com", "strategy": "priority"},
        states={
            "state-alpha-1234": PageState(
                state_id="state-alpha-1234",
                url="https://example.com",
                title="Home",
                fingerprint="f" * 64,
                depth=0,
                dom_structure_hash="dom-a",
                visible_text_hash="text-a",
                form_state_hash="form-a",
            ),
            "state-beta-9876": PageState(
                state_id="state-beta-9876",
                url="https://example.com/details",
                title="Details",
                fingerprint="e" * 64,
                depth=1,
                dom_structure_hash="dom-b",
                visible_text_hash="text-b",
                form_state_hash="form-b",
            ),
        },
        actions={
            "action-machine-888": Action(
                action_id="action-machine-888",
                action_type=ActionType.CLICK,
                target_selector="#toggle-track-desktop",
                label="Open details",
                metadata={"dom_id": "toggle-track-desktop"},
            )
        },
        results=[
            ActionResult(
                action_id="action-machine-888",
                source_state_id="state-alpha-1234",
                target_state_id="state-beta-9876",
                outcome=OutcomeType.NAVIGATION,
                url_before="https://example.com",
                url_after="https://example.com/details",
            )
        ],
    )

    HTMLReporter().generate(result, str(output))
    visible_text = _visible_text_without_scripts(output.read_text())

    assert "state-alpha-1234" not in visible_text
    assert "state-beta-9876" not in visible_text
    assert "action-machine-888" not in visible_text
    assert "toggle-track-desktop" not in visible_text


def test_report_includes_timeline_filters_and_debug_trace_panel(
    tmp_path: Path,
) -> None:
    output = tmp_path / "report.html"
    result = ExplorationResult(
        config={"start_url": "https://example.com", "strategy": "priority"},
        states={
            "state-home": PageState(
                state_id="state-home",
                url="https://example.com",
                title="Home",
                fingerprint="f" * 64,
                depth=0,
                dom_structure_hash="dom-home",
                visible_text_hash="text-home",
                form_state_hash="form-home",
            )
        },
        actions={
            "action-refresh": Action(
                action_id="action-refresh",
                action_type=ActionType.CLICK,
                target_selector="button.refresh",
                label="Refresh page",
            )
        },
        results=[
            ActionResult(
                action_id="action-refresh",
                source_state_id="state-home",
                target_state_id="state-home",
                outcome=OutcomeType.NO_CHANGE,
                url_before="https://example.com",
                url_after="https://example.com",
            )
        ],
    )

    HTMLReporter().generate(result, str(output))
    html = output.read_text()

    assert 'id="timeline-visibility-filter"' in html
    assert "Effective steps only" in html
    assert 'id="timeline-outcome-filter"' in html
    assert 'id="timeline-action-filter"' in html
    assert 'id="timeline-page-filter"' in html
    assert 'data-effective="false"' in html
    assert "function filterExecutionTimeline()" in html
    assert 'id="debug-trace-panel"' in html
    assert "Debug Trace (raw technical details)" in html

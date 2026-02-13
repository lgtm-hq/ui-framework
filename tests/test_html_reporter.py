"""Tests for HTML report helper utilities."""

import os
from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.reporting.html import (
    _build_page_object_cards,
    _build_site_model,
    _build_execution_rows,
    _build_flow_execution_map,
    _build_locator_quality_data,
    _build_mbt_coverage_data,
    _to_report_asset_href,
)


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

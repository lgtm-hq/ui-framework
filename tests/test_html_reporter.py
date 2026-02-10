"""Tests for HTML report helper utilities."""

import os
from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.reporting.html import (
    _build_execution_rows,
    _build_flow_execution_map,
    _to_report_asset_href,
)


def test_to_report_asset_href_none() -> None:
    report_dir = Path("/tmp/reports/run")
    assert _to_report_asset_href(None, report_dir=report_dir) is None


def test_to_report_asset_href_relative_path() -> None:
    report_dir = Path("/tmp/reports/run")
    href = _to_report_asset_href("evidence/actions/a.png", report_dir=report_dir)
    assert href == "evidence/actions/a.png"


def test_to_report_asset_href_inside_report_dir() -> None:
    report_dir = Path("/tmp/reports/run")
    path = report_dir / "evidence" / "actions" / "shot.png"
    href = _to_report_asset_href(str(path), report_dir=report_dir)
    assert href == "evidence/actions/shot.png"


def test_to_report_asset_href_outside_report_dir() -> None:
    report_dir = Path("/tmp/reports/run")
    path = Path("/tmp/other/location/shot.png")
    href = _to_report_asset_href(str(path), report_dir=report_dir)
    assert href == path.as_uri()


def test_to_report_asset_href_cwd_relative_run_path(tmp_path: Path) -> None:
    run_dir = tmp_path / "reports" / "site" / "baseline" / "runs" / "2026-02-09_00.00.00"
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
        confidence=0.95,
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

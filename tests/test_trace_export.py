"""Tests for crawl trace sidecar export."""

from __future__ import annotations

import json
from pathlib import Path

import flowscout.cli.explore as explore_cli
from flowscout.analysis.graph import ExplorationResult
from flowscout.core.action_types import ActionType
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, OutcomeType
from flowscout.reporting.trace_export import build_crawl_trace, write_crawl_trace


def _sample_result() -> ExplorationResult:
    """Build a minimal exploration result for trace export tests."""
    home_state = PageState(
        state_id="state-home",
        url="https://example.com",
        title="Home",
        fingerprint="fp-home",
        depth=0,
        dom_structure_hash="dom-home",
        visible_text_hash="text-home",
        form_state_hash="form-home",
    )
    detail_state = PageState(
        state_id="state-detail",
        url="https://example.com/detail/42",
        title="Detail",
        fingerprint="fp-detail",
        depth=1,
        dom_structure_hash="dom-detail",
        visible_text_hash="text-detail",
        form_state_hash="form-detail",
    )
    action = Action(
        action_id="action-open-detail",
        action_type=ActionType.CLICK,
        target_selector="a.movie-card",
        label="Open detail page",
        metadata={"dom_id": "movie-card-42"},
    )
    action_result = ActionResult(
        action_id="action-open-detail",
        source_state_id="state-home",
        target_state_id="state-detail",
        outcome=OutcomeType.NAVIGATION,
        url_before=home_state.url,
        url_after=detail_state.url,
        transition_kind="hard_navigation",
        transition_detail="Top-level document navigation completed.",
    )
    return ExplorationResult(
        config={
            "start_url": "https://example.com",
            "environment": "dev",
            "behavior_modes": {
                "outcome_mode": "legacy",
                "link_scope_mode": "legacy",
            },
        },
        states={
            home_state.state_id: home_state,
            detail_state.state_id: detail_state,
        },
        actions={action.action_id: action},
        results=[action_result],
    )


def test_build_crawl_trace_contains_expected_schema_keys() -> None:
    """Trace payload should expose stable top-level schema keys."""
    payload = build_crawl_trace(result=_sample_result())
    assert payload["schema_version"] == "1.0.0"
    assert "summary" in payload
    assert "states" in payload
    assert "actions" in payload
    assert "steps" in payload
    assert payload["steps"][0]["result"]["transition_kind"] == "hard_navigation"


def test_write_crawl_trace_writes_json_file(tmp_path: Path) -> None:
    """Sidecar writer should create crawl_trace.json."""
    path = write_crawl_trace(
        result=_sample_result(),
        output_path=tmp_path / "crawl_trace.json",
    )
    payload = json.loads(path.read_text())
    assert payload["summary"]["total_steps"] == 1
    assert payload["steps"][0]["action"]["label"] == "Open detail page"


def test_cli_run_artifacts_include_trace_sidecar(tmp_path: Path) -> None:
    """CLI artifact helper should write both result.json and crawl_trace.json."""
    json_path, trace_path = explore_cli._write_run_artifacts(
        result=_sample_result(),
        run_dir=tmp_path,
    )
    assert Path(json_path).exists()
    assert Path(trace_path).exists()

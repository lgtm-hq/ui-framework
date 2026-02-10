"""Tests for HTML report diagnostics helpers."""

from flowscout.analysis.graph import ExplorationResult
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.reporting.html import (
    _build_diagnostics,
    _build_element_drilldown_map,
    _build_execution_rows,
)


def _make_action(*, action_id: str, label: str) -> Action:
    return Action(
        action_id=action_id,
        action_type=ActionType.CLICK,
        target_selector=f"#{action_id}",
        label=label,
    )


def test_build_diagnostics_summarizes_low_confidence_and_flaky_steps() -> None:
    result = ExplorationResult(
        actions={
            "a1": _make_action(action_id="a1", label="Open card"),
            "a2": _make_action(action_id="a2", label="Open menu"),
        },
        results=[
            ActionResult(
                action_id="a1",
                source_state_id="state-alpha",
                target_state_id="state-beta",
                outcome=OutcomeType.NAVIGATION,
                confidence=0.55,
                confidence_reason="weak_dom_signal",
            ),
            ActionResult(
                action_id="a1",
                source_state_id="state-alpha",
                target_state_id="state-gamma",
                outcome=OutcomeType.NO_CHANGE,
                confidence=0.45,
                confidence_reason="weak_dom_signal",
            ),
            ActionResult(
                action_id="a2",
                source_state_id="state-beta",
                target_state_id="state-delta",
                outcome=OutcomeType.DOM_CHANGE,
                confidence=0.92,
                confidence_reason="stable_transition",
            ),
        ],
    )

    diagnostics = _build_diagnostics(
        result=result,
        action_labels={
            "a1": "Open card",
            "a2": "Open menu",
        },
        action_selectors={
            "a1": "#card",
            "a2": "#menu",
        },
        screenshot_links=[
            "evidence/actions/1.png",
            None,
            None,
        ],
        low_confidence_threshold=0.6,
    )

    assert diagnostics["low_confidence_count"] == 2
    assert diagnostics["low_confidence_pct"] == 67
    assert diagnostics["flaky_paths_count"] == 1
    assert diagnostics["reason_breakdown"][0] == {
        "reason": "weak_dom_signal",
        "count": 2,
    }
    assert diagnostics["flaky_items"][0]["outcomes"] == [
        "navigation",
        "no_change",
    ]
    assert diagnostics["low_confidence_items"][0]["confidence_pct"] == 45


def test_build_diagnostics_uses_unspecified_reason_when_missing() -> None:
    result = ExplorationResult(
        actions={"a1": _make_action(action_id="a1", label="Submit")},
        results=[
            ActionResult(
                action_id="a1",
                source_state_id="state-alpha",
                target_state_id="state-beta",
                outcome=OutcomeType.NO_CHANGE,
                confidence=0.4,
                confidence_reason="",
            )
        ],
    )

    diagnostics = _build_diagnostics(
        result=result,
        action_labels={"a1": "Submit"},
        action_selectors={"a1": "form button[type='submit']"},
        screenshot_links=[None],
        low_confidence_threshold=0.6,
    )

    assert diagnostics["low_confidence_count"] == 1
    assert diagnostics["reason_breakdown"] == [
        {"reason": "unspecified", "count": 1}
    ]


def test_build_execution_rows_includes_dom_id_from_action_metadata() -> None:
    result = ExplorationResult(
        actions={"a1": _make_action(action_id="a1", label="Toggle theme")},
        results=[
            ActionResult(
                action_id="a1",
                source_state_id="state-alpha",
                target_state_id="state-beta",
                outcome=OutcomeType.NO_CHANGE,
            )
        ],
    )

    rows = _build_execution_rows(
        result=result,
        action_labels={"a1": "Toggle theme"},
        action_selectors={"a1": "#toggle-track-desktop"},
        action_metadata={"a1": {"dom_id": "toggle-track-desktop"}},
        screenshot_links=[None],
    )

    assert len(rows) == 1
    assert rows[0]["dom_id"] == "toggle-track-desktop"


def test_element_drilldown_marks_hidden_entries() -> None:
    state = PageState(
        state_id="state-alpha",
        url="https://example.com",
        title="Example",
        fingerprint="a" * 64,
        depth=0,
        dom_structure_hash="dom",
        visible_text_hash="text",
        form_state_hash="form",
    )
    result = ExplorationResult(
        states={"state-alpha": state},
        smart_analyses={
            "state-alpha": {
                "catalog": {
                    "entries": [
                        {
                            "selector": "#visible-item",
                            "dom_id": "visible-item",
                            "tag": "button",
                            "label": "Visible CTA",
                            "zone_type": "main_content",
                            "element_type": "button",
                            "is_visible": True,
                        },
                        {
                            "selector": "#hidden-item",
                            "dom_id": "hidden-item",
                            "tag": "input",
                            "label": "Hidden Toggle",
                            "zone_type": "header",
                            "element_type": "input_checkbox",
                            "is_visible": False,
                        },
                    ]
                }
            }
        },
    )

    drilldown = _build_element_drilldown_map(result=result, element_inventory=None)
    info = drilldown["state-alpha"]

    assert info["visible"] == 1
    assert info["hidden"] == 1
    assert any(entry["is_visible"] is False for entry in info["entries"])

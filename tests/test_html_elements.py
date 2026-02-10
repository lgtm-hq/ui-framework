"""Tests for HTML report element drilldown helpers."""

from flowscout.analysis.graph import ExplorationResult
from flowscout.core.state import PageState
from flowscout.reporting.html import _build_element_drilldown_map


def _make_state(*, state_id: str, title: str, url: str, depth: int = 0) -> PageState:
    return PageState(
        state_id=state_id,
        url=url,
        title=title,
        fingerprint=f"fp-{state_id}",
        depth=depth,
        dom_structure_hash="dom",
        visible_text_hash="text",
        form_state_hash="form",
    )


def test_build_element_drilldown_map_includes_locator_rows() -> None:
    result = ExplorationResult(
        states={
            "state-a": _make_state(
                state_id="state-a",
                title="Popular Movies",
                url="https://example.com/popular",
            )
        },
        smart_analyses={
            "state-a": {
                "catalog": {
                    "entries": [
                        {
                            "selector": "a[href='/movie/1']",
                            "label": "Movie card .react-stars-123:before { position: absolute; }",
                            "element_type": "link",
                            "zone_type": "main_content",
                            "tag": "a",
                            "aria_role": "link",
                        },
                        {
                            "selector": "h1",
                            "label": "Popular Movies",
                            "element_type": "heading",
                            "zone_type": "header",
                            "tag": "h1",
                        },
                    ]
                }
            }
        },
        element_inventory={
            "per_page": [
                {
                    "state_id": "state-a",
                    "interactive_elements": 1,
                    "non_interactive_elements": 1,
                    "total_elements": 2,
                }
            ]
        },
    )

    drilldown = _build_element_drilldown_map(
        result=result,
        element_inventory=result.element_inventory,
        execution_rows=[
            {
                "source_state_id": "state-a",
                "target_selector": "a[href='/movie/1']",
                "screenshot_link": "evidence/actions/1.png",
            }
        ],
        state_screenshot_links={"state-a": "evidence/states/state-a.png"},
    )

    row = drilldown["state-a"]
    assert row["catalog_entry_count"] == 2
    assert row["entries_truncated"] is False
    assert row["entries"][0]["selector"] == "a[href='/movie/1']"
    assert row["entries"][0]["label"] == "Movie card"
    assert row["entries"][0]["is_interactive"] is True
    assert row["entries"][0]["screenshot_link"] == "evidence/actions/1.png"
    assert row["entries"][0]["screenshot_source"] == "action_target"
    assert row["entries"][1]["is_interactive"] is False
    assert row["entries"][1]["screenshot_link"] == "evidence/actions/1.png"
    assert row["entries"][1]["screenshot_source"] == "state_action"
    assert row["top_types"][0] == {"name": "heading", "count": 1}
    assert row["top_types"][1] == {"name": "link", "count": 1}


def test_build_element_drilldown_map_truncates_large_entry_lists() -> None:
    entries = [
        {
            "selector": f".card:nth-of-type({i})",
            "label": f"Card {i}",
            "element_type": "heading",
            "zone_type": "main_content",
            "tag": "h2",
        }
        for i in range(260)
    ]
    result = ExplorationResult(
        states={
            "state-b": _make_state(
                state_id="state-b",
                title="Catalog",
                url="https://example.com/catalog",
            )
        },
        smart_analyses={"state-b": {"catalog": {"entries": entries}}},
    )

    drilldown = _build_element_drilldown_map(
        result=result,
        element_inventory=None,
        state_screenshot_links={"state-b": "evidence/states/state-b.png"},
    )

    row = drilldown["state-b"]
    assert row["entries_truncated"] is True
    assert len(row["entries"]) == 250
    assert row["catalog_entry_count"] == 260
    assert row["interactive"] == 0
    assert row["non_interactive"] == 260
    assert row["total"] == 260
    assert row["entries"][0]["screenshot_link"] == "evidence/states/state-b.png"
    assert row["entries"][0]["screenshot_source"] == "state_snapshot"

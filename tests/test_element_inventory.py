"""Tests for element inventory aggregation helpers."""

from flowscout.analysis.element_inventory import (
    is_interactive_element_type,
    summarize_element_inventory,
)
from flowscout.core.state import PageState


def _make_state(state_id: str, url: str) -> PageState:
    return PageState(
        state_id=state_id,
        url=url,
        title=state_id,
        fingerprint=f"{state_id * 6}fingerprint",
        depth=0,
        dom_structure_hash="dom",
        visible_text_hash="text",
        form_state_hash="form",
    )


def test_is_interactive_element_type_handles_inputs_and_controls() -> None:
    assert is_interactive_element_type("input_text")
    assert is_interactive_element_type("button")
    assert is_interactive_element_type("select")
    assert not is_interactive_element_type("heading")
    assert not is_interactive_element_type("image")


def test_summarize_element_inventory_builds_counts_and_page_rows() -> None:
    analyses = {
        "s1": {
            "catalog": {
                "entries": [
                    {"element_type": "link"},
                    {"element_type": "button"},
                    {"element_type": "input_text"},
                    {"element_type": "heading"},
                    {"element_type": "image"},
                ]
            }
        },
        "s2": {
            "catalog": {
                "entries": [
                    {"element_type": "select"},
                    {"element_type": "textarea"},
                    {"element_type": "other"},
                ]
            }
        },
    }
    states = {
        "s1": _make_state("s1", "https://example.com"),
        "s2": _make_state("s2", "https://example.com/details"),
    }

    summary = summarize_element_inventory(analyses=analyses, states_by_id=states)

    assert summary["pages_analyzed"] == 2
    assert summary["total_elements"] == 8
    assert summary["interactive_elements"] == 5
    assert summary["non_interactive_elements"] == 3
    assert summary["interactive_pct"] == 62
    assert summary["per_page"][0]["state_id"] == "s1"
    assert summary["per_page"][0]["total_elements"] == 5
    assert summary["top_interactive_types"][0] == {
        "element_type": "button",
        "count": 1,
    }

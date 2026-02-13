"""Tests for flow-template deduplication and reporting surfaces."""

from pathlib import Path

from rich.console import Console

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionType
from flowscout.modeling.flows import deduplicate_flows
from flowscout.modeling.site_model import SiteModel
from flowscout.reporting.html import HTMLReporter
from flowscout.reporting.terminal import TerminalReporter


def _state(*, state_id: str, url: str) -> PageState:
    return PageState(
        state_id=state_id,
        url=url,
        title=state_id,
        fingerprint=f"{state_id}-fingerprint".ljust(64, "x")[:64],
        depth=0,
        dom_structure_hash=f"{state_id}-dom",
        visible_text_hash=f"{state_id}-text",
        form_state_hash=f"{state_id}-form",
    )


def test_deduplicate_flows_groups_by_page_type_sequence() -> None:
    flows = [
        Flow(
            flow_id="flow-1",
            name="Listing to Detail 1",
            description="Open first tile",
            state_ids=["s-listing", "s-detail-1"],
            action_ids=["a-open-1"],
            stability_score=0.82,
        ),
        Flow(
            flow_id="flow-2",
            name="Listing to Detail 2",
            description="Open second tile",
            state_ids=["s-listing", "s-detail-2"],
            action_ids=["a-open-2"],
            stability_score=0.91,
        ),
    ]

    state_to_page_type = {
        "s-listing": "listing_sig",
        "s-detail-1": "detail_sig",
        "s-detail-2": "detail_sig",
    }
    actions = {
        "a-open-1": Action(
            action_id="a-open-1",
            action_type=ActionType.CLICK,
            target_selector="a.tile-1",
            label="Click tile 1",
        ),
        "a-open-2": Action(
            action_id="a-open-2",
            action_type=ActionType.CLICK,
            target_selector="a.tile-2",
            label="Click tile 2",
        ),
    }

    templates = deduplicate_flows(
        flows=flows,
        state_to_page_type=state_to_page_type,
        actions_by_id=actions,
    )

    assert len(templates) == 1
    template = templates[0]
    assert template.page_type_sequence == ["listing_sig", "detail_sig"]
    assert template.occurrence_count == 2
    assert template.representative_flow_id == "flow-2"
    assert template.instance_flow_ids == ["flow-1", "flow-2"]
    assert template.action_type_sequence == ["CLICK"]
    assert template.name == "Browse Listing \u2192 Detail"


def test_terminal_site_model_summary_includes_template_instance_counts() -> None:
    reporter = TerminalReporter(verbose=False)
    reporter.console = Console(record=True, force_terminal=False, width=140)

    model = SiteModel.model_validate(
        {
            "flow_templates": [
                {
                    "template_id": "flow-template-1",
                    "name": "Browse Listing \u2192 Detail",
                    "page_type_sequence": ["listing_sig", "detail_sig"],
                    "occurrence_count": 10,
                    "representative_flow_id": "flow-9",
                    "instance_flow_ids": [f"flow-{index}" for index in range(10)],
                    "action_type_sequence": ["CLICK"],
                    "stability_score": 0.84,
                }
            ]
        }
    )

    reporter.print_site_model_summary(model)
    output = reporter.console.export_text()

    assert "Flow Templates" in output
    assert "Browse Listing → Detail (10 instances)" in output


def test_html_report_groups_test_suites_by_flow_template(tmp_path: Path) -> None:
    output = tmp_path / "report.html"
    result = ExplorationResult(
        config={"start_url": "https://example.com", "strategy": "priority"},
        states={
            "s-listing": _state(state_id="s-listing", url="https://example.com/movies"),
            "s-detail-1": _state(
                state_id="s-detail-1", url="https://example.com/movies/1"
            ),
            "s-detail-2": _state(
                state_id="s-detail-2", url="https://example.com/movies/2"
            ),
        },
        smart_analyses={
            "s-listing": {"structural_signature": "listing_sig"},
            "s-detail-1": {"structural_signature": "detail_sig"},
            "s-detail-2": {"structural_signature": "detail_sig"},
        },
        flows=[
            Flow(
                flow_id="flow-1",
                name="Movie 1 detail",
                description="Open movie 1",
                state_ids=["s-listing", "s-detail-1"],
                action_ids=["a1"],
                category="Catalog",
            ),
            Flow(
                flow_id="flow-2",
                name="Movie 2 detail",
                description="Open movie 2",
                state_ids=["s-listing", "s-detail-2"],
                action_ids=["a2"],
                category="Catalog",
            ),
        ],
    )

    HTMLReporter().generate(result, str(output))
    html = output.read_text()

    assert "Flow Templates" in html
    assert (
        "Browse Listing Page \u2192 Detail Page" in html
        or "Browse Listing \u2192 Detail" in html
    )
    assert "2 instances" in html
    assert "Show all instances" in html
    assert "Movie 1 detail" in html
    assert "Movie 2 detail" in html

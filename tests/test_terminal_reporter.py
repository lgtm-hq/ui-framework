"""Tests for terminal reporter banner output."""

from rich.console import Console

from flowscout.analysis.graph import ExplorationResult
from flowscout.core.action_types import ActionType
from flowscout.core.state import ExplorerConfig, PageBlockReason, PageState
from flowscout.modeling.scenarios import FlowScenario, ScenarioStep
from flowscout.modeling.site_model import NavigationEdge, PageType, SiteModel
from flowscout.reporting.terminal import TerminalReporter


def _base_config() -> ExplorerConfig:
    return ExplorerConfig(
        start_url="https://example.com",
        max_depth=2,
        max_states=30,
        max_actions_per_state=15,
        headless=True,
        take_screenshots=True,
    )


def test_print_banner_includes_smart_detection_metrics_when_enabled() -> None:
    reporter = TerminalReporter(verbose=False)
    reporter.console = Console(record=True, force_terminal=False, width=120)
    config = _base_config().model_copy(
        update={
            "smart_mode": True,
            "smart_stop_on_saturation": False,
            "smart_min_archetypes_before_stop": 4,
            "smart_min_features_before_stop": 6,
            "smart_archetype_instance_limit": 8,
        }
    )

    reporter.print_banner("https://example.com", config)
    output = reporter.console.export_text()

    assert "Smart mode: ON" in output
    assert "Saturation stop: OFF" in output
    assert "Min archetypes: 4" in output
    assert "Min features: 6" in output
    assert "Signature repeat limit: 8" in output


def test_print_banner_hides_smart_detection_metrics_when_disabled() -> None:
    reporter = TerminalReporter(verbose=False)
    reporter.console = Console(record=True, force_terminal=False, width=120)
    config = _base_config().model_copy(update={"smart_mode": False})

    reporter.print_banner("https://example.com", config)
    output = reporter.console.export_text()

    assert "Smart mode: ON" not in output
    assert "Saturation stop" not in output


def test_print_site_model_summary_includes_mbt_coverage_metrics() -> None:
    """Site model summaries should include explicit MBT coverage percentages."""
    reporter = TerminalReporter(verbose=False)
    reporter.console = Console(record=True, force_terminal=False, width=120)
    model = SiteModel(
        page_types=[
            PageType(page_type_id="home", name="Home"),
            PageType(page_type_id="catalog", name="Catalog"),
            PageType(page_type_id="detail", name="Detail"),
        ],
        navigation_edges=[
            NavigationEdge(
                from_page_type="home",
                to_page_type="catalog",
                trigger="Open catalog",
                action_type=ActionType.CLICK,
                occurrence_count=1,
            ),
            NavigationEdge(
                from_page_type="catalog",
                to_page_type="detail",
                trigger="Open detail",
                action_type=ActionType.CLICK,
                occurrence_count=1,
            ),
        ],
        test_scenarios=[
            FlowScenario(
                scenario_id="mbt-edge-1",
                name="MBT edge 1",
                description="Edge walk",
                page_type_sequence=["home", "catalog"],
                steps=[
                    ScenarioStep(
                        page_type="home",
                        action_description="Navigate to Home",
                        action_type=ActionType.NAVIGATE,
                    ),
                    ScenarioStep(
                        page_type="home",
                        action_description="click via Open catalog",
                        action_type=ActionType.CLICK,
                    ),
                ],
                template="mbt_edge_coverage",
                tags=["mbt"],
            ),
        ],
    )

    reporter.print_site_model_summary(model)
    output = reporter.console.export_text()

    assert "State coverage: 67% (2/3 states)" in output
    assert "Edge coverage: 50% (1/2 edges)" in output
    assert "Uncovered edges: catalog->detail (click)" in output


def test_print_summary_includes_blocked_state_count() -> None:
    reporter = TerminalReporter(verbose=False)
    reporter.console = Console(record=True, force_terminal=False, width=120)
    blocked_state = PageState(
        state_id="s1",
        url="https://example.com/forbidden",
        title="Forbidden",
        fingerprint="f" * 64,
        depth=0,
        dom_structure_hash="dom1",
        visible_text_hash="text1",
        form_state_hash="form1",
        block_reason=PageBlockReason.ACCESS_DENIED,
        block_detail="HTTP 403 response from page navigation",
    )
    result = ExplorationResult(
        states={"s1": blocked_state},
        stats={
            "total_states": 1,
            "total_actions_executed": 0,
            "total_unique_actions": 0,
        },
    )

    reporter.print_summary(result)
    output = reporter.console.export_text()

    assert "Blocked states" in output
    assert "1" in output

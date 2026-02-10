"""Tests for terminal reporter banner output."""

from rich.console import Console

from flowscout.core.state import ExplorerConfig
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

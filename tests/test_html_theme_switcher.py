"""Tests for report theme-switcher rendering."""

from pathlib import Path

from flowscout.analysis.graph import ExplorationResult
from flowscout.reporting.html import HTMLReporter


def test_report_renders_turbo_theme_assets_and_selector(tmp_path: Path) -> None:
    output = tmp_path / "report.html"
    result = ExplorationResult(
        config={
            "start_url": "https://example.com",
            "strategy": "priority",
        }
    )

    HTMLReporter().generate(result, str(output))
    html = output.read_text()

    assert "turbo-core.css" in html
    assert "turbo-base.css" in html
    assert 'id="turbo-theme-stylesheet"' in html
    assert 'id="theme-picker-select"' in html
    assert "flowscout-report-theme" in html
    assert "catppuccin-mocha" in html
    assert "tokyo-night-storm" in html

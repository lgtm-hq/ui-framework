"""Tests for report theme-switcher rendering."""

from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.analysis.narrative import FlowNarrative, NarrativeStep
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
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


def test_report_moves_selector_into_flow_timeline_table(tmp_path: Path) -> None:
    output = tmp_path / "report.html"
    result = ExplorationResult(
        config={
            "start_url": "https://www.saucedemo.com/",
            "strategy": "priority",
        },
        states={
            "s1": PageState(
                state_id="s1",
                url="https://www.saucedemo.com/",
                title="Swag Labs",
                fingerprint="a" * 64,
                depth=0,
                dom_structure_hash="dom",
                visible_text_hash="text",
                form_state_hash="form",
            ),
            "s2": PageState(
                state_id="s2",
                url="https://www.saucedemo.com/",
                title="Swag Labs",
                fingerprint="b" * 64,
                depth=0,
                dom_structure_hash="dom2",
                visible_text_hash="text2",
                form_state_hash="form2",
            ),
        },
        actions={
            "a1": Action(
                action_id="a1",
                action_type=ActionType.FILL,
                target_selector="#user-name",
                label="Fill: Username = 'janedoe42'",
                metadata={"dom_id": "user-name"},
            )
        },
        results=[
            ActionResult(
                action_id="a1",
                source_state_id="s1",
                target_state_id="s2",
                outcome=OutcomeType.NO_CHANGE,
                confidence=0.55,
                duration_ms=220,
                expected="The username field should contain the entered value",
                actual="No visible UI change observed",
            )
        ],
        flows=[
            Flow(
                flow_id="f1",
                name="Swag Labs · Enter Username · No Visible Change",
                description="Fill username",
                state_ids=["s1", "s2"],
                action_ids=["a1"],
                outcomes=[OutcomeType.NO_CHANGE],
                depth=1,
                category="Form",
                tags=["form"],
                narrative=FlowNarrative(
                    title="Swag Labs · Enter Username · No Visible Change",
                    precondition='I am on the "Swag Labs" page (https://www.saucedemo.com/)',
                    steps=[
                        NarrativeStep(
                            step_number=1,
                            action_description="Enter 'janedoe42' into the Username field",
                            expected="The user-name field should contain the entered value",
                            actual="No visible UI change observed",
                            target_selector="#user-name",
                            target_description="Username",
                        )
                    ],
                    conclusion="All 1 steps passed",
                    gherkin="Scenario: Enter username",
                ),
            )
        ],
    )

    HTMLReporter().generate(result, str(output))
    html = output.read_text()

    assert "show technical selector" not in html
    assert "<th>Locator</th>" in html
    assert "#user-name" in html


def test_report_modal_styles_use_theme_tokens(tmp_path: Path) -> None:
    output = tmp_path / "report.html"
    result = ExplorationResult(
        config={
            "start_url": "https://example.com",
            "strategy": "priority",
        }
    )

    HTMLReporter().generate(result, str(output))
    html = output.read_text()

    assert "--modal-overlay:" in html
    assert "--modal-shell-start:" in html
    assert "var(--modal-shell-start)" in html
    assert "var(--modal-card-start)" in html
    assert "rgba(0, 8, 18, 0.78)" not in html
    assert "linear-gradient(180deg, #0c151f 0%, #0a121a 100%)" not in html
    assert "rgba(45, 212, 191, 0.10)" not in html

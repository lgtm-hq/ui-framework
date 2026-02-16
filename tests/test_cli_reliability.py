"""Tests for the reliability CLI command."""

from __future__ import annotations

from typing import Any

from click.testing import CliRunner

import flowscout.cli.reliability as reliability_cli
from flowscout.cli import main


class _FakeReliabilityDB:
    """Small DB test double for reliability command tests."""

    def __init__(
        self,
        *,
        actions: list[dict[str, Any]],
        flaky: list[dict[str, Any]],
    ) -> None:
        self._actions = actions
        self._flaky = flaky
        self.closed = False

    def get_action_reliability(
        self, start_url: str | None = None
    ) -> list[dict[str, Any]]:
        return self._actions

    def get_flaky_actions(
        self, start_url: str, min_runs: int = 2
    ) -> list[dict[str, Any]]:
        return self._flaky

    def close(self) -> None:
        self.closed = True


def test_reliability_prints_empty_state(monkeypatch: Any) -> None:
    """Reliability command should show empty-state when no data exists."""
    fake_db = _FakeReliabilityDB(actions=[], flaky=[])
    monkeypatch.setattr(reliability_cli, "FlowscoutDB", lambda _path: fake_db)
    result = CliRunner().invoke(main, ["reliability", "--url", "https://example.com"])
    assert result.exit_code == 0
    assert "No data found" in result.output


def test_reliability_renders_tables_with_new_columns(monkeypatch: Any) -> None:
    """Reliability output should include visual/other outcome columns."""
    actions = [
        {
            "label": "Click login",
            "total_attempts": 4,
            "navigations": 2,
            "dom_changes": 1,
            "visual_changes": 1,
            "errors": 0,
            "no_changes": 0,
            "other_outcomes": 0,
        }
    ]
    flaky = [
        {
            "label": "Click login",
            "runs_seen": 3,
            "outcomes_seen": "navigation,no_change",
        }
    ]
    fake_db = _FakeReliabilityDB(actions=actions, flaky=flaky)
    monkeypatch.setattr(reliability_cli, "FlowscoutDB", lambda _path: fake_db)

    result = CliRunner().invoke(main, ["reliability", "--url", "https://example.com"])
    assert result.exit_code == 0
    assert "Action Reliability" in result.output
    assert "Visual" in result.output
    assert "Other" in result.output
    assert "Flaky Actions" in result.output

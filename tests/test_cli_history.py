"""Tests for the history CLI command."""

from __future__ import annotations

from typing import Any

from click.testing import CliRunner

import flowscout.cli.history as history_cli
from flowscout.cli import main


class _FakeDB:
    """Small DB test double for history command tests."""

    def __init__(self, runs: list[dict[str, Any]]) -> None:
        self._runs = runs
        self.closed = False

    def list_runs(
        self,
        *,
        start_url: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        rows = self._runs[:limit]
        if start_url:
            return [row for row in rows if row["start_url"] == start_url]
        return rows

    def close(self) -> None:
        self.closed = True


def test_history_prints_empty_message(monkeypatch: Any) -> None:
    """History command should show empty-state message when no runs exist."""
    monkeypatch.setattr(history_cli, "FlowscoutDB", lambda _path: _FakeDB([]))
    result = CliRunner().invoke(main, ["history"])
    assert result.exit_code == 0
    assert "No runs found" in result.output


def test_history_renders_table_for_runs(monkeypatch: Any) -> None:
    """History command should render rows when runs are present."""
    rows = [
        {
            "run_id": "run_1",
            "start_url": "https://example.com",
            "started_at": "2026-02-13T12:00:00Z",
            "duration_seconds": 1.2,
            "total_states": 3,
            "total_actions": 5,
            "total_flows": 2,
        }
    ]
    monkeypatch.setattr(history_cli, "FlowscoutDB", lambda _path: _FakeDB(rows))
    result = CliRunner().invoke(main, ["history", "--limit", "5"])
    assert result.exit_code == 0
    assert "Exploration History" in result.output
    assert "run_1" in result.output
    assert "https://exam" in result.output

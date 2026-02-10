"""Tests for FlowscoutDB with in-memory SQLite."""

from __future__ import annotations

import sqlite3


from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.storage.db import FlowscoutDB

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _in_memory_db() -> FlowscoutDB:
    """Create a FlowscoutDB backed by an in-memory SQLite connection."""
    conn = sqlite3.connect(":memory:")
    return FlowscoutDB.from_connection(conn)


def _make_result(
    *,
    start_url: str = "https://example.com",
    num_states: int = 2,
    num_actions: int = 1,
    num_flows: int = 1,
) -> ExplorationResult:
    """Build a minimal ExplorationResult for save_run round-trip tests."""
    states = {}
    for i in range(num_states):
        sid = f"state-{i}"
        states[sid] = PageState(
            state_id=sid,
            url=f"https://example.com/page{i}",
            title=f"Page {i}",
            fingerprint=f"fp-{i}",
            depth=i,
            dom_structure_hash=f"dom-{i}",
            visible_text_hash=f"text-{i}",
            form_state_hash=f"form-{i}",
        )

    actions = {}
    results = []
    for i in range(num_actions):
        aid = f"act-{i}"
        actions[aid] = Action(
            action_id=aid,
            action_type=ActionType.CLICK,
            target_selector=f"button#{i}",
            label=f"Click button {i}",
        )
        results.append(
            ActionResult(
                action_id=aid,
                source_state_id="state-0",
                target_state_id=f"state-{min(i + 1, num_states - 1)}",
                outcome=(
                    OutcomeType.NAVIGATION if num_states > 1 else OutcomeType.NO_CHANGE
                ),
                duration_ms=100.0,
                url_before="https://example.com/page0",
                url_after=f"https://example.com/page{min(i + 1, num_states - 1)}",
            ),
        )

    flows = []
    for i in range(num_flows):
        flows.append(
            Flow(
                flow_id=f"flow-{i}",
                name=f"Flow {i}",
                description=f"Test flow {i}",
                state_ids=list(states.keys()),
                action_ids=list(actions.keys()),
                outcomes=[OutcomeType.NAVIGATION],
                depth=1,
            ),
        )

    return ExplorationResult(
        config={"start_url": start_url},
        started_at="2025-01-01T00:00:00Z",
        finished_at="2025-01-01T00:01:00Z",
        duration_seconds=60.0,
        states=states,
        actions=actions,
        results=results,
        flows=flows,
        stats={"total_states": num_states, "total_actions": num_actions},
    )


# ---------------------------------------------------------------------------
# Tests: from_connection
# ---------------------------------------------------------------------------


class TestFromConnection:
    """Tests for the from_connection classmethod."""

    def test_creates_db_with_schema(self) -> None:
        db = _in_memory_db()
        # Tables should exist
        tables = db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
        ).fetchall()
        table_names = {row["name"] for row in tables}
        assert "runs" in table_names
        assert "states" in table_names
        assert "actions" in table_names
        assert "results" in table_names
        assert "flows" in table_names

    def test_migrations_applied(self) -> None:
        db = _in_memory_db()
        # The verdict column should exist in results (from migrations)
        cols = [
            row[1] for row in db.conn.execute("PRAGMA table_info(results)").fetchall()
        ]
        assert "verdict" in cols
        assert "verdict_reason" in cols
        assert "expected" in cols
        assert "actual" in cols

    def test_from_connection_path_is_memory(self) -> None:
        db = _in_memory_db()
        assert str(db.db_path) == ":memory:"


# ---------------------------------------------------------------------------
# Tests: save_run round-trip
# ---------------------------------------------------------------------------


class TestSaveRunRoundTrip:
    """Tests for saving and reading back exploration runs."""

    def test_save_and_list_runs(self) -> None:
        db = _in_memory_db()
        result = _make_result()
        run_id = db.save_run(result)

        runs = db.list_runs()
        assert len(runs) == 1
        assert runs[0]["run_id"] == run_id
        assert runs[0]["start_url"] == "https://example.com"

    def test_save_and_get_run(self) -> None:
        db = _in_memory_db()
        result = _make_result()
        run_id = db.save_run(result)

        run = db.get_run(run_id)
        assert run is not None
        assert run["duration_seconds"] == 60.0
        assert run["total_states"] == 2

    def test_get_nonexistent_run_returns_none(self) -> None:
        db = _in_memory_db()
        assert db.get_run("nonexistent") is None

    def test_save_and_get_run_states(self) -> None:
        db = _in_memory_db()
        result = _make_result(num_states=3)
        run_id = db.save_run(result)

        states = db.get_run_states(run_id)
        assert len(states) == 3
        assert states[0]["url"] == "https://example.com/page0"

    def test_save_and_get_run_results(self) -> None:
        db = _in_memory_db()
        result = _make_result(num_actions=2, num_states=3)
        run_id = db.save_run(result)

        results = db.get_run_results(run_id)
        assert len(results) == 2

    def test_save_and_get_run_flows(self) -> None:
        db = _in_memory_db()
        result = _make_result(num_flows=2)
        run_id = db.save_run(result)

        flows = db.get_run_flows(run_id)
        assert len(flows) == 2
        assert flows[0]["name"] == "Flow 0"


# ---------------------------------------------------------------------------
# Tests: list_runs with filtering
# ---------------------------------------------------------------------------


class TestListRuns:
    """Tests for list_runs filtering and ordering."""

    def test_filter_by_start_url(self) -> None:
        db = _in_memory_db()
        db.save_run(_make_result(start_url="https://a.com"))
        db.save_run(_make_result(start_url="https://b.com"))

        runs_a = db.list_runs(start_url="https://a.com")
        assert len(runs_a) == 1
        assert runs_a[0]["start_url"] == "https://a.com"

    def test_limit_results(self) -> None:
        db = _in_memory_db()
        for _ in range(5):
            db.save_run(_make_result())

        runs = db.list_runs(limit=3)
        assert len(runs) == 3


# ---------------------------------------------------------------------------
# Tests: cross-run analysis
# ---------------------------------------------------------------------------


class TestCrossRunAnalysis:
    """Tests for cross-run state comparison and flaky action detection."""

    def test_get_new_states_since(self) -> None:
        db = _in_memory_db()
        result1 = _make_result(num_states=2)
        db.save_run(result1)

        # Second run with an extra state
        result2 = _make_result(num_states=3)
        run_id2 = db.save_run(result2)

        new_states = db.get_new_states_since(run_id2)
        # state-2 (fp-2) is new in run2
        new_fps = {s["fingerprint"] for s in new_states}
        assert "fp-2" in new_fps

    def test_get_disappeared_states(self) -> None:
        db = _in_memory_db()
        # First run: 3 states, with earlier timestamp
        result1 = _make_result(num_states=3)
        result1.started_at = "2025-01-01T00:00:00Z"
        result1.finished_at = "2025-01-01T00:01:00Z"
        db.save_run(result1)

        # Second run: 2 states (missing state-2), with later timestamp
        result2 = _make_result(num_states=2)
        result2.started_at = "2025-01-02T00:00:00Z"
        result2.finished_at = "2025-01-02T00:01:00Z"
        run_id2 = db.save_run(result2)

        disappeared = db.get_disappeared_states(run_id2)
        disappeared_fps = {s["fingerprint"] for s in disappeared}
        assert "fp-2" in disappeared_fps

    def test_get_disappeared_states_nonexistent_run(self) -> None:
        db = _in_memory_db()
        assert db.get_disappeared_states("nonexistent") == []

    def test_get_state_history(self) -> None:
        db = _in_memory_db()
        db.save_run(_make_result())
        db.save_run(_make_result())

        history = db.get_state_history("https://example.com/page0")
        assert len(history) == 2

    def test_get_action_reliability(self) -> None:
        db = _in_memory_db()
        db.save_run(_make_result(num_actions=2, num_states=3))

        reliability = db.get_action_reliability()
        assert len(reliability) > 0
        assert reliability[0]["total_attempts"] >= 1

    def test_get_action_reliability_filtered_by_url(self) -> None:
        db = _in_memory_db()
        db.save_run(_make_result(start_url="https://a.com"))
        db.save_run(_make_result(start_url="https://b.com"))

        reliability = db.get_action_reliability(start_url="https://a.com")
        # Should only include actions from the a.com run
        assert len(reliability) >= 1

    def test_get_flaky_actions_requires_min_runs(self) -> None:
        db = _in_memory_db()
        # Only one run — flaky detection requires min_runs=2
        db.save_run(_make_result())

        flaky = db.get_flaky_actions("https://example.com")
        assert len(flaky) == 0


# ---------------------------------------------------------------------------
# Tests: close
# ---------------------------------------------------------------------------


class TestClose:
    """Tests for connection lifecycle."""

    def test_close_idempotent(self) -> None:
        db = _in_memory_db()
        db.close()
        db.close()  # Should not raise

"""SQLite persistent storage for exploration history across runs."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flowscout.analysis.graph import ExplorationResult

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id          TEXT PRIMARY KEY,
    start_url       TEXT NOT NULL,
    started_at      TEXT NOT NULL,
    finished_at     TEXT NOT NULL,
    duration_seconds REAL NOT NULL,
    config_json     TEXT NOT NULL,
    stats_json      TEXT NOT NULL,
    total_states    INTEGER NOT NULL DEFAULT 0,
    total_actions   INTEGER NOT NULL DEFAULT 0,
    total_flows     INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS states (
    state_id        TEXT NOT NULL,
    run_id          TEXT NOT NULL,
    url             TEXT NOT NULL,
    title           TEXT NOT NULL DEFAULT '',
    fingerprint     TEXT NOT NULL,
    depth           INTEGER NOT NULL DEFAULT 0,
    dom_hash        TEXT NOT NULL DEFAULT '',
    text_hash       TEXT NOT NULL DEFAULT '',
    form_hash       TEXT NOT NULL DEFAULT '',
    signals_json    TEXT NOT NULL DEFAULT '[]',
    screenshot_path TEXT,
    discovered_at   TEXT NOT NULL,
    PRIMARY KEY (state_id, run_id),
    FOREIGN KEY (run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS actions (
    action_id       TEXT NOT NULL,
    run_id          TEXT NOT NULL,
    action_type     TEXT NOT NULL,
    target_selector TEXT NOT NULL,
    label           TEXT NOT NULL DEFAULT '',
    value           TEXT,
    metadata_json   TEXT NOT NULL DEFAULT '{}',
    priority        INTEGER NOT NULL DEFAULT 50,
    PRIMARY KEY (action_id, run_id),
    FOREIGN KEY (run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT NOT NULL,
    action_id       TEXT NOT NULL,
    source_state_id TEXT NOT NULL,
    target_state_id TEXT NOT NULL,
    outcome         TEXT NOT NULL,
    duration_ms     REAL NOT NULL DEFAULT 0,
    message         TEXT NOT NULL DEFAULT '',
    url_before      TEXT NOT NULL DEFAULT '',
    url_after       TEXT NOT NULL DEFAULT '',
    error_messages_json TEXT NOT NULL DEFAULT '[]',
    console_errors_json TEXT NOT NULL DEFAULT '[]',
    screenshot_path TEXT DEFAULT '',
    executed_at     TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS flows (
    flow_id         TEXT NOT NULL,
    run_id          TEXT NOT NULL,
    name            TEXT NOT NULL,
    description     TEXT NOT NULL DEFAULT '',
    state_ids_json  TEXT NOT NULL DEFAULT '[]',
    action_ids_json TEXT NOT NULL DEFAULT '[]',
    outcomes_json   TEXT NOT NULL DEFAULT '[]',
    is_cycle        INTEGER NOT NULL DEFAULT 0,
    depth           INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (flow_id, run_id),
    FOREIGN KEY (run_id) REFERENCES runs(run_id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_states_url ON states(url);
CREATE INDEX IF NOT EXISTS idx_states_fingerprint ON states(fingerprint);
CREATE INDEX IF NOT EXISTS idx_results_outcome ON results(outcome);
CREATE INDEX IF NOT EXISTS idx_results_source ON results(source_state_id);
CREATE INDEX IF NOT EXISTS idx_runs_start_url ON runs(start_url);
"""


_KNOWN_TABLES = frozenset({"runs", "states", "actions", "results", "flows"})

_MIGRATIONS: list[tuple[str, str, str]] = [
    ("results", "verdict", "ALTER TABLE results ADD COLUMN verdict TEXT DEFAULT ''"),
    (
        "results",
        "verdict_reason",
        "ALTER TABLE results ADD COLUMN verdict_reason TEXT DEFAULT ''",
    ),
    ("results", "expected", "ALTER TABLE results ADD COLUMN expected TEXT DEFAULT ''"),
    ("results", "actual", "ALTER TABLE results ADD COLUMN actual TEXT DEFAULT ''"),
    (
        "results",
        "screenshot_path",
        "ALTER TABLE results ADD COLUMN screenshot_path TEXT DEFAULT ''",
    ),
    ("flows", "verdict", "ALTER TABLE flows ADD COLUMN verdict TEXT DEFAULT ''"),
    (
        "flows",
        "narrative_json",
        "ALTER TABLE flows ADD COLUMN narrative_json TEXT DEFAULT ''",
    ),
]


class FlowscoutDB:
    """SQLite storage for exploration history."""

    def __init__(self, db_path: str = ".flowscout/history.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._conn.executescript(_SCHEMA)
            self._apply_migrations()
        return self._conn

    def _apply_migrations(self) -> None:
        """Apply schema migrations (add columns if they don't exist)."""
        for table, column, sql in _MIGRATIONS:
            if table not in _KNOWN_TABLES:
                logger.warning("Skipping migration for unknown table: %s", table)
                continue
            try:
                cols = [
                    row[1]
                    for row in self._conn.execute(
                        f"PRAGMA table_info({table})"
                    ).fetchall()  # type: ignore[union-attr]
                ]
                if column not in cols:
                    self._conn.execute(sql)  # type: ignore[union-attr]
            except Exception:
                logger.debug("Migration failed for %s.%s", table, column, exc_info=True)

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # ── Saving ──

    def save_run(self, result: ExplorationResult) -> str:
        """Save a complete exploration run. Returns the run_id."""
        run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

        self.conn.execute(
            """INSERT INTO runs
               (run_id, start_url, started_at, finished_at, duration_seconds,
                config_json, stats_json, total_states, total_actions, total_flows)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                run_id,
                result.config.get("start_url", ""),
                result.started_at,
                result.finished_at,
                result.duration_seconds,
                json.dumps(result.config),
                json.dumps(result.stats),
                len(result.states),
                len(result.results),
                len(result.flows),
            ),
        )

        # States
        for state in result.states.values():
            self.conn.execute(
                """INSERT OR REPLACE INTO states
                   (state_id, run_id, url, title, fingerprint, depth,
                    dom_hash, text_hash, form_hash, signals_json,
                    screenshot_path, discovered_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    state.state_id,
                    run_id,
                    state.url,
                    state.title,
                    state.fingerprint,
                    state.depth,
                    state.dom_structure_hash,
                    state.visible_text_hash,
                    state.form_state_hash,
                    json.dumps(state.signals),
                    state.screenshot_path,
                    state.timestamp,
                ),
            )

        # Actions
        for action in result.actions.values():
            self.conn.execute(
                """INSERT OR REPLACE INTO actions
                   (action_id, run_id, action_type, target_selector,
                    label, value, metadata_json, priority)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    action.action_id,
                    run_id,
                    action.action_type.value,
                    action.target_selector,
                    action.label,
                    action.value,
                    json.dumps(action.metadata),
                    action.priority,
                ),
            )

        # Results
        for r in result.results:
            self.conn.execute(
                """INSERT INTO results
                   (run_id, action_id, source_state_id, target_state_id,
                    outcome, duration_ms, message, url_before, url_after,
                    error_messages_json, console_errors_json, screenshot_path, executed_at,
                    verdict, verdict_reason, expected, actual)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    run_id,
                    r.action_id,
                    r.source_state_id,
                    r.target_state_id,
                    r.outcome.value,
                    r.duration_ms,
                    r.message,
                    r.url_before,
                    r.url_after,
                    json.dumps(r.error_messages),
                    json.dumps(r.console_errors),
                    r.screenshot_path or "",
                    r.timestamp,
                    r.verdict or "",
                    r.verdict_reason or "",
                    r.expected or "",
                    r.actual or "",
                ),
            )

        # Flows
        for flow in result.flows:
            verdict_str = ""
            if flow.verdict and hasattr(flow.verdict, "verdict"):
                verdict_str = flow.verdict.verdict.value
            narrative_json = ""
            if flow.narrative:
                try:
                    narrative_json = flow.narrative.model_dump_json()
                except Exception:
                    logger.debug("Failed to serialize narrative", exc_info=True)

            self.conn.execute(
                """INSERT OR REPLACE INTO flows
                   (flow_id, run_id, name, description, state_ids_json,
                    action_ids_json, outcomes_json, is_cycle, depth,
                    verdict, narrative_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    flow.flow_id,
                    run_id,
                    flow.name,
                    flow.description,
                    json.dumps(flow.state_ids),
                    json.dumps(flow.action_ids),
                    json.dumps([o.value for o in flow.outcomes]),
                    int(flow.is_cycle),
                    flow.depth,
                    verdict_str,
                    narrative_json,
                ),
            )

        self.conn.commit()
        return run_id

    # ── Querying ──

    def list_runs(self, *, start_url: str | None = None, limit: int = 20) -> list[dict]:
        """List exploration runs, most recent first."""
        query = "SELECT * FROM runs"
        params: list = []
        if start_url:
            query += " WHERE start_url = ?"
            params.append(start_url)
        query += " ORDER BY started_at DESC LIMIT ?"
        params.append(limit)

        rows = self.conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_run(self, run_id: str) -> dict | None:
        """Get a single run by ID."""
        row = self.conn.execute(
            "SELECT * FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_run_states(self, run_id: str) -> list[dict]:
        """Get all states from a run."""
        rows = self.conn.execute(
            "SELECT * FROM states WHERE run_id = ? ORDER BY depth, discovered_at",
            (run_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_run_results(self, run_id: str) -> list[dict]:
        """Get all action results from a run."""
        rows = self.conn.execute(
            "SELECT * FROM results WHERE run_id = ? ORDER BY id",
            (run_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_run_flows(self, run_id: str) -> list[dict]:
        """Get all flows from a run."""
        rows = self.conn.execute(
            "SELECT * FROM flows WHERE run_id = ? ORDER BY flow_id",
            (run_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Cross-run analysis ──

    def get_state_history(self, url: str) -> list[dict]:
        """Get all states ever observed at a given URL, across runs."""
        rows = self.conn.execute(
            """SELECT s.*, r.started_at as run_started_at, r.run_id
               FROM states s
               JOIN runs r ON s.run_id = r.run_id
               WHERE s.url = ?
               ORDER BY r.started_at DESC""",
            (url,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_action_reliability(self, start_url: str | None = None) -> list[dict]:
        """Get success/failure rates for each action across runs.

        Returns action label, total attempts, and outcome breakdown.
        """
        query = """
            SELECT
                a.label,
                a.action_type,
                a.target_selector,
                COUNT(*) as total_attempts,
                SUM(CASE WHEN res.outcome = 'navigation' THEN 1 ELSE 0 END) as navigations,
                SUM(CASE WHEN res.outcome = 'dom_change' THEN 1 ELSE 0 END) as dom_changes,
                SUM(CASE WHEN res.outcome = 'no_change' THEN 1 ELSE 0 END) as no_changes,
                SUM(CASE WHEN res.outcome IN ('timeout', 'exception', 'validation_error', 'network_error', 'console_error') THEN 1 ELSE 0 END) as errors
            FROM results res
            JOIN actions a ON res.action_id = a.action_id AND res.run_id = a.run_id
        """
        params: list = []
        if start_url:
            query += " JOIN runs r ON res.run_id = r.run_id WHERE r.start_url = ?"
            params.append(start_url)
        query += " GROUP BY a.label, a.action_type, a.target_selector ORDER BY total_attempts DESC"

        rows = self.conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_new_states_since(self, run_id: str) -> list[dict]:
        """Find states in this run that weren't seen in any previous run."""
        rows = self.conn.execute(
            """SELECT s.*
               FROM states s
               WHERE s.run_id = ?
               AND s.fingerprint NOT IN (
                   SELECT s2.fingerprint
                   FROM states s2
                   JOIN runs r2 ON s2.run_id = r2.run_id
                   WHERE r2.started_at < (SELECT started_at FROM runs WHERE run_id = ?)
               )""",
            (run_id, run_id),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_disappeared_states(self, run_id: str) -> list[dict]:
        """Find states from the previous run of the same URL that are missing in this run."""
        run = self.get_run(run_id)
        if not run:
            return []

        rows = self.conn.execute(
            """SELECT DISTINCT s.*
               FROM states s
               JOIN runs r ON s.run_id = r.run_id
               WHERE r.start_url = ?
               AND r.started_at < ?
               AND s.fingerprint NOT IN (
                   SELECT s2.fingerprint
                   FROM states s2
                   WHERE s2.run_id = ?
               )
               ORDER BY r.started_at DESC""",
            (run["start_url"], run["started_at"], run_id),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_flaky_actions(self, start_url: str, min_runs: int = 2) -> list[dict]:
        """Find actions that produce different outcomes across runs.

        These are "flaky" — sometimes they work, sometimes they don't.
        """
        rows = self.conn.execute(
            """SELECT
                a.label,
                a.target_selector,
                COUNT(DISTINCT res.outcome) as outcome_variety,
                COUNT(DISTINCT res.run_id) as runs_seen,
                GROUP_CONCAT(DISTINCT res.outcome) as outcomes_seen
               FROM results res
               JOIN actions a ON res.action_id = a.action_id AND res.run_id = a.run_id
               JOIN runs r ON res.run_id = r.run_id
               WHERE r.start_url = ?
               GROUP BY a.label, a.target_selector
               HAVING COUNT(DISTINCT res.outcome) > 1 AND COUNT(DISTINCT res.run_id) >= ?
               ORDER BY outcome_variety DESC""",
            (start_url, min_runs),
        ).fetchall()
        return [dict(r) for r in rows]

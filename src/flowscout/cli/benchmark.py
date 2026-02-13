"""Benchmark command — metrics aggregation and gate evaluation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click
from rich.table import Table

from flowscout.analysis.graph import ExplorationResult
from flowscout.cli.app import (
    DEFAULT_DB_PATH,
    DEFAULT_LOW_CONFIDENCE_THRESHOLD,
    console,
    main,
)
from flowscout.storage.db import FlowscoutDB


def _compute_benchmark_metrics(
    result: ExplorationResult,
    *,
    low_confidence_threshold: float = DEFAULT_LOW_CONFIDENCE_THRESHOLD,
) -> dict[str, int | float | bool]:
    """Compute key v1 benchmark metrics from an exploration result."""

    def _result_stability_score(action_result: Any) -> float:
        """Return normalized stability score for current/legacy artifacts."""
        score = float(getattr(action_result, "stability_score", 0.0) or 0.0)
        if score > 0:
            return score
        return float(getattr(action_result, "confidence", 0.0) or 0.0)

    def _result_stability_note(action_result: Any) -> str:
        """Return observation note for current/legacy artifacts."""
        note = str(getattr(action_result, "observation_notes", "") or "").strip()
        if note:
            return note
        return str(getattr(action_result, "confidence_reason", "") or "").strip()

    all_urls = {state.url for state in result.states.values()}
    tested_urls: set[str] = set()
    for action_result in result.results:
        source = result.states.get(action_result.source_state_id)
        target = result.states.get(action_result.target_state_id)
        if source:
            tested_urls.add(source.url)
        if target:
            tested_urls.add(target.url)

    executed_ids = {action_result.action_id for action_result in result.results}
    total_discovered_actions = len(result.actions)
    confidence_samples = [
        _result_stability_score(action_result)
        for action_result in result.results
        if _result_stability_score(action_result) > 0
        or _result_stability_note(action_result)
    ]
    avg_confidence = sum(confidence_samples) / max(len(confidence_samples), 1)
    low_confidence_count = sum(
        1 for score in confidence_samples if score < low_confidence_threshold
    )

    page_coverage_pct = round(len(tested_urls) / max(len(all_urls), 1) * 100)
    action_coverage_pct = round(
        len(executed_ids) / max(total_discovered_actions, 1) * 100
    )
    inventory = (
        result.element_inventory if isinstance(result.element_inventory, dict) else {}
    )
    interactive_elements = int(inventory.get("interactive_elements", 0))
    non_interactive_elements = int(inventory.get("non_interactive_elements", 0))
    total_catalog_elements = int(inventory.get("total_elements", 0))
    interactive_mix_pct = round(
        interactive_elements / max(total_catalog_elements, 1) * 100
    )

    return {
        "duration_seconds": result.duration_seconds,
        "total_states": result.stats.get("total_states", len(result.states)),
        "total_actions_executed": result.stats.get(
            "total_actions_executed",
            len(result.results),
        ),
        "total_unique_actions": result.stats.get(
            "total_unique_actions",
            len(result.actions),
        ),
        "page_coverage_pct": page_coverage_pct,
        "action_coverage_pct": action_coverage_pct,
        "confidence_sample_count": len(confidence_samples),
        "low_confidence_transitions": low_confidence_count,
        "avg_transition_confidence": round(avg_confidence, 3),
        "coverage_target_met": page_coverage_pct >= 80,
        "interactive_elements": interactive_elements,
        "non_interactive_elements": non_interactive_elements,
        "total_catalog_elements": total_catalog_elements,
        "interactive_mix_pct": interactive_mix_pct,
    }


def _evaluate_benchmark_gates(
    *,
    metrics: dict[str, int | float | bool],
    require_coverage_target: bool,
    max_low_confidence: int | None,
    low_confidence_threshold: float,
) -> list[str]:
    """Evaluate optional benchmark gates and return failures."""
    failures: list[str] = []
    if require_coverage_target and not bool(metrics["coverage_target_met"]):
        failures.append("coverage target check failed (required >= 80% page coverage)")

    if max_low_confidence is not None:
        confidence_sample_count = int(metrics["confidence_sample_count"])
        if confidence_sample_count == 0:
            failures.append(
                "low-confidence gate requested but artifact has no confidence samples",
            )
        elif int(metrics["low_confidence_transitions"]) > max_low_confidence:
            failures.append(
                "low-confidence transition count exceeds configured limit "
                f"({metrics['low_confidence_transitions']} > {max_low_confidence}, "
                f"threshold < {low_confidence_threshold:.2f})",
            )

    return failures


@main.command()
@click.argument("json_path", type=click.Path(exists=True))
@click.option("--db-path", default=DEFAULT_DB_PATH, help="SQLite database path.")
@click.option(
    "--low-confidence-threshold",
    default=DEFAULT_LOW_CONFIDENCE_THRESHOLD,
    show_default=True,
    help="Threshold for counting low-confidence transitions.",
)
@click.option(
    "--require-coverage-target/--no-require-coverage-target",
    default=False,
    help="Fail the command when the >=80% page-coverage target is not met.",
)
@click.option(
    "--max-low-confidence",
    type=int,
    default=None,
    help="Fail when low-confidence transitions exceed this count.",
)
def benchmark(
    json_path: str,
    db_path: str,
    low_confidence_threshold: float,
    require_coverage_target: bool,
    max_low_confidence: int | None,
) -> None:
    """Summarize benchmark metrics from a result artifact."""
    data = json.loads(Path(json_path).read_text())
    result = ExplorationResult.model_validate(data)
    metrics = _compute_benchmark_metrics(
        result,
        low_confidence_threshold=low_confidence_threshold,
    )

    table = Table(title="V1 Benchmark Snapshot", border_style="cyan")
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", justify="right")
    table.add_row("Result file", json_path)
    table.add_row("Duration (seconds)", f"{metrics['duration_seconds']:.2f}")
    table.add_row("States discovered", str(metrics["total_states"]))
    table.add_row("Actions executed", str(metrics["total_actions_executed"]))
    table.add_row("Unique actions discovered", str(metrics["total_unique_actions"]))
    table.add_row("Page coverage %", f"{metrics['page_coverage_pct']}%")
    table.add_row("Action coverage %", f"{metrics['action_coverage_pct']}%")
    if metrics["total_catalog_elements"]:
        table.add_row("Interactive elements", str(metrics["interactive_elements"]))
        table.add_row(
            "Content elements",
            str(metrics["non_interactive_elements"]),
        )
        table.add_row("Interactive mix %", f"{metrics['interactive_mix_pct']}%")
    if metrics["confidence_sample_count"]:
        table.add_row(
            "Avg transition confidence",
            f"{metrics['avg_transition_confidence']:.3f}",
        )
        table.add_row(
            f"Low-confidence transitions (< {low_confidence_threshold:.2f})",
            str(metrics["low_confidence_transitions"]),
        )
    else:
        table.add_row("Avg transition confidence", "n/a (legacy artifact)")
        table.add_row(
            f"Low-confidence transitions (< {low_confidence_threshold:.2f})",
            "n/a (legacy artifact)",
        )
    table.add_row(
        "Coverage target (>=80%)",
        "PASS" if metrics["coverage_target_met"] else "FAIL",
    )

    start_url = result.config.get("start_url", "")
    if start_url and Path(db_path).exists():
        db = FlowscoutDB(db_path)
        try:
            flaky_count = len(db.get_flaky_actions(start_url))
        finally:
            db.close()
        table.add_row("Flaky actions (history)", str(flaky_count))
    elif start_url:
        table.add_row("Flaky actions (history)", "n/a (db missing)")

    console.print(table)

    failures = _evaluate_benchmark_gates(
        metrics=metrics,
        require_coverage_target=require_coverage_target,
        max_low_confidence=max_low_confidence,
        low_confidence_threshold=low_confidence_threshold,
    )
    if failures:
        lines = "\n".join(f"- {line}" for line in failures)
        raise click.ClickException(f"Benchmark gates failed:\n{lines}")

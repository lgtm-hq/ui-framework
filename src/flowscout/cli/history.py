"""History command — show exploration history from database."""

from __future__ import annotations

import click
from rich.table import Table

from flowscout.cli.app import DEFAULT_DB_PATH, console, main
from flowscout.storage.db import FlowscoutDB


@main.command()
@click.option("--url", "-u", default=None, help="Filter by start URL.")
@click.option("--limit", "-n", default=20, help="Maximum runs to show.")
@click.option("--db-path", default=DEFAULT_DB_PATH, help="SQLite database path.")
def history(url: str | None, limit: int, db_path: str) -> None:
    """Show exploration history from the database."""
    db = FlowscoutDB(db_path)
    try:
        runs = db.list_runs(start_url=url, limit=limit)
        if not runs:
            console.print("  [dim]No runs found[/dim]")
            return

        table = Table(title="Exploration History", border_style="cyan")
        table.add_column("Run ID", style="bold cyan")
        table.add_column("URL", max_width=50)
        table.add_column("Started", style="dim")
        table.add_column("Duration", justify="right")
        table.add_column("States", justify="right")
        table.add_column("Actions", justify="right")
        table.add_column("Flows", justify="right")

        for run in runs:
            table.add_row(
                run["run_id"],
                run["start_url"][:50],
                run["started_at"][:19],
                f"{run['duration_seconds']:.1f}s",
                str(run["total_states"]),
                str(run["total_actions"]),
                str(run["total_flows"]),
            )

        console.print(table)
    finally:
        db.close()

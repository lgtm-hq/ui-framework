"""Reliability command — show action reliability across runs."""

from __future__ import annotations

import click
from rich.table import Table

from flowscout.cli.app import DEFAULT_DB_PATH, console, main
from flowscout.storage.db import FlowscoutDB


@main.command()
@click.option("--url", "-u", required=True, help="Start URL to analyze.")
@click.option("--db-path", default=DEFAULT_DB_PATH, help="SQLite database path.")
def reliability(url: str, db_path: str) -> None:
    """Show action reliability across runs."""
    db = FlowscoutDB(db_path)
    try:
        actions = db.get_action_reliability(start_url=url)
        if not actions:
            console.print("  [dim]No data found[/dim]")
            return

        table = Table(title=f"Action Reliability — {url}", border_style="cyan")
        table.add_column("Action", max_width=50)
        table.add_column("Attempts", justify="right")
        table.add_column("Nav", justify="right", style="green")
        table.add_column("DOM", justify="right", style="yellow")
        table.add_column("Errors", justify="right", style="red")
        table.add_column("No Change", justify="right", style="dim")

        for a in actions:
            table.add_row(
                a["label"][:50],
                str(a["total_attempts"]),
                str(a["navigations"]),
                str(a["dom_changes"]),
                str(a["errors"]),
                str(a["no_changes"]),
            )

        console.print(table)

        # Flaky actions
        flaky = db.get_flaky_actions(url)
        if flaky:
            console.print()
            flaky_table = Table(title="Flaky Actions", border_style="yellow")
            flaky_table.add_column("Action", max_width=50)
            flaky_table.add_column("Runs Seen", justify="right")
            flaky_table.add_column("Outcomes")

            for f in flaky:
                flaky_table.add_row(
                    f["label"][:50],
                    str(f["runs_seen"]),
                    f["outcomes_seen"],
                )

            console.print(flaky_table)
    finally:
        db.close()

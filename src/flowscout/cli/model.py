"""Model command — build SiteModel artifacts from exploration results."""

from __future__ import annotations

import json
from pathlib import Path

import click

from flowscout.analysis.graph import ExplorationResult
from flowscout.cli.app import console, main
from flowscout.modeling.site_model import SiteModel
from flowscout.reporting.terminal import TerminalReporter


@main.command()  # type: ignore[untyped-decorator]  # Click decorators are untyped
@click.argument("result_path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output SiteModel JSON path.",
)
def model(result_path: str, output: str | None) -> None:
    """Build a site model JSON artifact from an exploration result JSON."""
    data = json.loads(Path(result_path).read_text())
    result = ExplorationResult.model_validate(data)
    site_model = SiteModel.from_exploration_result(result=result)

    model_output = output or result_path.replace(".json", "_model.json")
    Path(model_output).write_text(site_model.model_dump_json(indent=2))
    console.print(f"  [green]Site model generated:[/green] {model_output}")

    terminal = TerminalReporter()
    terminal.print_site_model_summary(site_model)

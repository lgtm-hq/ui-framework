"""Serve command — local HTTP server for HTML reports."""

from __future__ import annotations

import click

from flowscout.cli.app import main


@main.command()
@click.argument("report_path", type=click.Path(exists=True))
@click.option(
    "--port", "-p", default=8765, help="Server port (auto-increments if taken)."
)
@click.option("--no-open", is_flag=True, help="Don't auto-open browser.")
def serve(report_path: str, port: int, no_open: bool) -> None:
    """Serve an HTML report via local HTTP server."""
    from flowscout.serve.server import run_server

    run_server(report_path, port=port, open_browser=not no_open)

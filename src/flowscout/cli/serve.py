"""Serve command — local HTTP server for HTML reports."""

from __future__ import annotations

import click

from flowscout.cli.app import main


@main.command()
@click.argument("report_path", type=click.Path(exists=True))
@click.option(
    "--port", "-p", default=8765, help="Server port (auto-increments if taken)."
)
@click.option(
    "--host",
    default="127.0.0.1",
    show_default=True,
    help="Host interface to bind (use 0.0.0.0 for LAN access).",
)
@click.option("--no-open", is_flag=True, help="Don't auto-open browser.")
@click.option(
    "--allow-cors",
    is_flag=True,
    help="Allow cross-origin reads of report responses.",
)
def serve(
    report_path: str,
    port: int,
    host: str,
    no_open: bool,
    allow_cors: bool,
) -> None:
    """Serve an HTML report via local HTTP server."""
    from flowscout.serve.server import run_server

    run_server(
        report_path,
        port=port,
        host=host,
        open_browser=not no_open,
        allow_cors=allow_cors,
    )

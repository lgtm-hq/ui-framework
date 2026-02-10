"""Serve command — open HTML report in browser."""

from __future__ import annotations

import os
import webbrowser

import click

from flowscout.cli.app import console, main


@main.command()
@click.argument("report_path", type=click.Path(exists=True))
def serve(report_path: str) -> None:
    """Open an HTML report in the browser."""
    abs_path = os.path.abspath(report_path)
    console.print(f"  Opening {abs_path}")
    webbrowser.open(f"file://{abs_path}")

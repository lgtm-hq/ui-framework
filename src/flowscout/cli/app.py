"""Click group definition and shared CLI state."""

from __future__ import annotations

import click
from rich.console import Console

from flowscout import __version__

console = Console()

DEFAULT_DB_PATH = ".flowscout/history.db"
DEFAULT_CRAWL_CONFIG_PATH = ".crawl-config"
DEFAULT_AUTH_CONFIG_PATH = ".flowscout-auth.toml"
DEFAULT_LOW_CONFIDENCE_THRESHOLD = 0.6


@click.group()
@click.version_option(version=__version__, prog_name="flowscout")
def main() -> None:
    """Flowscout — LLM-free automated web path exploration."""

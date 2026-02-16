"""Vite build integration for the SolidJS dashboard.

Provides ``get_dashboard_shell()`` which returns the built HTML shell
with all JS/CSS inlined. The report generator replaces the data
placeholder with actual report JSON.
"""

from __future__ import annotations

import logging
import shutil
import subprocess  # nosec B404 - required for running bun CLI, no user input involved
from pathlib import Path

logger = logging.getLogger(__name__)

_DASHBOARD_DIR = Path(__file__).parent / "dashboard"
_DIST_HTML = _DASHBOARD_DIR / "dist" / "index.html"
_PLACEHOLDER = '"__REPORT_DATA_PLACEHOLDER__"'


def _resolve_bun() -> str:
    """Resolve the full path to the ``bun`` executable.

    Raises:
        RuntimeError: If bun is not installed.
    """
    bun = shutil.which("bun")
    if bun is None:
        msg = "bun is not installed — required for dashboard build"
        raise RuntimeError(msg)
    return bun


def _run_bun(*args: str) -> None:
    """Run a bun command with the resolved full path."""
    bun = _resolve_bun()
    subprocess.run(  # nosec B603 - hardcoded command with no user input
        [bun, *args],
        cwd=str(_DASHBOARD_DIR),
        check=True,
        capture_output=True,
    )


def build_dashboard() -> Path:
    """Run Vite build and return path to the built index.html.

    Raises:
        RuntimeError: If the build fails.
    """
    if not (_DASHBOARD_DIR / "node_modules").exists():
        logger.info("Installing dashboard dependencies...")
        _run_bun("install")

    logger.info("Building dashboard SPA...")
    _run_bun("run", "build")

    if not _DIST_HTML.exists():
        msg = f"Dashboard build did not produce {_DIST_HTML}"
        raise RuntimeError(msg)

    return _DIST_HTML


def get_dashboard_shell() -> str:
    """Return the built dashboard HTML shell.

    Uses pre-built output if available, otherwise builds on demand.
    """
    if _DIST_HTML.exists():
        return _DIST_HTML.read_text()

    build_dashboard()
    return _DIST_HTML.read_text()


def inject_report_data(*, html_shell: str, report_json: str) -> str:
    """Replace the data placeholder in the dashboard shell with actual data."""
    return html_shell.replace(_PLACEHOLDER, report_json)

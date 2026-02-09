"""Tests for CLI output workspace path building."""

from datetime import datetime, timezone
from pathlib import Path

from flowscout.cli import _build_output_dirs
from flowscout.core.state import ExplorerConfig


def test_build_output_dirs_uses_domain_and_environment(tmp_path: Path) -> None:
    config = ExplorerConfig(
        start_url="https://example.com",
        output_dir=str(tmp_path),
        environment="staging",
    )
    run_dir, workspace = _build_output_dirs(
        config,
        datetime(2026, 2, 9, 12, 0, 0, tzinfo=timezone.utc),
        smart_workspace=True,
    )

    assert workspace is not None
    assert "example.com/staging" in str(workspace)
    assert str(run_dir).startswith(str(workspace))
    assert "/runs/" in str(run_dir)


def test_build_output_dirs_sanitizes_environment_name(tmp_path: Path) -> None:
    config = ExplorerConfig(
        start_url="https://example.com",
        output_dir=str(tmp_path),
        environment="prod/us-east-1",
    )
    run_dir, workspace = _build_output_dirs(
        config,
        datetime(2026, 2, 9, 12, 0, 0, tzinfo=timezone.utc),
        smart_workspace=True,
    )

    assert workspace is not None
    assert "prod_us-east-1" in str(workspace)
    assert run_dir.exists()

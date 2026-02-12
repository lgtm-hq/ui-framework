"""Tests for ``flowscout explore`` smart-mode CLI behavior."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from click.testing import CliRunner

from flowscout.cli import main
from flowscout.core.state import ExplorerConfig
import flowscout.cli.explore as explore_cli


def _run_explore(
    *,
    runner: CliRunner,
    tmp_path: Path,
    monkeypatch: Any,
    extra_args: list[str],
) -> ExplorerConfig:
    """Invoke ``flowscout explore`` and return the resolved config passed downstream."""
    captured: dict[str, ExplorerConfig] = {}

    async def _fake_run_exploration(
        config: ExplorerConfig,
        **_: Any,
    ) -> None:
        captured["config"] = config

    monkeypatch.setattr(explore_cli, "_run_exploration", _fake_run_exploration)

    config_file = tmp_path / ".crawl-config"
    auth_file = tmp_path / ".flowscout-auth.toml"

    result = runner.invoke(
        main,
        [
            "explore",
            "https://example.com",
            "--no-db",
            "--config-file",
            str(config_file),
            "--auth-config-file",
            str(auth_file),
            *extra_args,
        ],
    )

    assert result.exit_code == 0, result.output
    assert "config" in captured
    return captured["config"]


def test_explore_defaults_to_smart_mode_enabled(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Smart mode should be enabled unless explicitly disabled."""
    config = _run_explore(
        runner=CliRunner(),
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        extra_args=[],
    )

    assert config.smart_mode is True


def test_explore_no_smart_disables_smart_mode(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """``--no-smart`` should disable smart mode."""
    config = _run_explore(
        runner=CliRunner(),
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        extra_args=["--no-smart"],
    )

    assert config.smart_mode is False


def test_explore_reads_smart_mode_from_config_when_flag_omitted(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Config file value should apply when CLI flag is omitted."""
    config_file = tmp_path / ".crawl-config"
    config_file.write_text("smart = false\n")

    config = _run_explore(
        runner=CliRunner(),
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        extra_args=[],
    )

    assert config.smart_mode is False


def test_explore_cli_flag_overrides_config_value(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Explicit ``--smart`` should override ``smart = false`` in config."""
    config_file = tmp_path / ".crawl-config"
    config_file.write_text("smart = false\n")

    config = _run_explore(
        runner=CliRunner(),
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        extra_args=["--smart"],
    )

    assert config.smart_mode is True


def test_explore_help_lists_no_smart_option() -> None:
    """CLI help should document the opt-out flag."""
    result = CliRunner().invoke(main, ["explore", "--help"])

    assert result.exit_code == 0, result.output
    assert "--smart / --no-smart" in result.output

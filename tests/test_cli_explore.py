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
) -> tuple[ExplorerConfig, dict[str, Any]]:
    """Invoke ``flowscout explore`` and return the resolved config passed downstream."""
    captured: dict[str, ExplorerConfig] = {}
    captured_kwargs: dict[str, Any] = {}

    async def _fake_run_exploration(
        config: ExplorerConfig,
        **kwargs: Any,
    ) -> None:
        captured["config"] = config
        captured_kwargs.update(kwargs)

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
    return captured["config"], captured_kwargs


def test_explore_defaults_to_smart_mode_enabled(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Smart mode should be enabled unless explicitly disabled."""
    config, _ = _run_explore(
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
    config, _ = _run_explore(
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

    config, _ = _run_explore(
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

    config, _ = _run_explore(
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


def test_explore_help_lists_legacy_option() -> None:
    """CLI help should document the legacy flat test option."""
    result = CliRunner().invoke(main, ["explore", "--help"])

    assert result.exit_code == 0, result.output
    assert "--legacy" in result.output


def test_explore_legacy_flag_forwards_to_runner(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """``--legacy`` should propagate to runtime orchestration."""
    _, kwargs = _run_explore(
        runner=CliRunner(),
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        extra_args=["--generate-tests", "--legacy"],
    )

    assert kwargs["generate_legacy"] is True
    assert kwargs["generate_tests"] is True

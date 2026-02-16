"""Tests for the serve CLI command."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from click.testing import CliRunner

from flowscout.cli import main


def test_serve_passes_host_and_cors_options(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    """Serve command should forward new host/CORS options to run_server."""
    report = tmp_path / "report.html"
    report.write_text("<html><body>ok</body></html>")

    captured: dict[str, Any] = {}

    def _fake_run_server(
        report_path: str,
        *,
        port: int,
        host: str,
        open_browser: bool,
        allow_cors: bool,
    ) -> None:
        captured["report_path"] = report_path
        captured["port"] = port
        captured["host"] = host
        captured["open_browser"] = open_browser
        captured["allow_cors"] = allow_cors

    monkeypatch.setattr("flowscout.serve.server.run_server", _fake_run_server)

    result = CliRunner().invoke(
        main,
        [
            "serve",
            str(report),
            "--port",
            "9100",
            "--host",
            "localhost",
            "--allow-cors",
            "--no-open",
        ],
    )

    assert result.exit_code == 0, result.output
    assert captured["report_path"] == str(report)
    assert captured["port"] == 9100
    assert captured["host"] == "localhost"
    assert captured["open_browser"] is False
    assert captured["allow_cors"] is True

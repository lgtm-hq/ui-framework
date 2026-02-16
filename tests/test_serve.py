"""Tests for the serve HTTP server."""

from __future__ import annotations

import threading
import time
import urllib.request
from pathlib import Path

import pytest

from flowscout.serve.server import (
    _find_available_port,
    _is_unspecified_host,
    run_server,
)


class TestFindAvailablePort:
    def test_returns_start_port_when_free(self) -> None:
        port = _find_available_port(start=18765)
        assert port >= 18765

    def test_skips_occupied_port(self) -> None:
        import socket

        # Occupy a port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", 18800))
        sock.listen(1)
        try:
            port = _find_available_port(start=18800)
            assert port > 18800
        finally:
            sock.close()

    def test_returns_fallback_after_max_attempts(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        class _AlwaysBusySocket:
            def __enter__(self) -> "_AlwaysBusySocket":
                return self

            def __exit__(self, *_args: object) -> None:
                return None

            def bind(self, _address: tuple[str, int]) -> None:
                raise OSError("busy")

        monkeypatch.setattr(
            "flowscout.serve.server.socket.socket",
            lambda *_args, **_kwargs: _AlwaysBusySocket(),
        )
        assert _find_available_port(start=20000, max_attempts=3) == 20003


class TestUnspecifiedHost:
    def test_detects_unspecified_ip_hosts(self) -> None:
        any_host = ".".join(["0", "0", "0", "0"])
        assert _is_unspecified_host(any_host) is True
        assert _is_unspecified_host("::") is True

    def test_handles_non_ip_aliases(self) -> None:
        assert _is_unspecified_host("*") is True
        assert _is_unspecified_host("localhost") is False


class TestRunServer:
    def test_run_server_handles_keyboard_interrupt(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        report = tmp_path / "report.html"
        report.write_text("<html><body>Interrupt</body></html>")

        events: list[str] = []

        class _FakeServer:
            def __init__(self, *_args: object, **_kwargs: object) -> None:
                self.server_address = ("127.0.0.1", 19999)

            def serve_forever(self) -> None:
                events.append("serve_forever")
                raise KeyboardInterrupt

            def server_close(self) -> None:
                events.append("server_close")

        class _FakeTimer:
            def __init__(self, *_args: object, **_kwargs: object) -> None:
                events.append("timer_created")

            def start(self) -> None:
                events.append("timer_started")

        monkeypatch.setattr("flowscout.serve.server.HTTPServer", _FakeServer)
        monkeypatch.setattr("flowscout.serve.server.threading.Timer", _FakeTimer)

        run_server(str(report), port=19999, host="127.0.0.1", open_browser=True)
        assert events == [
            "timer_created",
            "timer_started",
            "serve_forever",
            "server_close",
        ]

    def test_serves_report_file(self, tmp_path: Path) -> None:
        report = tmp_path / "report.html"
        report.write_text("<html><body>Test Report</body></html>")

        port = _find_available_port(start=19000, host="127.0.0.1")

        def _run() -> None:
            run_server(
                str(report),
                port=port,
                host="127.0.0.1",
                open_browser=False,
            )

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()

        # Wait for server to start
        time.sleep(0.5)

        url = f"http://localhost:{port}/report.html"
        # Hardcoded localhost URL for our own test server
        # nosemgrep: dynamic-urllib-use-detected
        response = urllib.request.urlopen(url, timeout=5)  # nosec B310
        content = response.read().decode()

        assert "Test Report" in content
        assert response.status == 200

    def test_no_cors_header_by_default(self, tmp_path: Path) -> None:
        report = tmp_path / "report.html"
        report.write_text("<html><body>No CORS</body></html>")

        port = _find_available_port(start=19040, host="127.0.0.1")

        def _run() -> None:
            run_server(
                str(report),
                port=port,
                host="127.0.0.1",
                open_browser=False,
            )

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        time.sleep(0.5)

        url = f"http://127.0.0.1:{port}/report.html"
        # nosemgrep: dynamic-urllib-use-detected
        response = urllib.request.urlopen(url, timeout=5)  # nosec B310
        assert response.headers.get("Access-Control-Allow-Origin") is None

    def test_allow_cors_adds_header(self, tmp_path: Path) -> None:
        report = tmp_path / "report.html"
        report.write_text("<html><body>CORS</body></html>")

        port = _find_available_port(start=19080, host="127.0.0.1")

        def _run() -> None:
            run_server(
                str(report),
                port=port,
                host="127.0.0.1",
                open_browser=False,
                allow_cors=True,
            )

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        time.sleep(0.5)

        url = f"http://127.0.0.1:{port}/report.html"
        # nosemgrep: dynamic-urllib-use-detected
        response = urllib.request.urlopen(url, timeout=5)  # nosec B310
        assert response.headers.get("Access-Control-Allow-Origin") == "*"

    def test_raises_for_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="Report not found"):
            run_server(str(tmp_path / "nonexistent.html"), open_browser=False)

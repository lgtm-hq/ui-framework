"""Tests for the serve HTTP server."""

from __future__ import annotations

import threading
import time
import urllib.request
from pathlib import Path
from unittest.mock import patch

import pytest

from flowscout.serve.server import _find_available_port, run_server


class TestFindAvailablePort:

    def test_returns_start_port_when_free(self):
        port = _find_available_port(start=18765)
        assert port >= 18765

    def test_skips_occupied_port(self):
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


class TestRunServer:

    def test_serves_report_file(self, tmp_path: Path):
        report = tmp_path / "report.html"
        report.write_text("<html><body>Test Report</body></html>")

        port = _find_available_port(start=19000)

        def _run():
            run_server(str(report), port=port, open_browser=False)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()

        # Wait for server to start
        time.sleep(0.5)

        url = f"http://localhost:{port}/report.html"
        response = urllib.request.urlopen(url, timeout=5)
        content = response.read().decode()

        assert "Test Report" in content
        assert response.status == 200

    def test_raises_for_missing_file(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError, match="Report not found"):
            run_server(str(tmp_path / "nonexistent.html"), open_browser=False)

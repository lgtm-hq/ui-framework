"""Local HTTP server for serving HTML reports."""

from __future__ import annotations

import socket
import threading
import webbrowser
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class _ReportHandler(SimpleHTTPRequestHandler):
    """Handler that serves files from a specific directory with CORS headers."""

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default request logging."""


def _find_available_port(start: int = 8765, max_attempts: int = 20) -> int:
    """Find an available port starting from ``start``."""
    for offset in range(max_attempts):
        port = start + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("localhost", port))
                return port
            except OSError:
                continue
    return start + max_attempts


def run_server(
    report_path: str,
    *,
    port: int = 8765,
    open_browser: bool = True,
) -> None:
    """Start HTTP server serving the report directory.

    Args:
        report_path: Path to the HTML report file.
        port: Preferred port (auto-increments if taken).
        open_browser: Open the report in the default browser.
    """
    report = Path(report_path).resolve()
    if not report.exists():
        raise FileNotFoundError(f"Report not found: {report}")

    serve_dir = str(report.parent)
    filename = report.name
    actual_port = _find_available_port(port)

    handler = partial(_ReportHandler, directory=serve_dir)
    server = HTTPServer(("localhost", actual_port), handler)

    url = f"http://localhost:{actual_port}/{filename}"
    print(f"  Serving report at {url}")
    print("  Press Ctrl+C to stop")

    if open_browser:
        threading.Timer(0.5, webbrowser.open, args=[url]).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped")
    finally:
        server.server_close()

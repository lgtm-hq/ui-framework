"""Local HTTP server for serving HTML reports."""

from __future__ import annotations

import ipaddress
import socket
import threading
import webbrowser
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class _ReportHandler(SimpleHTTPRequestHandler):
    """Handler that serves files from a specific directory with CORS headers."""

    allow_cors = False

    def end_headers(self) -> None:
        if self.allow_cors:
            self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default request logging."""


def _is_unspecified_host(host: str) -> bool:
    """Return True for wildcard bind addresses (IPv4/IPv6)."""
    try:
        return ipaddress.ip_address(host).is_unspecified
    except ValueError:
        return host.strip().lower() in {"*", "all"}


def _find_available_port(
    start: int = 8765,
    max_attempts: int = 20,
    *,
    host: str = "127.0.0.1",
) -> int:
    """Find an available port starting from ``start``."""
    for offset in range(max_attempts):
        port = start + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return port
            except OSError:
                continue
    return start + max_attempts


def run_server(
    report_path: str,
    *,
    port: int = 8765,
    host: str = "127.0.0.1",
    open_browser: bool = True,
    allow_cors: bool = False,
) -> None:
    """Start HTTP server serving the report directory.

    Args:
        report_path: Path to the HTML report file.
        port: Preferred port (auto-increments if taken).
        host: Host interface to bind.
        open_browser: Open the report in the default browser.
        allow_cors: If True, include wildcard CORS response header.
    """
    report = Path(report_path).resolve()
    if not report.exists():
        raise FileNotFoundError(f"Report not found: {report}")

    serve_dir = str(report.parent)
    filename = report.name
    actual_port = _find_available_port(port, host=host)
    _ReportHandler.allow_cors = allow_cors

    handler = partial(_ReportHandler, directory=serve_dir)
    server = HTTPServer((host, actual_port), handler)

    display_host = "127.0.0.1" if _is_unspecified_host(host) else host
    url = f"http://{display_host}:{actual_port}/{filename}"
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

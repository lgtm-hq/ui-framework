"""Shared URL normalization utilities.

Consolidates URL parsing, domain extraction, and filesystem-safe name
generation that was previously duplicated across cli.py, navigator.py,
codegen/playwright_tests.py, and analysis modules.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse


def extract_hostname(url: str) -> str:
    """Return the lowercase hostname from a URL, or empty string."""
    return (urlparse(url).hostname or "").lower()


def extract_netloc(url: str) -> str:
    """Return the netloc (host:port) from a URL."""
    return urlparse(url).netloc or ""


def extract_path(url: str) -> str:
    """Return the URL path, with trailing slash stripped."""
    return urlparse(url).path.rstrip("/") or "/"


def extract_path_tail(url: str) -> str:
    """Return the last path segment (e.g. '/items/42' -> '42')."""
    path = extract_path(url)
    return path.split("/")[-1] if path and path != "/" else ""


def extract_url_path_pattern(url: str) -> str:
    """Extract a regex-escaped path pattern from a full URL.

    Strips protocol and domain, keeps path. Used by codegen to build
    URL-matching assertions.
    """
    parsed = urlparse(url)
    if parsed.path and parsed.path != "/":
        return re.escape(parsed.path)
    return re.escape(url)


def is_same_origin(url: str, base_url: str) -> bool:
    """Check whether *url* shares the same origin as *base_url*."""
    if not base_url:
        return True
    return urlparse(url).netloc == urlparse(base_url).netloc


def sanitize_for_filesystem(name: str) -> str:
    """Replace characters unsafe for filesystem paths with underscores."""
    return re.sub(r"[^\w.\-]", "_", name)

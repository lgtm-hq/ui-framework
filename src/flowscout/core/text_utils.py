"""Shared text normalization utilities.

Consolidates regex patterns and sanitization functions that were
duplicated across discovery/elements.py and reporting/html.py.
"""

from __future__ import annotations

import re

# ── Compiled patterns (shared, not duplicated) ───────────────────────

# Matches CSS declarations like: .className:pseudo { ... }
CSS_BLOCK_RE = re.compile(r"\.[a-zA-Z0-9_-]+(?::[\w-]+)?\s*\{[^}]*\}")

# Matches bare brace groups: { ... }
BRACE_RE = re.compile(r"\{[^}]*\}")

# Matches whitespace runs
WHITESPACE_RE = re.compile(r"\s+")


def normalize_whitespace(text: str) -> str:
    """Collapse whitespace runs into single spaces and strip."""
    return WHITESPACE_RE.sub(" ", text).strip()


def strip_css_blocks(text: str) -> str:
    """Remove CSS pseudo-element declarations and brace groups from text."""
    cleaned = CSS_BLOCK_RE.sub("", text)
    cleaned = BRACE_RE.sub("", cleaned)
    return normalize_whitespace(cleaned)

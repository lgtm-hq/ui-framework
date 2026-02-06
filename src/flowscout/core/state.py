"""Page state representation and fingerprinting."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum, auto
from hashlib import sha256
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from pydantic import BaseModel, Field


class ExplorationStrategy(StrEnum):
    BFS = auto()
    DFS = auto()
    PRIORITY = auto()


class ExplorerConfig(BaseModel):
    """Configuration for an exploration run."""

    start_url: str
    max_depth: int = Field(default=3, ge=1)
    max_states: int = Field(default=50, ge=1)
    max_actions_per_state: int = Field(default=20, ge=1)
    headless: bool = True
    timeout_ms: int = Field(default=10000, ge=1000)
    output_dir: str = "./reports"
    take_screenshots: bool = False
    strategy: ExplorationStrategy = ExplorationStrategy.PRIORITY
    verbose: bool = False


class PageState(BaseModel):
    """A uniquely fingerprinted page state."""

    state_id: str = Field(description="First 12 chars of fingerprint hash")
    url: str
    title: str
    fingerprint: str = Field(description="Full SHA-256 of the state signature")
    depth: int = Field(ge=0)
    dom_structure_hash: str
    visible_text_hash: str
    form_state_hash: str
    signals: list[str] = Field(default_factory=list)
    screenshot_path: str | None = None
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


class FingerprintConfig(BaseModel):
    """Controls which signals contribute to state fingerprinting."""

    include_url: bool = True
    include_dom_structure: bool = True
    include_visible_text: bool = True
    include_form_state: bool = True
    ignore_url_params: list[str] = Field(default_factory=list)
    ignore_selectors: list[str] = Field(default_factory=list)


def normalize_url(url: str, *, ignore_params: list[str] | None = None) -> str:
    """Normalize a URL for consistent fingerprinting."""
    parsed = urlparse(url)
    # Strip trailing slash from path
    path = parsed.path.rstrip("/") or "/"
    # Sort query params, remove ignored ones
    params = parse_qs(parsed.query, keep_blank_values=True)
    if ignore_params:
        for p in ignore_params:
            params.pop(p, None)
    sorted_query = urlencode(sorted(params.items()), doseq=True)
    # Strip fragment
    return urlunparse((parsed.scheme, parsed.netloc, path, "", sorted_query, ""))


def build_fingerprint(
    url: str,
    title: str,
    dom_structure_hash: str,
    visible_text_hash: str,
    form_state_hash: str,
    *,
    config: FingerprintConfig | None = None,
) -> str:
    """Build a SHA-256 state fingerprint from multiple signals.

    Combines normalized URL, DOM structure skeleton hash, visible text hash
    (headings, active nav, selected tabs), and form state hash (selected
    options, checked boxes, input values).
    """
    cfg = config or FingerprintConfig()
    parts: list[str] = []

    if cfg.include_url:
        parts.append(normalize_url(url, ignore_params=cfg.ignore_url_params))
    parts.append(title)
    if cfg.include_dom_structure:
        parts.append(dom_structure_hash)
    if cfg.include_visible_text:
        parts.append(visible_text_hash)
    if cfg.include_form_state:
        parts.append(form_state_hash)

    payload = "|".join(parts)
    return sha256(payload.encode()).hexdigest()


def make_state_id(fingerprint: str) -> str:
    """Create a short state ID from a full fingerprint hash."""
    return fingerprint[:12]

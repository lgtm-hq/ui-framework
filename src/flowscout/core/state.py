"""Page state representation and fingerprinting."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum, auto
from fnmatch import fnmatch
from hashlib import sha256
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from pydantic import BaseModel, Field

from flowscout.core.policy import ActionPolicyConfig


class ExplorationStrategy(StrEnum):
    BFS = auto()
    DFS = auto()
    PRIORITY = auto()


class InputProfile(StrEnum):
    SAFE = auto()
    CONTEXTUAL = auto()
    NEGATIVE = auto()


class ExplorerConfig(BaseModel):
    """Configuration for an exploration run."""

    start_url: str
    max_depth: int = Field(default=3, ge=1)
    max_states: int = Field(default=50, ge=1)
    max_actions_per_state: int = Field(default=20, ge=1)
    headless: bool = True
    timeout_ms: int = Field(default=10000, ge=1000)
    action_timeout_ms: int = Field(default=5000, ge=500)
    stability_timeout_ms: int = Field(default=2000, ge=200)
    load_wait_timeout_ms: int = Field(default=3000, ge=500)
    output_dir: str = "./reports"
    take_screenshots: bool = False
    strategy: ExplorationStrategy = ExplorationStrategy.PRIORITY
    verbose: bool = False
    smart_mode: bool = False
    input_profile: InputProfile = InputProfile.SAFE
    action_policy: ActionPolicyConfig = Field(default_factory=ActionPolicyConfig)


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
    query_allowlist: list[str] = Field(
        default_factory=lambda: [
            "page",
            "sort",
            "filter",
            "category",
            "tab",
            "view",
            "q",
            "lang",
        ]
    )
    ignore_url_params: list[str] = Field(default_factory=list)
    ignore_url_param_patterns: list[str] = Field(
        default_factory=lambda: [
            "utm_*",
            "gclid",
            "fbclid",
            "*session*",
            "*token*",
            "ts",
            "_",
            "*cache*",
        ]
    )
    ignore_selectors: list[str] = Field(default_factory=list)


def normalize_url(
    url: str,
    *,
    allow_params: list[str] | None = None,
    ignore_params: list[str] | None = None,
    ignore_param_patterns: list[str] | None = None,
) -> str:
    """Normalize a URL for consistent fingerprinting."""
    parsed = urlparse(url)
    # Strip trailing slash from path
    path = parsed.path.rstrip("/") or "/"
    # Sort query params, remove ignored ones
    params = parse_qs(parsed.query, keep_blank_values=True)

    if allow_params:
        allowed_keys = {key.casefold() for key in allow_params}
        params = {
            key: value
            for key, value in params.items()
            if key.casefold() in allowed_keys
        }

    if ignore_params:
        ignored_keys = {key.casefold() for key in ignore_params}
        params = {
            key: value
            for key, value in params.items()
            if key.casefold() not in ignored_keys
        }

    if ignore_param_patterns:
        lowered_patterns = [pattern.casefold() for pattern in ignore_param_patterns]
        params = {
            key: value
            for key, value in params.items()
            if not any(fnmatch(key.casefold(), pattern) for pattern in lowered_patterns)
        }

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
        parts.append(
            normalize_url(
                url,
                allow_params=cfg.query_allowlist,
                ignore_params=cfg.ignore_url_params,
                ignore_param_patterns=cfg.ignore_url_param_patterns,
            )
        )
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

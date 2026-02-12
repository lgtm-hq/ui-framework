"""Page state representation and fingerprinting."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum, auto
from fnmatch import fnmatch
from hashlib import sha256
import re
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
    environment: str = "dev"
    take_screenshots: bool = True
    evidence_dir: str | None = None
    strategy: ExplorationStrategy = ExplorationStrategy.PRIORITY
    verbose: bool = False
    smart_mode: bool = True
    smart_stop_on_saturation: bool = True
    smart_min_features_before_stop: int = Field(default=3, ge=0)
    smart_min_archetypes_before_stop: int = Field(default=2, ge=0)
    smart_archetype_instance_limit: int = Field(default=3, ge=1)
    input_profile: InputProfile = InputProfile.SAFE
    auth_profile: str | None = None
    auth_required: bool = False
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
    route_key: str = ""
    view_key: str = ""
    context_key: str = ""
    primary_heading: str = ""
    context_markers: list[str] = Field(default_factory=list)
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


_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
_HEX_LONG_RE = re.compile(r"^[0-9a-f]{16,}$", re.IGNORECASE)
_ALNUM_TOKEN_RE = re.compile(r"^[a-z0-9_-]{16,}$", re.IGNORECASE)
_MIXED_ID_RE = re.compile(r"^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9._~-]{8,}$")


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
    sorted_query = _normalize_query_params(
        parsed.query,
        allow_params=allow_params,
        ignore_params=ignore_params,
        ignore_param_patterns=ignore_param_patterns,
    )
    # Strip fragment
    return urlunparse((parsed.scheme, parsed.netloc, path, "", sorted_query, ""))


def build_route_key(url: str, *, config: FingerprintConfig | None = None) -> str:
    """Build a normalized route key with dynamic path segment abstraction."""
    cfg = config or FingerprintConfig()
    parsed = urlparse(url)
    path = _normalize_route_path(parsed.path)
    sorted_query = _normalize_query_params(
        parsed.query,
        allow_params=cfg.query_allowlist,
        ignore_params=cfg.ignore_url_params,
        ignore_param_patterns=cfg.ignore_url_param_patterns,
    )
    return urlunparse((parsed.scheme, parsed.netloc, path, "", sorted_query, ""))


def build_view_key(
    *,
    route_key: str,
    dom_structure_hash: str,
    primary_heading: str,
) -> str:
    """Build a view-level identity key from route + structure + heading."""
    payload = "|".join(
        [
            route_key,
            dom_structure_hash,
            _normalize_text_value(primary_heading),
        ]
    )
    return sha256(payload.encode()).hexdigest()


def build_context_key(*, view_key: str, context_markers: list[str]) -> str:
    """Build context identity key from view key + context markers."""
    normalized_markers = sorted(
        {m for m in map(_normalize_text_value, context_markers) if m}
    )
    payload = "|".join([view_key, *normalized_markers])
    return sha256(payload.encode()).hexdigest()


def extract_primary_heading(*, signals: list[str], title: str) -> str:
    """Extract primary page heading for view-level identity."""
    for signal in signals:
        if signal.startswith("h1:"):
            return signal.removeprefix("h1:").strip()
    if title.strip():
        return title.strip()
    return "untitled"


def extract_context_markers(*, signals: list[str], form_state_hash: str) -> list[str]:
    """Extract context markers that represent interactive UI state."""
    prefixes = ("nav:", "tab:", "modal:", "step:", "h1:")
    markers = [s for s in signals if s.startswith(prefixes)]
    if form_state_hash:
        markers.append(f"form:{form_state_hash[:12]}")
    return sorted({m for m in map(_normalize_text_value, markers) if m})


def build_fingerprint(
    url: str,
    title: str,
    dom_structure_hash: str,
    visible_text_hash: str,
    form_state_hash: str,
    *,
    route_key: str | None = None,
    view_key: str | None = None,
    context_key: str | None = None,
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
        parts.append(route_key or build_route_key(url, config=cfg))
    if view_key:
        parts.append(view_key)
    else:
        parts.append(title)
        if cfg.include_dom_structure:
            parts.append(dom_structure_hash)
    if context_key:
        parts.append(context_key)
    else:
        if cfg.include_visible_text:
            parts.append(visible_text_hash)
        if cfg.include_form_state:
            parts.append(form_state_hash)

    payload = "|".join(parts)
    return sha256(payload.encode()).hexdigest()


def make_state_id(fingerprint: str) -> str:
    """Create a short state ID from a full fingerprint hash."""
    return fingerprint[:12]


def _normalize_query_params(
    query: str,
    *,
    allow_params: list[str] | None,
    ignore_params: list[str] | None,
    ignore_param_patterns: list[str] | None,
) -> str:
    """Normalize query parameters according to allow/ignore rules."""
    params = parse_qs(query, keep_blank_values=True)

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

    return urlencode(sorted(params.items()), doseq=True)


def _normalize_route_path(path: str) -> str:
    """Normalize path and collapse dynamic-looking segments into placeholders."""
    segments = [segment for segment in path.split("/") if segment]
    if not segments:
        return "/"

    normalized_segments: list[str] = []
    for segment in segments:
        if _looks_dynamic_segment(segment):
            normalized_segments.append("{id}")
        else:
            normalized_segments.append(segment)
    return "/" + "/".join(normalized_segments)


def _looks_dynamic_segment(segment: str) -> bool:
    """Heuristically detect path segments that represent entity identifiers."""
    value = segment.strip()
    if not value:
        return False
    lower = value.casefold()

    if lower.isdigit():
        return True
    if _UUID_RE.match(lower):
        return True
    if _HEX_LONG_RE.match(lower):
        return True
    if _ALNUM_TOKEN_RE.match(lower) and any(char.isdigit() for char in lower):
        return True
    if _MIXED_ID_RE.match(value):
        return True

    return False


def _normalize_text_value(value: str) -> str:
    """Normalize free text for stable key generation."""
    return " ".join(value.strip().split()).casefold()

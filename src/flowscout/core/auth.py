"""Authentication profile loading and secure runtime credential bootstrap."""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
import os
from pathlib import Path
import re
import tomllib
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, Field


class AuthConfigError(ValueError):
    """Raised when auth profile configuration is invalid or incomplete."""


class AuthProfile(BaseModel):
    """Auth profile definition loaded from TOML."""

    name: str
    domains: list[str] = Field(default_factory=list)
    environments: list[str] = Field(default_factory=list)
    login_url: str | None = None
    username_selector: str
    password_selector: str
    submit_selector: str | None = None
    success_selector: str | None = None
    success_url_pattern: str | None = None
    username_env_var: str = "FLOWSCOUT_AUTH_USERNAME"
    password_env_var: str = "FLOWSCOUT_AUTH_PASSWORD"
    post_login_wait_ms: int = Field(default=3000, ge=0)


@dataclass(slots=True)
class AuthBootstrap:
    """Runtime auth bootstrap payload with resolved credentials."""

    profile_name: str
    login_url: str | None
    username_selector: str
    password_selector: str
    submit_selector: str | None
    success_selector: str | None
    success_url_pattern: str | None
    username: str
    password: str
    post_login_wait_ms: int
    required: bool


def load_auth_profiles(*, config_file: str) -> dict[str, AuthProfile]:
    """Load auth profiles from a TOML file.

    File shape:
    [profiles.<name>]
    domains = ["example.com", "*.example.com"]
    environments = ["staging"]
    login_url = "https://example.com/login"
    username_selector = "#username"
    password_selector = "#password"
    submit_selector = "button[type='submit']"
    success_selector = "[data-test='dashboard']"
    success_url_pattern = "/dashboard"
    username_env_var = "E2E_USER"
    password_env_var = "E2E_PASS"
    post_login_wait_ms = 3000
    """
    path = Path(config_file).expanduser()
    if not path.exists():
        return {}

    try:
        with path.open(mode="rb") as handle:
            payload = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise AuthConfigError(f"Invalid auth config TOML at {path}: {exc}") from exc
    except OSError as exc:
        raise AuthConfigError(f"Could not read auth config at {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise AuthConfigError("Auth config root must be a key/value table.")

    profiles_raw = payload.get("profiles", {})
    if not isinstance(profiles_raw, dict):
        raise AuthConfigError("Auth config must contain a [profiles] table.")

    profiles: dict[str, AuthProfile] = {}
    for name, data in profiles_raw.items():
        if not isinstance(data, dict):
            raise AuthConfigError(f"Profile '{name}' must be a TOML table.")
        try:
            profiles[name] = AuthProfile.model_validate(
                {
                    "name": name,
                    **data,
                }
            )
        except Exception as exc:  # pragma: no cover - pydantic detail path noise
            raise AuthConfigError(f"Invalid auth profile '{name}': {exc}") from exc

    return profiles


def select_auth_profile(
    *,
    profiles: dict[str, AuthProfile],
    start_url: str,
    environment: str,
    requested_profile: str | None = None,
) -> AuthProfile | None:
    """Select an auth profile by explicit name or domain/environment match."""
    if requested_profile:
        return profiles.get(requested_profile)

    host = (urlparse(start_url).hostname or "").lower()
    env = environment.lower()

    for profile in profiles.values():
        if not _matches_domain(profile=profile, host=host):
            continue
        if not _matches_environment(profile=profile, environment=env):
            continue
        return profile

    return None


def build_auth_bootstrap(
    *,
    profile: AuthProfile,
    required: bool,
) -> AuthBootstrap:
    """Build runtime auth bootstrap by resolving credentials from env vars."""
    username = os.getenv(profile.username_env_var, "")
    password = os.getenv(profile.password_env_var, "")

    missing_vars = []
    if not username:
        missing_vars.append(profile.username_env_var)
    if not password:
        missing_vars.append(profile.password_env_var)

    if missing_vars:
        joined = ", ".join(missing_vars)
        raise AuthConfigError(
            f"Auth profile '{profile.name}' is missing required environment variable(s): {joined}",
        )

    if profile.success_url_pattern:
        try:
            re.compile(profile.success_url_pattern)
        except re.error as exc:
            raise AuthConfigError(
                f"Auth profile '{profile.name}' has invalid success_url_pattern: {exc}",
            ) from exc

    return AuthBootstrap(
        profile_name=profile.name,
        login_url=profile.login_url,
        username_selector=profile.username_selector,
        password_selector=profile.password_selector,
        submit_selector=profile.submit_selector,
        success_selector=profile.success_selector,
        success_url_pattern=profile.success_url_pattern,
        username=username,
        password=password,
        post_login_wait_ms=profile.post_login_wait_ms,
        required=required,
    )


def _matches_domain(*, profile: AuthProfile, host: str) -> bool:
    """Return whether profile matches host."""
    if not profile.domains:
        return True
    for pattern in profile.domains:
        candidate = pattern.lower()
        if fnmatch(host, candidate):
            return True
        if host == candidate:
            return True
        if host.endswith(f".{candidate}"):
            return True
    return False


def _matches_environment(*, profile: AuthProfile, environment: str) -> bool:
    """Return whether profile matches environment."""
    if not profile.environments:
        return True
    lower_envs = {value.lower() for value in profile.environments}
    return environment in lower_envs


def sanitize_auth_summary(*, profile: AuthProfile) -> dict[str, Any]:
    """Return safe, non-secret auth profile metadata for reporting/logging."""
    return {
        "profile": profile.name,
        "domains": profile.domains,
        "environments": profile.environments,
        "login_url": profile.login_url,
        "username_env_var": profile.username_env_var,
        "password_env_var": profile.password_env_var,
        "post_login_wait_ms": profile.post_login_wait_ms,
    }

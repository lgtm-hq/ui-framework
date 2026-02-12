"""Config loading, TOML parsing, and domain-scoped option resolution."""

from __future__ import annotations

import tomllib
from fnmatch import fnmatch
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import click
from click.core import ParameterSource

from flowscout.cli.app import console
from flowscout.core.auth import (
    AuthBootstrap,
    AuthConfigError,
    build_auth_bootstrap,
    load_auth_profiles,
    sanitize_auth_summary,
    select_auth_profile,
)


def _load_crawl_config(*, config_file: str) -> dict[str, Any]:
    """Load crawl defaults from a TOML-style config file.

    Args:
        config_file: Path to config file.

    Returns:
        Parsed key/value config dictionary.

    Raises:
        click.ClickException: If config file cannot be parsed as TOML.
    """
    config_path = Path(config_file).expanduser()
    if not config_path.exists():
        return {}

    try:
        with config_path.open(mode="rb") as handle:
            payload = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise click.ClickException(
            f"Invalid crawl config at {config_path}: {exc}",
        ) from exc
    except OSError as exc:
        raise click.ClickException(
            f"Could not read crawl config at {config_path}: {exc}",
        ) from exc

    if not isinstance(payload, dict):
        raise click.ClickException(
            f"Invalid crawl config at {config_path}: root must be a key/value table",
        )
    return payload


def _came_from_cli(*, ctx: click.Context, parameter: str) -> bool:
    """Return whether a Click parameter was explicitly passed via CLI."""
    return ctx.get_parameter_source(parameter) == ParameterSource.COMMANDLINE


def _find_config_value(
    *,
    config: dict[str, Any],
    keys: tuple[str, ...],
) -> tuple[str, Any] | None:
    """Find first matching key in config and return key/value pair."""
    for key in keys:
        if key in config:
            return key, config[key]
    return None


def _coerce_int(*, value: Any, config_key: str) -> int:
    """Validate integer value loaded from config."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise click.ClickException(
            f"Config key '{config_key}' must be an integer, got {type(value).__name__}",
        )
    return int(value)


def _coerce_bool(*, value: Any, config_key: str) -> bool:
    """Validate boolean value loaded from config."""
    if not isinstance(value, bool):
        raise click.ClickException(
            f"Config key '{config_key}' must be true/false, got {type(value).__name__}",
        )
    return value


def _coerce_str(*, value: Any, config_key: str) -> str:
    """Validate string value loaded from config."""
    if not isinstance(value, str):
        raise click.ClickException(
            f"Config key '{config_key}' must be a string, got {type(value).__name__}",
        )
    return value


def _resolve_int_option(
    *,
    ctx: click.Context,
    parameter: str,
    cli_value: int,
    config: dict[str, Any],
    config_keys: tuple[str, ...],
) -> int:
    """Resolve integer option with precedence: CLI > config > CLI default."""
    if _came_from_cli(ctx=ctx, parameter=parameter):
        return cli_value
    maybe_value = _find_config_value(config=config, keys=config_keys)
    if maybe_value is None:
        return cli_value
    key, value = maybe_value
    return _coerce_int(value=value, config_key=key)


def _resolve_bool_option(
    *,
    ctx: click.Context,
    parameter: str,
    cli_value: bool,
    config: dict[str, Any],
    config_keys: tuple[str, ...],
) -> bool:
    """Resolve bool option with precedence: CLI > config > CLI default."""
    if _came_from_cli(ctx=ctx, parameter=parameter):
        return cli_value
    maybe_value = _find_config_value(config=config, keys=config_keys)
    if maybe_value is None:
        return cli_value
    key, value = maybe_value
    return _coerce_bool(value=value, config_key=key)


def _resolve_str_option(
    *,
    ctx: click.Context,
    parameter: str,
    cli_value: str,
    config: dict[str, Any],
    config_keys: tuple[str, ...],
) -> str:
    """Resolve string option with precedence: CLI > config > CLI default."""
    if _came_from_cli(ctx=ctx, parameter=parameter):
        return cli_value
    maybe_value = _find_config_value(config=config, keys=config_keys)
    if maybe_value is None:
        return cli_value
    key, value = maybe_value
    return _coerce_str(value=value, config_key=key)


def _resolve_int_config(
    *,
    config: dict[str, Any],
    config_keys: tuple[str, ...],
    default: int,
) -> int:
    """Resolve int value from config with fallback to default."""
    maybe_value = _find_config_value(config=config, keys=config_keys)
    if maybe_value is None:
        return default
    key, value = maybe_value
    return _coerce_int(value=value, config_key=key)


def _resolve_bool_config(
    *,
    config: dict[str, Any],
    config_keys: tuple[str, ...],
    default: bool,
) -> bool:
    """Resolve bool value from config with fallback to default."""
    maybe_value = _find_config_value(config=config, keys=config_keys)
    if maybe_value is None:
        return default
    key, value = maybe_value
    return _coerce_bool(value=value, config_key=key)


def _resolve_domain_scoped_config(
    *,
    ctx: click.Context,
    start_url: str,
    cli_environment: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Merge optional domain/environment overrides into crawl config.

    Supported shape:

    [domains."<pattern>"]
    max_depth = 3
    environment = "staging"

    [domains."<pattern>".environments.staging]
    max_states = 120
    """
    merged: dict[str, Any] = {k: v for k, v in config.items() if k != "domains"}
    raw_domains = config.get("domains")
    if not isinstance(raw_domains, dict):
        return merged

    host = (urlparse(start_url).hostname or "").lower()
    matches: list[tuple[tuple[int, int, int], str, dict[str, Any]]] = []
    for pattern, domain_config in raw_domains.items():
        if not isinstance(pattern, str) or not isinstance(domain_config, dict):
            continue
        if not fnmatch(host, pattern.lower()):
            continue
        matches.append(
            (
                _domain_match_score(pattern=pattern.lower(), host=host),
                pattern,
                domain_config,
            )
        )

    if not matches:
        return merged

    matches.sort(key=lambda item: item[0])
    for _, _, domain_config in matches:
        for key, value in domain_config.items():
            if key == "environments":
                continue
            merged[key] = value

    if _came_from_cli(ctx=ctx, parameter="environment"):
        effective_env = cli_environment
    else:
        configured_env = merged.get("environment")
        effective_env = (
            configured_env if isinstance(configured_env, str) else cli_environment
        )
    normalized_env = effective_env.lower()

    for _, _, domain_config in matches:
        envs = domain_config.get("environments")
        if not isinstance(envs, dict):
            continue

        matching_env: dict[str, Any] | None = None
        for env_name, env_config in envs.items():
            if not isinstance(env_name, str) or not isinstance(env_config, dict):
                continue
            if env_name.lower() == normalized_env:
                matching_env = env_config
                break

        if matching_env:
            merged.update(matching_env)

    return merged


def _domain_match_score(*, pattern: str, host: str) -> tuple[int, int, int]:
    """Return sort score for domain override precedence."""
    wildcard_count = pattern.count("*") + pattern.count("?")
    literal_chars = len(pattern.replace("*", "").replace("?", ""))
    exact = 1 if pattern == host else 0
    return (exact, literal_chars, -wildcard_count)


def _resolve_auth_bootstrap(
    *,
    start_url: str,
    environment: str,
    auth_profile_name: str | None,
    auth_config_file: str,
    auth_required: bool,
) -> tuple[AuthBootstrap | None, dict[str, Any] | None]:
    """Resolve auth bootstrap from auth profile config and environment variables."""
    try:
        profiles = load_auth_profiles(config_file=auth_config_file)
    except AuthConfigError as exc:
        raise click.ClickException(str(exc)) from exc

    if not profiles:
        if auth_profile_name or auth_required:
            raise click.ClickException(
                f"No auth profiles found in {auth_config_file},"
                " but auth was requested.",
            )
        return None, None

    selected = select_auth_profile(
        profiles=profiles,
        start_url=start_url,
        environment=environment,
        requested_profile=auth_profile_name,
    )
    if selected is None:
        if auth_profile_name:
            raise click.ClickException(
                f"Requested auth profile '{auth_profile_name}'"
                " was not found or did not match"
                " target context.",
            )
        if auth_required:
            raise click.ClickException(
                "No matching auth profile found for target"
                " URL/environment and auth is required.",
            )
        return None, None

    try:
        bootstrap = build_auth_bootstrap(profile=selected, required=auth_required)
    except AuthConfigError as exc:
        if auth_required:
            raise click.ClickException(str(exc)) from exc
        console.print(f"  [yellow]Auth disabled:[/yellow] {exc}")
        return None, None

    return bootstrap, sanitize_auth_summary(profile=selected)

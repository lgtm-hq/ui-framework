"""Tests for auth profile loading and runtime bootstrap."""

from pathlib import Path

import pytest

from flowscout.core.auth import (
    AuthConfigError,
    build_auth_bootstrap,
    load_auth_profiles,
    sanitize_auth_summary,
    select_auth_profile,
)


def test_load_auth_profiles_from_toml(tmp_path: Path) -> None:
    config_path = tmp_path / ".flowscout-auth.toml"
    toml = """
[profiles.shop_staging]
domains = ["shop.example.com"]
environments = ["staging"]
login_url = "https://shop.example.com/login"
username_selector = "#user"
password_selector = "#pass"
submit_selector = "button[type='submit']"
username_env_var = "SHOP_USER"
password_env_var = "SHOP_PASS"
post_login_wait_ms = 1500
""".strip()
    config_path.write_text(toml)

    profiles = load_auth_profiles(config_file=str(config_path))

    assert "shop_staging" in profiles
    profile = profiles["shop_staging"]
    assert profile.name == "shop_staging"
    assert profile.username_env_var == "SHOP_USER"
    assert profile.post_login_wait_ms == 1500


def test_select_auth_profile_matches_domain_and_environment(tmp_path: Path) -> None:
    config_path = tmp_path / ".flowscout-auth.toml"
    toml = """
[profiles.default]
domains = ["*.example.com"]
environments = ["staging"]
username_selector = "#username"
password_selector = "#password"
""".strip()
    config_path.write_text(toml)
    profiles = load_auth_profiles(config_file=str(config_path))

    selected = select_auth_profile(
        profiles=profiles,
        start_url="https://shop.example.com",
        environment="staging",
    )

    assert selected is not None
    assert selected.name == "default"


def test_build_auth_bootstrap_reads_env_vars(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path = tmp_path / ".flowscout-auth.toml"
    toml = """
[profiles.default]
domains = ["example.com"]
environments = ["dev"]
username_selector = "#username"
password_selector = "#password"
username_env_var = "E2E_USER"
password_env_var = "E2E_PASS"
""".strip()
    config_path.write_text(toml)
    profiles = load_auth_profiles(config_file=str(config_path))
    profile = profiles["default"]

    monkeypatch.setenv("E2E_USER", "test-user")
    monkeypatch.setenv("E2E_PASS", "test-pass")

    bootstrap = build_auth_bootstrap(profile=profile, required=True)

    assert bootstrap.profile_name == "default"
    assert bootstrap.username == "test-user"
    assert bootstrap.password == "test-pass"  # nosec B105 - test fixture


def test_build_auth_bootstrap_raises_for_missing_env_vars(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path = tmp_path / ".flowscout-auth.toml"
    toml = """
[profiles.default]
username_selector = "#username"
password_selector = "#password"
username_env_var = "MISSING_USER"
password_env_var = "MISSING_PASS"
""".strip()
    config_path.write_text(toml)
    profiles = load_auth_profiles(config_file=str(config_path))
    profile = profiles["default"]

    monkeypatch.delenv("MISSING_USER", raising=False)
    monkeypatch.delenv("MISSING_PASS", raising=False)

    with pytest.raises(AuthConfigError):
        build_auth_bootstrap(profile=profile, required=True)


def test_sanitize_auth_summary_hides_secret_values(tmp_path: Path) -> None:
    config_path = tmp_path / ".flowscout-auth.toml"
    toml = """
[profiles.default]
domains = ["example.com"]
username_selector = "#username"
password_selector = "#password"
username_env_var = "AUTH_USER"
password_env_var = "AUTH_PASS"
""".strip()
    config_path.write_text(toml)
    profiles = load_auth_profiles(config_file=str(config_path))
    summary = sanitize_auth_summary(profile=profiles["default"])

    assert summary["profile"] == "default"
    assert summary["username_env_var"] == "AUTH_USER"
    assert "password" not in summary

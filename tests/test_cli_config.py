"""Tests for crawl config loading and option resolution."""

from pathlib import Path

import click
import pytest
from click.core import ParameterSource

from flowscout.cli import (
    CrawlConfig,
    _domain_match_score,
    _load_crawl_config,
    _resolve_auth_bootstrap,
    _resolve_bool_config,
    _resolve_bool_option,
    _resolve_domain_scoped_config,
    _resolve_int_config,
    _resolve_int_option,
    _resolve_str_option,
    validate_crawl_config,
)


def _make_context(*, source: ParameterSource, parameter: str) -> click.Context:
    """Build a click context with a controlled parameter source."""
    ctx = click.Context(click.Command("test"))
    ctx.set_parameter_source(parameter, source)
    return ctx


def test_load_crawl_config_missing_file_returns_empty(tmp_path: Path) -> None:
    config = _load_crawl_config(config_file=str(tmp_path / ".crawl-config"))
    assert config == {}


def test_load_crawl_config_parses_toml(tmp_path: Path) -> None:
    config_path = tmp_path / ".crawl-config"
    config_path.write_text("max_depth = 2\ncapture_screenshots = true\n")

    config = _load_crawl_config(config_file=str(config_path))

    assert config["max_depth"] == 2
    assert config["capture_screenshots"] is True


def test_load_crawl_config_rejects_invalid_toml(tmp_path: Path) -> None:
    config_path = tmp_path / ".crawl-config"
    config_path.write_text("max_depth =\n")

    with pytest.raises(click.ClickException):
        _load_crawl_config(config_file=str(config_path))


def test_resolve_int_option_prefers_config_when_cli_default() -> None:
    ctx = _make_context(source=ParameterSource.DEFAULT, parameter="max_depth")

    value = _resolve_int_option(
        ctx=ctx,
        parameter="max_depth",
        cli_value=3,
        config={"max_depth": 7},
        config_keys=("max_depth",),
    )

    assert value == 7


def test_resolve_int_option_prefers_cli_when_explicit() -> None:
    ctx = _make_context(source=ParameterSource.COMMANDLINE, parameter="max_depth")

    value = _resolve_int_option(
        ctx=ctx,
        parameter="max_depth",
        cli_value=3,
        config={"max_depth": 7},
        config_keys=("max_depth",),
    )

    assert value == 3


def test_resolve_str_option_uses_first_matching_alias() -> None:
    ctx = _make_context(source=ParameterSource.DEFAULT, parameter="timeout")

    value = _resolve_str_option(
        ctx=ctx,
        parameter="timeout",
        cli_value="default",
        config={"timeout_ms": "from-alias"},
        config_keys=("timeout", "timeout_ms"),
    )

    assert value == "from-alias"


def test_resolve_bool_option_rejects_non_boolean_values() -> None:
    ctx = _make_context(source=ParameterSource.DEFAULT, parameter="screenshot")

    with pytest.raises(click.ClickException):
        _resolve_bool_option(
            ctx=ctx,
            parameter="screenshot",
            cli_value=True,
            config={"capture_screenshots": "yes"},
            config_keys=("capture_screenshots",),
        )


def test_resolve_int_config_uses_default_when_key_missing() -> None:
    value = _resolve_int_config(
        config={},
        config_keys=("action_timeout_ms",),
        default=5000,
    )
    assert value == 5000


def test_resolve_bool_config_uses_default_when_key_missing() -> None:
    value = _resolve_bool_config(
        config={},
        config_keys=("smart_stop_on_saturation",),
        default=True,
    )
    assert value is True


def test_resolve_bool_config_reads_config_value() -> None:
    value = _resolve_bool_config(
        config={"smart_stop_on_saturation": False},
        config_keys=("smart_stop_on_saturation",),
        default=True,
    )
    assert value is False


def test_resolve_auth_bootstrap_returns_none_when_not_required(tmp_path: Path) -> None:
    auth_config_path = tmp_path / ".flowscout-auth.toml"

    bootstrap, summary = _resolve_auth_bootstrap(
        start_url="https://example.com",
        environment="dev",
        auth_profile_name=None,
        auth_config_file=str(auth_config_path),
        auth_required=False,
    )

    assert bootstrap is None
    assert summary is None


def test_resolve_auth_bootstrap_raises_when_required_without_config(
    tmp_path: Path,
) -> None:
    auth_config_path = tmp_path / ".flowscout-auth.toml"

    with pytest.raises(click.ClickException):
        _resolve_auth_bootstrap(
            start_url="https://example.com",
            environment="dev",
            auth_profile_name=None,
            auth_config_file=str(auth_config_path),
            auth_required=True,
        )


def test_domain_match_score_prefers_exact_and_more_specific_patterns() -> None:
    exact = _domain_match_score(pattern="shop.example.com", host="shop.example.com")
    wildcard = _domain_match_score(pattern="*.example.com", host="shop.example.com")

    assert exact > wildcard


def test_resolve_domain_scoped_config_applies_domain_and_env_overrides() -> None:
    ctx = click.Context(click.Command("test"))
    ctx.set_parameter_source("environment", ParameterSource.DEFAULT)

    config = {
        "max_depth": 2,
        "max_states": 30,
        "environment": "dev",
        "domains": {
            "*.example.com": {
                "max_depth": 4,
                "environments": {
                    "staging": {
                        "max_states": 90,
                        "auth_profile": "shop_staging",
                    }
                },
            },
            "shop.example.com": {
                "max_depth": 5,
                "environment": "staging",
            },
        },
    }

    resolved = _resolve_domain_scoped_config(
        ctx=ctx,
        start_url="https://shop.example.com",
        cli_environment="dev",
        config=config,
    )

    assert resolved["max_depth"] == 5
    assert resolved["environment"] == "staging"
    assert resolved["max_states"] == 90
    assert resolved["auth_profile"] == "shop_staging"


def test_resolve_domain_scoped_config_respects_cli_environment() -> None:
    ctx = click.Context(click.Command("test"))
    ctx.set_parameter_source("environment", ParameterSource.COMMANDLINE)

    config = {
        "domains": {
            "shop.example.com": {
                "environment": "staging",
                "environments": {
                    "staging": {"max_states": 70},
                    "prod": {"max_states": 40},
                },
            }
        }
    }

    resolved = _resolve_domain_scoped_config(
        ctx=ctx,
        start_url="https://shop.example.com",
        cli_environment="prod",
        config=config,
    )

    assert resolved["environment"] == "staging"
    assert resolved["max_states"] == 40


# --- CrawlConfig Pydantic validation tests ---


class TestCrawlConfig:
    def test_defaults_are_valid(self) -> None:
        config = CrawlConfig()
        assert config.max_depth == 3
        assert config.max_states == 50
        assert config.input_profile.value == "safe"

    def test_valid_config_accepted(self) -> None:
        config = CrawlConfig.model_validate(
            {
                "max_depth": 5,
                "max_states": 100,
                "input_profile": "safe",
                "outcome_mode": "legacy",
                "link_scope_mode": "origin",
            }
        )
        assert config.max_depth == 5
        assert config.max_states == 100

    def test_rejects_max_depth_too_high(self) -> None:
        with pytest.raises(Exception, match="less than or equal to 20"):
            CrawlConfig(max_depth=999)

    def test_rejects_max_depth_too_low(self) -> None:
        with pytest.raises(Exception, match="greater than or equal to 1"):
            CrawlConfig(max_depth=0)

    def test_rejects_max_states_too_high(self) -> None:
        with pytest.raises(Exception, match="less than or equal to 500"):
            CrawlConfig(max_states=9999)

    def test_rejects_invalid_input_profile(self) -> None:
        with pytest.raises(Exception, match="input_profile"):
            CrawlConfig.model_validate({"input_profile": "bogus"})

    def test_rejects_invalid_outcome_mode(self) -> None:
        with pytest.raises(Exception, match="outcome_mode"):
            CrawlConfig.model_validate({"outcome_mode": "invalid"})

    def test_rejects_unknown_keys(self) -> None:
        with pytest.raises(Exception, match="extra_field"):
            CrawlConfig.model_validate({"extra_field": "unexpected"})

    def test_rejects_timeout_below_minimum(self) -> None:
        with pytest.raises(Exception, match="greater than or equal to 1000"):
            CrawlConfig(navigation_timeout_ms=100)

    def test_allowed_domains_defaults_empty(self) -> None:
        config = CrawlConfig()
        assert config.allowed_domains == []

    def test_allowed_domains_accepted(self) -> None:
        config = CrawlConfig(allowed_domains=["api.example.com", "cdn.example.com"])
        assert config.allowed_domains == ["api.example.com", "cdn.example.com"]

    def test_domains_passthrough_accepted(self) -> None:
        config = CrawlConfig(
            domains={"*.example.com": {"max_depth": 5}},
        )
        assert "*.example.com" in config.domains

    def test_document_only_outcome_mode_accepted(self) -> None:
        config = CrawlConfig.model_validate({"outcome_mode": "document_only"})
        assert config.outcome_mode.value == "document_only"


class TestValidateCrawlConfig:
    def test_missing_file_returns_defaults(self, tmp_path: Path) -> None:
        config = validate_crawl_config(
            config_file=str(tmp_path / ".crawl-config"),
        )
        assert config.max_depth == 3

    def test_valid_file_parsed(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".crawl-config"
        config_path.write_text("max_depth = 7\nmax_states = 200\n")
        config = validate_crawl_config(config_file=str(config_path))
        assert config.max_depth == 7
        assert config.max_states == 200

    def test_invalid_values_raise_click_exception(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".crawl-config"
        config_path.write_text("max_depth = 999\n")
        with pytest.raises(click.ClickException, match="Invalid .crawl-config"):
            validate_crawl_config(config_file=str(config_path))

    def test_unknown_keys_raise_click_exception(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".crawl-config"
        config_path.write_text("typo_key = true\n")
        with pytest.raises(click.ClickException, match="typo_key"):
            validate_crawl_config(config_file=str(config_path))

    def test_invalid_enum_raises_click_exception(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".crawl-config"
        config_path.write_text('input_profile = "bogus"\n')
        with pytest.raises(click.ClickException, match="Invalid .crawl-config"):
            validate_crawl_config(config_file=str(config_path))

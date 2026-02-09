"""CLI entry point for flowscout."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import tomllib
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import click
from click.core import ParameterSource
from rich.console import Console
from rich.table import Table

from flowscout import __version__
from flowscout.analysis.graph import ExplorationGraph, ExplorationResult
from flowscout.codegen.playwright_tests import generate_test_suite
from flowscout.core.auth import (
    AuthBootstrap,
    AuthConfigError,
    build_auth_bootstrap,
    load_auth_profiles,
    sanitize_auth_summary,
    select_auth_profile,
)
from flowscout.core.browser import BrowserManager
from flowscout.core.navigator import Navigator
from flowscout.core.policy import ActionPolicyConfig
from flowscout.core.state import ExplorerConfig, ExplorationStrategy, InputProfile
from flowscout.reporting.html import HTMLReporter
from flowscout.reporting.terminal import TerminalReporter
from flowscout.storage.db import FlowscoutDB

console = Console()

DEFAULT_DB_PATH = ".flowscout/history.db"
DEFAULT_CRAWL_CONFIG_PATH = ".crawl-config"
DEFAULT_AUTH_CONFIG_PATH = ".flowscout-auth.toml"
DEFAULT_LOW_CONFIDENCE_THRESHOLD = 0.6


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
    return value


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
                f"No auth profiles found in {auth_config_file}, but auth was requested.",
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
                f"Requested auth profile '{auth_profile_name}' was not found or did not match target context.",
            )
        if auth_required:
            raise click.ClickException(
                "No matching auth profile found for target URL/environment and auth is required.",
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


@click.group()
@click.version_option(version=__version__, prog_name="flowscout")
def main() -> None:
    """Flowscout — LLM-free automated web path exploration."""


@main.command()
@click.argument("url")
@click.option(
    "--max-depth", "-d", default=3, help="Maximum traversal depth from start URL."
)
@click.option(
    "--max-states", "-s", default=50, help="Maximum unique states to discover."
)
@click.option("--max-actions", "-a", default=20, help="Maximum actions per state.")
@click.option(
    "--headless/--no-headless", default=True, help="Run browser in headless mode."
)
@click.option(
    "--timeout", "-t", default=10000, help="Navigation timeout in milliseconds."
)
@click.option(
    "--output-dir", "-o", default="./reports", help="Output directory for reports."
)
@click.option(
    "--environment",
    default="dev",
    help="Environment label for workspace isolation (e.g., dev, staging, prod).",
)
@click.option(
    "--screenshot/--no-screenshot",
    default=True,
    help="Capture action evidence screenshots with highlighted targets.",
)
@click.option(
    "--strategy",
    type=click.Choice(["bfs", "dfs", "priority"]),
    default="priority",
    help="Exploration strategy.",
)
@click.option("--verbose", "-v", is_flag=True, help="Verbose output.")
@click.option(
    "--generate-tests",
    "-g",
    is_flag=True,
    help="Generate Playwright test suite from results.",
)
@click.option(
    "--test-framework",
    type=click.Choice(["pytest", "playwright"]),
    default="pytest",
    help="Test framework for code generation.",
)
@click.option("--bdd", is_flag=True, help="Generate Gherkin .feature file.")
@click.option("--narrative", is_flag=True, help="Generate Markdown narrative report.")
@click.option(
    "--db-path", default=DEFAULT_DB_PATH, help="SQLite database path for history."
)
@click.option("--no-db", is_flag=True, help="Skip saving to database.")
@click.option(
    "--smart",
    is_flag=True,
    help="Enable smart mode: archetype recognition, contextual input, coverage-aware exploration.",
)
@click.option(
    "--input-profile",
    type=click.Choice(["safe", "contextual", "negative"]),
    default="safe",
    help="Input generation profile.",
)
@click.option(
    "--enforce-non-destructive/--no-enforce-non-destructive",
    default=True,
    help="Enforce non-destructive exploration policy.",
)
@click.option(
    "--allow-form-submits",
    is_flag=True,
    help="Allow form submit actions (disabled by default for safety).",
)
@click.option(
    "--config-file",
    default=DEFAULT_CRAWL_CONFIG_PATH,
    show_default=True,
    help="Path to TOML-style crawl defaults (CLI args override file values).",
)
@click.option(
    "--auth-config-file",
    default=DEFAULT_AUTH_CONFIG_PATH,
    show_default=True,
    help="Path to auth profile TOML file.",
)
@click.option(
    "--auth-profile",
    default="",
    help="Explicit auth profile name. If omitted, profile is auto-selected by domain/environment.",
)
@click.option(
    "--auth-required/--no-auth-required",
    default=False,
    help="Fail fast if auth profile or credentials are missing.",
)
def explore(
    url: str,
    max_depth: int,
    max_states: int,
    max_actions: int,
    headless: bool,
    timeout: int,
    output_dir: str,
    environment: str,
    screenshot: bool,
    strategy: str,
    verbose: bool,
    generate_tests: bool,
    test_framework: str,
    bdd: bool,
    narrative: bool,
    db_path: str,
    no_db: bool,
    smart: bool,
    input_profile: str,
    enforce_non_destructive: bool,
    allow_form_submits: bool,
    config_file: str,
    auth_config_file: str,
    auth_profile: str,
    auth_required: bool,
) -> None:
    """Explore a web application starting from URL."""
    ctx = click.get_current_context()
    crawl_config = _load_crawl_config(config_file=config_file)

    resolved_max_depth = _resolve_int_option(
        ctx=ctx,
        parameter="max_depth",
        cli_value=max_depth,
        config=crawl_config,
        config_keys=("max_depth",),
    )
    resolved_max_states = _resolve_int_option(
        ctx=ctx,
        parameter="max_states",
        cli_value=max_states,
        config=crawl_config,
        config_keys=("max_states",),
    )
    resolved_max_actions = _resolve_int_option(
        ctx=ctx,
        parameter="max_actions",
        cli_value=max_actions,
        config=crawl_config,
        config_keys=("max_actions", "max_actions_per_state"),
    )
    resolved_headless = _resolve_bool_option(
        ctx=ctx,
        parameter="headless",
        cli_value=headless,
        config=crawl_config,
        config_keys=("headless",),
    )
    resolved_timeout = _resolve_int_option(
        ctx=ctx,
        parameter="timeout",
        cli_value=timeout,
        config=crawl_config,
        config_keys=("timeout", "timeout_ms", "navigation_timeout_ms"),
    )
    resolved_output_dir = _resolve_str_option(
        ctx=ctx,
        parameter="output_dir",
        cli_value=output_dir,
        config=crawl_config,
        config_keys=("output_dir",),
    )
    resolved_environment = _resolve_str_option(
        ctx=ctx,
        parameter="environment",
        cli_value=environment,
        config=crawl_config,
        config_keys=("environment",),
    )
    resolved_screenshot = _resolve_bool_option(
        ctx=ctx,
        parameter="screenshot",
        cli_value=screenshot,
        config=crawl_config,
        config_keys=("capture_screenshots", "take_screenshots", "screenshot"),
    )
    resolved_strategy = _resolve_str_option(
        ctx=ctx,
        parameter="strategy",
        cli_value=strategy,
        config=crawl_config,
        config_keys=("strategy",),
    )
    resolved_verbose = _resolve_bool_option(
        ctx=ctx,
        parameter="verbose",
        cli_value=verbose,
        config=crawl_config,
        config_keys=("verbose",),
    )
    resolved_db_path = _resolve_str_option(
        ctx=ctx,
        parameter="db_path",
        cli_value=db_path,
        config=crawl_config,
        config_keys=("db_path",),
    )
    resolved_smart = _resolve_bool_option(
        ctx=ctx,
        parameter="smart",
        cli_value=smart,
        config=crawl_config,
        config_keys=("smart",),
    )
    resolved_input_profile = _resolve_str_option(
        ctx=ctx,
        parameter="input_profile",
        cli_value=input_profile,
        config=crawl_config,
        config_keys=("input_profile",),
    )
    resolved_enforce_non_destructive = _resolve_bool_option(
        ctx=ctx,
        parameter="enforce_non_destructive",
        cli_value=enforce_non_destructive,
        config=crawl_config,
        config_keys=("enforce_non_destructive",),
    )
    resolved_allow_form_submits = _resolve_bool_option(
        ctx=ctx,
        parameter="allow_form_submits",
        cli_value=allow_form_submits,
        config=crawl_config,
        config_keys=("allow_form_submits",),
    )
    resolved_auth_config_file = _resolve_str_option(
        ctx=ctx,
        parameter="auth_config_file",
        cli_value=auth_config_file,
        config=crawl_config,
        config_keys=("auth_config_file",),
    )
    resolved_auth_profile_name = _resolve_str_option(
        ctx=ctx,
        parameter="auth_profile",
        cli_value=auth_profile,
        config=crawl_config,
        config_keys=("auth_profile",),
    ).strip()
    resolved_auth_required = _resolve_bool_option(
        ctx=ctx,
        parameter="auth_required",
        cli_value=auth_required,
        config=crawl_config,
        config_keys=("auth_required",),
    )

    if _came_from_cli(ctx=ctx, parameter="no_db"):
        save_to_db = not no_db
    else:
        persist_history_cfg = _find_config_value(
            config=crawl_config,
            keys=("persist_history",),
        )
        if persist_history_cfg is not None:
            _, persist_history = persist_history_cfg
            save_to_db = _coerce_bool(
                value=persist_history,
                config_key="persist_history",
            )
        else:
            no_db_cfg = _find_config_value(config=crawl_config, keys=("no_db",))
            if no_db_cfg is not None:
                _, no_db_config_value = no_db_cfg
                save_to_db = not _coerce_bool(
                    value=no_db_config_value,
                    config_key="no_db",
                )
            else:
                save_to_db = True

    default_action_timeout_ms = int(
        ExplorerConfig.model_fields["action_timeout_ms"].default,
    )
    default_stability_timeout_ms = int(
        ExplorerConfig.model_fields["stability_timeout_ms"].default,
    )
    default_load_wait_timeout_ms = int(
        ExplorerConfig.model_fields["load_wait_timeout_ms"].default,
    )
    resolved_action_timeout_ms = _resolve_int_config(
        config=crawl_config,
        config_keys=("action_timeout_ms",),
        default=default_action_timeout_ms,
    )
    resolved_stability_timeout_ms = _resolve_int_config(
        config=crawl_config,
        config_keys=("stability_timeout_ms",),
        default=default_stability_timeout_ms,
    )
    resolved_load_wait_timeout_ms = _resolve_int_config(
        config=crawl_config,
        config_keys=("load_wait_timeout_ms",),
        default=default_load_wait_timeout_ms,
    )

    config = ExplorerConfig(
        start_url=url,
        max_depth=resolved_max_depth,
        max_states=resolved_max_states,
        max_actions_per_state=resolved_max_actions,
        headless=resolved_headless,
        timeout_ms=resolved_timeout,
        action_timeout_ms=resolved_action_timeout_ms,
        stability_timeout_ms=resolved_stability_timeout_ms,
        load_wait_timeout_ms=resolved_load_wait_timeout_ms,
        output_dir=resolved_output_dir,
        environment=resolved_environment,
        take_screenshots=resolved_screenshot,
        strategy=ExplorationStrategy(resolved_strategy),
        verbose=resolved_verbose,
        smart_mode=resolved_smart,
        input_profile=InputProfile(resolved_input_profile),
        auth_profile=resolved_auth_profile_name or None,
        auth_required=resolved_auth_required,
        action_policy=ActionPolicyConfig(
            enforce_non_destructive=resolved_enforce_non_destructive,
            block_form_submissions=not resolved_allow_form_submits,
        ),
    )

    auth_bootstrap, auth_profile_summary = _resolve_auth_bootstrap(
        start_url=url,
        environment=resolved_environment,
        auth_profile_name=resolved_auth_profile_name or None,
        auth_config_file=resolved_auth_config_file,
        auth_required=resolved_auth_required,
    )

    asyncio.run(
        _run_exploration(
            config,
            generate_tests=generate_tests,
            test_framework=test_framework,
            generate_bdd=bdd,
            generate_narrative=narrative,
            db_path=resolved_db_path,
            save_to_db=save_to_db,
            auth_bootstrap=auth_bootstrap,
            auth_profile_summary=auth_profile_summary,
        )
    )


def _build_output_dirs(
    config: ExplorerConfig,
    now: datetime,
    *,
    smart_workspace: bool = False,
) -> tuple[Path, Path | None]:
    """Build output directory paths.

    Args:
        config: Explorer configuration (provides output_dir and start_url).
        now: Current timestamp for directory naming.
        smart_workspace: If True, organize by site domain with per-run subdirs.

    Returns:
        (run_dir, workspace_dir_or_none)
    """
    base = Path(config.output_dir)

    if smart_workspace:
        # Extract and sanitize domain for filesystem use
        netloc = urlparse(config.start_url).netloc or "unknown"
        domain = re.sub(r"[^\w.\-]", "_", netloc)
        environment = re.sub(r"[^\w.\-]", "_", config.environment or "dev")
        workspace = base / domain / environment
        timestamp = now.strftime("%Y-%m-%d_%H.%M.%S")
        run_dir = workspace / "runs" / timestamp
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir, workspace

    # Legacy hierarchical layout
    run_dir = (
        base
        / now.strftime("%Y")
        / now.strftime("%m.%B")
        / now.strftime("%d-%m-%Y")
        / now.strftime("%H.%M.%S")
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir, None


async def _run_exploration(
    config: ExplorerConfig,
    *,
    generate_tests: bool = False,
    test_framework: str = "pytest",
    generate_bdd: bool = False,
    generate_narrative: bool = False,
    db_path: str = DEFAULT_DB_PATH,
    save_to_db: bool = True,
    auth_bootstrap: AuthBootstrap | None = None,
    auth_profile_summary: dict[str, Any] | None = None,
) -> None:
    """Run the exploration."""
    # Configure logging
    log_dir = Path(".flowscout")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_level = logging.DEBUG if config.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_dir / "debug.log", mode="a")],
        force=True,
    )
    if config.verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(name)s: %(message)s"))
        logging.getLogger("flowscout").addHandler(console_handler)

    now = datetime.now(timezone.utc)
    use_smart_workspace = True
    run_dir, workspace_dir = _build_output_dirs(
        config,
        now,
        smart_workspace=use_smart_workspace,
    )
    if config.take_screenshots:
        evidence_dir = run_dir / "evidence" / "actions"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        config.evidence_dir = str(evidence_dir)

    browser = BrowserManager(config)
    graph = ExplorationGraph()
    terminal = TerminalReporter(verbose=config.verbose)

    navigator = Navigator(
        browser=browser,
        graph=graph,
        config=config,
        terminal=terminal,
    )

    db: FlowscoutDB | None = None
    try:
        await browser.launch()
        if auth_bootstrap is not None:
            console.print(
                "  [cyan]Applying auth profile:[/cyan] "
                f"{auth_bootstrap.profile_name} (credentials from environment variables)",
            )
            await browser.apply_auth_bootstrap(auth_bootstrap)
        result = await navigator.explore(config.start_url)
        if auth_profile_summary is not None:
            result.config["auth"] = auth_profile_summary

        # Generate HTML report
        report_path = str(run_dir / "report.html")
        reporter = HTMLReporter()
        reporter.generate(result, report_path)
        console.print(f"\n  [green]Report saved:[/green] {report_path}")

        # Save JSON
        json_path = str(run_dir / "result.json")
        Path(json_path).write_text(result.model_dump_json(indent=2))
        console.print(f"  [green]JSON saved:[/green] {json_path}")

        # Save to database
        if save_to_db:
            db = FlowscoutDB(db_path)
            run_id = db.save_run(result)
            console.print(f"  [green]DB saved:[/green] {db_path} (run: {run_id})")

            # Show cross-run insights if we have history
            _print_cross_run_insights(db, run_id, config.start_url)

        # Generate tests
        if generate_tests:
            ext = ".py" if test_framework == "pytest" else ".spec.ts"
            test_path = str(run_dir / f"tests{ext}")
            generate_test_suite(result, test_path, framework=test_framework)
            console.print(f"  [green]Tests generated:[/green] {test_path}")

        # Generate POM classes + POM-based tests when smart mode is on
        if config.smart_mode and generate_tests and result.page_catalogs:
            from flowscout.codegen.page_objects import generate_page_objects
            from flowscout.codegen.pom_tests import generate_pom_tests

            pom_dir = str((workspace_dir or run_dir) / "pages")
            pom_paths = generate_page_objects(
                result.page_catalogs,
                pom_dir,
                framework=test_framework,
                base_url=config.start_url,
            )
            if pom_paths:
                console.print(
                    f"  [green]POM classes generated:[/green] {len(pom_paths)} files in {pom_dir}"
                )

                pom_ext = ".py" if test_framework == "pytest" else ".spec.ts"
                pom_test_path = str(run_dir / f"pom_tests{pom_ext}")
                generate_pom_tests(
                    result,
                    result.page_catalogs,
                    pom_test_path,
                    framework=test_framework,
                )
                console.print(f"  [green]POM tests generated:[/green] {pom_test_path}")

        # Generate BDD feature file
        if generate_bdd:
            from flowscout.codegen.bdd import generate_feature_file

            feature_path = str(run_dir / "exploration.feature")
            generate_feature_file(result, feature_path)
            console.print(f"  [green]Feature file:[/green] {feature_path}")

        # Generate narrative report
        if generate_narrative:
            from flowscout.codegen.bdd import generate_markdown_report

            md_path = str(run_dir / "report.md")
            generate_markdown_report(result, md_path)
            console.print(f"  [green]Narrative report:[/green] {md_path}")

        # Build site model (when smart mode data is available)
        if config.smart_mode and result.smart_analyses:
            from flowscout.analysis.archetype import PageAnalysis
            from flowscout.analysis.site_model import SiteModelBuilder

            analyses = {
                sid: PageAnalysis.model_validate(data)
                for sid, data in result.smart_analyses.items()
            }

            builder = SiteModelBuilder()
            site_model = builder.build(result, analyses)

            # Save site model JSON
            model_path = str(run_dir / "site_model.json")
            Path(model_path).write_text(site_model.model_dump_json(indent=2))
            console.print(f"  [green]Site model saved:[/green] {model_path}")

            # Print site model summary
            terminal.print_site_model_summary(site_model)

            # Generate scenario-based tests (POMs are a prerequisite)
            if generate_tests and result.page_catalogs:
                from flowscout.codegen.scenario_tests import generate_scenario_tests

                scenario_ext = ".py" if test_framework == "pytest" else ".spec.ts"
                scenario_test_path = str(
                    (workspace_dir or run_dir) / f"scenario_tests{scenario_ext}"
                )
                generate_scenario_tests(
                    site_model,
                    scenario_test_path,
                    framework=test_framework,
                    base_url=config.start_url,
                )
                console.print(
                    f"  [green]Scenario tests generated:[/green] {scenario_test_path}"
                )

        # Update workspace symlink and print workspace path
        if workspace_dir:
            latest_link = workspace_dir / "latest"
            if latest_link.is_symlink() or latest_link.exists():
                latest_link.unlink()
            latest_link.symlink_to(run_dir.resolve(), target_is_directory=True)
            console.print(f"\n  [bold cyan]Workspace:[/bold cyan] {workspace_dir}")

        # Print smart mode summary
        if config.smart_mode and result.archetypes:
            console.print("\n  [bold magenta]Smart Mode Summary[/bold magenta]")
            for arch, count in sorted(result.archetypes.items()):
                console.print(f"    @ {arch}: {count} instances")
            if result.coverage:
                features = result.coverage.get("features_tested", [])
                if features:
                    console.print(f"    Features: {', '.join(features)}")

        # Print verdict summary
        pass_count = sum(1 for r in result.results if r.verdict == "pass")
        fail_count = sum(1 for r in result.results if r.verdict == "fail")
        if pass_count or fail_count:
            console.print(
                f"\n  Verdict: [green]{pass_count} passed[/green], [red]{fail_count} failed[/red]"
            )

    except KeyboardInterrupt:
        console.print("\n  [yellow]Interrupted by user[/yellow]")
    except Exception as exc:
        console.print(f"\n  [red]Error:[/red] {exc}")
        raise
    finally:
        await browser.close()
        if db:
            db.close()


def _print_cross_run_insights(db: FlowscoutDB, run_id: str, start_url: str) -> None:
    """Print cross-run insights if we have prior runs."""
    runs = db.list_runs(start_url=start_url)
    if len(runs) < 2:
        return

    console.print()

    # New states
    new_states = db.get_new_states_since(run_id)
    if new_states:
        console.print(f"  [cyan]New states this run:[/cyan] {len(new_states)}")
        for s in new_states[:5]:
            console.print(f"    [green]+[/green] {s['title'] or s['url']}")

    # Disappeared states
    disappeared = db.get_disappeared_states(run_id)
    if disappeared:
        console.print(
            f"  [yellow]States missing vs previous:[/yellow] {len(disappeared)}"
        )
        for s in disappeared[:5]:
            console.print(f"    [red]-[/red] {s['title'] or s['url']}")

    # Flaky actions
    flaky = db.get_flaky_actions(start_url)
    if flaky:
        console.print(
            f"  [yellow]Flaky actions (inconsistent outcomes):[/yellow] {len(flaky)}"
        )
        for f in flaky[:3]:
            console.print(
                f"    [yellow]~[/yellow] {f['label']} — outcomes: {f['outcomes_seen']}"
            )


def _compute_benchmark_metrics(
    result: ExplorationResult,
    *,
    low_confidence_threshold: float = DEFAULT_LOW_CONFIDENCE_THRESHOLD,
) -> dict[str, int | float | bool]:
    """Compute key v1 benchmark metrics from an exploration result."""
    all_urls = {state.url for state in result.states.values()}
    tested_urls: set[str] = set()
    for action_result in result.results:
        source = result.states.get(action_result.source_state_id)
        target = result.states.get(action_result.target_state_id)
        if source:
            tested_urls.add(source.url)
        if target:
            tested_urls.add(target.url)

    executed_ids = {action_result.action_id for action_result in result.results}
    total_discovered_actions = len(result.actions)
    confidence_samples = [
        action_result.confidence
        for action_result in result.results
        if action_result.confidence > 0 or action_result.confidence_reason
    ]
    avg_confidence = sum(confidence_samples) / max(len(confidence_samples), 1)
    low_confidence_count = sum(
        1 for score in confidence_samples if score < low_confidence_threshold
    )

    page_coverage_pct = round(len(tested_urls) / max(len(all_urls), 1) * 100)
    action_coverage_pct = round(
        len(executed_ids) / max(total_discovered_actions, 1) * 100
    )
    inventory = (
        result.element_inventory if isinstance(result.element_inventory, dict) else {}
    )
    interactive_elements = int(inventory.get("interactive_elements", 0))
    non_interactive_elements = int(inventory.get("non_interactive_elements", 0))
    total_catalog_elements = int(inventory.get("total_elements", 0))
    interactive_mix_pct = round(
        interactive_elements / max(total_catalog_elements, 1) * 100
    )

    return {
        "duration_seconds": result.duration_seconds,
        "total_states": result.stats.get("total_states", len(result.states)),
        "total_actions_executed": result.stats.get(
            "total_actions_executed",
            len(result.results),
        ),
        "total_unique_actions": result.stats.get(
            "total_unique_actions",
            len(result.actions),
        ),
        "page_coverage_pct": page_coverage_pct,
        "action_coverage_pct": action_coverage_pct,
        "confidence_sample_count": len(confidence_samples),
        "low_confidence_transitions": low_confidence_count,
        "avg_transition_confidence": round(avg_confidence, 3),
        "coverage_target_met": page_coverage_pct >= 80,
        "interactive_elements": interactive_elements,
        "non_interactive_elements": non_interactive_elements,
        "total_catalog_elements": total_catalog_elements,
        "interactive_mix_pct": interactive_mix_pct,
    }


@main.command()
@click.argument("report_path", type=click.Path(exists=True))
def serve(report_path: str) -> None:
    """Open an HTML report in the browser."""
    abs_path = os.path.abspath(report_path)
    console.print(f"  Opening {abs_path}")
    webbrowser.open(f"file://{abs_path}")


@main.command()
@click.option("--url", "-u", default=None, help="Filter by start URL.")
@click.option("--limit", "-n", default=20, help="Maximum runs to show.")
@click.option("--db-path", default=DEFAULT_DB_PATH, help="SQLite database path.")
def history(url: str | None, limit: int, db_path: str) -> None:
    """Show exploration history from the database."""
    db = FlowscoutDB(db_path)
    try:
        runs = db.list_runs(start_url=url, limit=limit)
        if not runs:
            console.print("  [dim]No runs found[/dim]")
            return

        table = Table(title="Exploration History", border_style="cyan")
        table.add_column("Run ID", style="bold cyan")
        table.add_column("URL", max_width=50)
        table.add_column("Started", style="dim")
        table.add_column("Duration", justify="right")
        table.add_column("States", justify="right")
        table.add_column("Actions", justify="right")
        table.add_column("Flows", justify="right")

        for run in runs:
            table.add_row(
                run["run_id"],
                run["start_url"][:50],
                run["started_at"][:19],
                f"{run['duration_seconds']:.1f}s",
                str(run["total_states"]),
                str(run["total_actions"]),
                str(run["total_flows"]),
            )

        console.print(table)
    finally:
        db.close()


@main.command()
@click.option("--url", "-u", required=True, help="Start URL to analyze.")
@click.option("--db-path", default=DEFAULT_DB_PATH, help="SQLite database path.")
def reliability(url: str, db_path: str) -> None:
    """Show action reliability across runs."""
    db = FlowscoutDB(db_path)
    try:
        actions = db.get_action_reliability(start_url=url)
        if not actions:
            console.print("  [dim]No data found[/dim]")
            return

        table = Table(title=f"Action Reliability — {url}", border_style="cyan")
        table.add_column("Action", max_width=50)
        table.add_column("Attempts", justify="right")
        table.add_column("Nav", justify="right", style="green")
        table.add_column("DOM", justify="right", style="yellow")
        table.add_column("Errors", justify="right", style="red")
        table.add_column("No Change", justify="right", style="dim")

        for a in actions:
            table.add_row(
                a["label"][:50],
                str(a["total_attempts"]),
                str(a["navigations"]),
                str(a["dom_changes"]),
                str(a["errors"]),
                str(a["no_changes"]),
            )

        console.print(table)

        # Flaky actions
        flaky = db.get_flaky_actions(url)
        if flaky:
            console.print()
            flaky_table = Table(title="Flaky Actions", border_style="yellow")
            flaky_table.add_column("Action", max_width=50)
            flaky_table.add_column("Runs Seen", justify="right")
            flaky_table.add_column("Outcomes")

            for f in flaky:
                flaky_table.add_row(
                    f["label"][:50],
                    str(f["runs_seen"]),
                    f["outcomes_seen"],
                )

            console.print(flaky_table)
    finally:
        db.close()


@main.command()
@click.argument("json_path", type=click.Path(exists=True))
@click.option("--db-path", default=DEFAULT_DB_PATH, help="SQLite database path.")
@click.option(
    "--low-confidence-threshold",
    default=DEFAULT_LOW_CONFIDENCE_THRESHOLD,
    show_default=True,
    help="Threshold for counting low-confidence transitions.",
)
def benchmark(json_path: str, db_path: str, low_confidence_threshold: float) -> None:
    """Summarize benchmark metrics from a result artifact."""
    data = json.loads(Path(json_path).read_text())
    result = ExplorationResult.model_validate(data)
    metrics = _compute_benchmark_metrics(
        result,
        low_confidence_threshold=low_confidence_threshold,
    )

    table = Table(title="V1 Benchmark Snapshot", border_style="cyan")
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", justify="right")
    table.add_row("Result file", json_path)
    table.add_row("Duration (seconds)", f"{metrics['duration_seconds']:.2f}")
    table.add_row("States discovered", str(metrics["total_states"]))
    table.add_row("Actions executed", str(metrics["total_actions_executed"]))
    table.add_row("Unique actions discovered", str(metrics["total_unique_actions"]))
    table.add_row("Page coverage %", f"{metrics['page_coverage_pct']}%")
    table.add_row("Action coverage %", f"{metrics['action_coverage_pct']}%")
    if metrics["total_catalog_elements"]:
        table.add_row("Interactive elements", str(metrics["interactive_elements"]))
        table.add_row(
            "Content elements",
            str(metrics["non_interactive_elements"]),
        )
        table.add_row("Interactive mix %", f"{metrics['interactive_mix_pct']}%")
    if metrics["confidence_sample_count"]:
        table.add_row(
            "Avg transition confidence",
            f"{metrics['avg_transition_confidence']:.3f}",
        )
        table.add_row(
            f"Low-confidence transitions (< {low_confidence_threshold:.2f})",
            str(metrics["low_confidence_transitions"]),
        )
    else:
        table.add_row("Avg transition confidence", "n/a (legacy artifact)")
        table.add_row(
            f"Low-confidence transitions (< {low_confidence_threshold:.2f})",
            "n/a (legacy artifact)",
        )
    table.add_row(
        "Coverage target (>=80%)",
        "PASS" if metrics["coverage_target_met"] else "FAIL",
    )

    start_url = result.config.get("start_url", "")
    if start_url and Path(db_path).exists():
        db = FlowscoutDB(db_path)
        try:
            flaky_count = len(db.get_flaky_actions(start_url))
        finally:
            db.close()
        table.add_row("Flaky actions (history)", str(flaky_count))
    elif start_url:
        table.add_row("Flaky actions (history)", "n/a (db missing)")

    console.print(table)


@main.command()
@click.argument("json_path", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output test file path.")
@click.option(
    "--framework",
    type=click.Choice(["pytest", "playwright", "bdd"]),
    default="pytest",
    help="Test framework (pytest, playwright, or bdd for Gherkin output).",
)
@click.option(
    "--site-model",
    is_flag=True,
    help="Generate site model and scenario tests from result.",
)
def generate(
    json_path: str,
    output: str | None,
    framework: str,
    site_model: bool,
) -> None:
    """Generate test suite from a JSON exploration result."""
    data = json.loads(Path(json_path).read_text())
    result = ExplorationResult.model_validate(data)

    if site_model and result.smart_analyses:
        from flowscout.analysis.archetype import PageAnalysis
        from flowscout.analysis.site_model import SiteModelBuilder
        from flowscout.codegen.scenario_tests import generate_scenario_tests
        from flowscout.reporting.terminal import TerminalReporter

        analyses = {
            sid: PageAnalysis.model_validate(d)
            for sid, d in result.smart_analyses.items()
        }
        builder = SiteModelBuilder()
        model = builder.build(result, analyses)

        # Save site model
        model_output = json_path.replace(".json", "_site_model.json")
        Path(model_output).write_text(model.model_dump_json(indent=2))
        console.print(f"  [green]Site model generated:[/green] {model_output}")

        # Print summary
        terminal = TerminalReporter()
        terminal.print_site_model_summary(model)

        # Generate scenario tests
        test_framework = "pytest" if framework != "playwright" else "playwright"
        ext = ".py" if test_framework == "pytest" else ".spec.ts"
        test_output = output or json_path.replace(".json", f"_scenario_tests{ext}")
        generate_scenario_tests(
            model,
            test_output,
            framework=test_framework,
            base_url=result.config.get("start_url", ""),
        )
        console.print(f"  [green]Scenario tests generated:[/green] {test_output}")

        # Also generate POMs if catalogs available
        if result.page_catalogs:
            from flowscout.codegen.page_objects import generate_page_objects

            pom_dir = str(Path(json_path).parent / "pages")
            pom_paths = generate_page_objects(
                result.page_catalogs,
                pom_dir,
                framework=test_framework,
                base_url=result.config.get("start_url", ""),
            )
            if pom_paths:
                console.print(
                    f"  [green]POM classes generated:[/green] {len(pom_paths)} files in {pom_dir}"
                )
        return

    if framework == "bdd":
        from flowscout.codegen.bdd import generate_feature_file

        if output is None:
            output = json_path.replace(".json", ".feature")
        generate_feature_file(result, output)
        console.print(f"  [green]Feature file generated:[/green] {output}")
    else:
        if output is None:
            ext = ".py" if framework == "pytest" else ".spec.ts"
            output = json_path.replace(".json", f"_tests{ext}")
        generate_test_suite(result, output, framework=framework)
        console.print(f"  [green]Tests generated:[/green] {output}")

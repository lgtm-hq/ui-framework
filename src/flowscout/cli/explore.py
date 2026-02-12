"""Explore command — main exploration entry point."""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import click

from flowscout.analysis.graph import ExplorationGraph
from flowscout.cli.app import (
    DEFAULT_AUTH_CONFIG_PATH,
    DEFAULT_CRAWL_CONFIG_PATH,
    DEFAULT_DB_PATH,
    console,
    main,
)
from flowscout.cli.config import (
    _came_from_cli,
    _coerce_bool,
    _find_config_value,
    _load_crawl_config,
    _resolve_auth_bootstrap,
    _resolve_bool_config,
    _resolve_bool_option,
    _resolve_int_config,
    _resolve_int_option,
    _resolve_str_option,
    _resolve_domain_scoped_config,
)
from flowscout.codegen.playwright_tests import generate_test_suite
from flowscout.core.auth import AuthBootstrap
from flowscout.core.browser import BrowserManager
from flowscout.core.navigator import Navigator
from flowscout.core.policy import ActionPolicyConfig
from flowscout.core.state import ExplorerConfig, ExplorationStrategy, InputProfile
from flowscout.plugins import PluginRegistry
from flowscout.reporting.html import HTMLReporter
from flowscout.reporting.terminal import TerminalReporter
from flowscout.storage.db import FlowscoutDB


@main.command()  # type: ignore[untyped-decorator]  # Click decorators are untyped
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
    help="Generate POM classes and scenario tests from results.",
)
@click.option(
    "--legacy",
    is_flag=True,
    help="Generate legacy flat tests (deprecated escape hatch).",
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
    "--smart/--no-smart",
    default=True,
    show_default=True,
    help=(
        "Enable smart mode: archetype recognition,"
        " contextual input, coverage-aware exploration."
    ),
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
    help=(
        "Explicit auth profile name."
        " If omitted, profile is auto-selected"
        " by domain/environment."
    ),
)
@click.option(
    "--auth-required/--no-auth-required",
    default=False,
    help="Fail fast if auth profile or credentials are missing.",
)
@click.option(
    "--reporter",
    default="html",
    help="Reporter plugin name (default: html). Use 'list' to see available reporters.",
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
    legacy: bool,
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
    reporter: str,
) -> None:
    """Explore a web application starting from URL."""
    # Load plugin registry and register built-in reporter
    plugin_registry = PluginRegistry()
    plugin_registry.register_reporter("html", HTMLReporter)
    plugin_registry.load_from_entry_points()

    if reporter == "list":
        console.print("[bold]Available reporters:[/bold]")
        for name in plugin_registry.list_reporters():
            console.print(f"  - {name}")
        return
    ctx = click.get_current_context()
    raw_crawl_config = _load_crawl_config(config_file=config_file)
    crawl_config = _resolve_domain_scoped_config(
        ctx=ctx,
        start_url=url,
        cli_environment=environment,
        config=raw_crawl_config,
    )

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
    default_smart_stop_on_saturation = bool(
        ExplorerConfig.model_fields["smart_stop_on_saturation"].default,
    )
    default_smart_min_features_before_stop = int(
        ExplorerConfig.model_fields["smart_min_features_before_stop"].default,
    )
    default_smart_min_archetypes_before_stop = int(
        ExplorerConfig.model_fields["smart_min_archetypes_before_stop"].default,
    )
    default_smart_archetype_instance_limit = int(
        ExplorerConfig.model_fields["smart_archetype_instance_limit"].default,
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
    resolved_smart_stop_on_saturation = _resolve_bool_config(
        config=crawl_config,
        config_keys=("smart_stop_on_saturation",),
        default=default_smart_stop_on_saturation,
    )
    resolved_smart_min_features_before_stop = _resolve_int_config(
        config=crawl_config,
        config_keys=("smart_min_features_before_stop", "smart_min_features"),
        default=default_smart_min_features_before_stop,
    )
    resolved_smart_min_archetypes_before_stop = _resolve_int_config(
        config=crawl_config,
        config_keys=("smart_min_archetypes_before_stop", "smart_min_archetypes"),
        default=default_smart_min_archetypes_before_stop,
    )
    resolved_smart_archetype_instance_limit = _resolve_int_config(
        config=crawl_config,
        config_keys=("smart_archetype_instance_limit",),
        default=default_smart_archetype_instance_limit,
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
        smart_stop_on_saturation=resolved_smart_stop_on_saturation,
        smart_min_features_before_stop=resolved_smart_min_features_before_stop,
        smart_min_archetypes_before_stop=resolved_smart_min_archetypes_before_stop,
        smart_archetype_instance_limit=resolved_smart_archetype_instance_limit,
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
            generate_legacy=legacy,
            test_framework=test_framework,
            generate_bdd=bdd,
            generate_narrative=narrative,
            db_path=resolved_db_path,
            save_to_db=save_to_db,
            auth_bootstrap=auth_bootstrap,
            auth_profile_summary=auth_profile_summary,
            plugin_registry=plugin_registry,
            reporter_name=reporter,
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
        timestamp = now.strftime("%Y-%m-%d_%H.%M.%S.%f")
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
    generate_legacy: bool = False,
    test_framework: str = "pytest",
    generate_bdd: bool = False,
    generate_narrative: bool = False,
    db_path: str = DEFAULT_DB_PATH,
    save_to_db: bool = True,
    auth_bootstrap: AuthBootstrap | None = None,
    auth_profile_summary: dict[str, Any] | None = None,
    plugin_registry: PluginRegistry | None = None,
    reporter_name: str = "html",
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
                f"{auth_bootstrap.profile_name}"
                " (credentials from environment variables)",
            )
            await browser.apply_auth_bootstrap(auth_bootstrap)
        result = await navigator.explore(config.start_url)
        if auth_profile_summary is not None:
            result.config["auth"] = auth_profile_summary

        # Generate report
        report_path = str(run_dir / "report.html")
        if plugin_registry is not None:
            reporter_cls = plugin_registry.get_reporter(reporter_name)
        else:
            reporter_cls = HTMLReporter if reporter_name == "html" else None
        if reporter_cls is None:
            available = (
                ", ".join(plugin_registry.list_reporters())
                if plugin_registry
                else "html"
            )
            console.print(
                f"[red]Unknown reporter '{reporter_name}'. Available: {available}[/red]"
            )
        else:
            reporter_instance = reporter_cls()
            reporter_instance.generate(result, report_path)
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

        generated_primary_tests = False

        # Generate legacy flat tests (deprecated escape hatch)
        if generate_tests and generate_legacy:
            ext = ".py" if test_framework == "pytest" else ".spec.ts"
            test_path = str(run_dir / f"tests{ext}")
            generate_test_suite(result, test_path, framework=test_framework)
            console.print(
                f"  [yellow]Legacy tests generated (deprecated):[/yellow] {test_path}"
            )

        # Generate POM classes by default when smart mode is on.
        if (
            config.smart_mode
            and generate_tests
            and not generate_legacy
            and result.page_catalogs
        ):
            from flowscout.codegen.page_objects import generate_page_objects

            pom_dir = str((workspace_dir or run_dir) / "pages")
            pom_paths = generate_page_objects(
                result.page_catalogs,
                pom_dir,
                framework=test_framework,
                base_url=config.start_url,
            )
            if pom_paths:
                console.print(
                    "  [green]POM classes generated:"
                    f"[/green] {len(pom_paths)}"
                    f" files in {pom_dir}"
                )

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
            if generate_tests and not generate_legacy and result.page_catalogs:
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
                generated_primary_tests = True

        if generate_tests and (not generate_legacy) and (not generated_primary_tests):
            console.print(
                "  [yellow]Unable to generate scenario tests from this run."
                " Use --legacy for flat test output.[/yellow]"
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

        # Print stability summary
        stability_scores = [
            float(action_result.stability_score or 0.0)
            for action_result in result.results
        ]
        if stability_scores:
            avg_stability = sum(stability_scores) / len(stability_scores)
            stable_steps = sum(1 for score in stability_scores if score >= 0.7)
            unstable_steps = len(stability_scores) - stable_steps
            console.print(
                "\n  Stability: "
                f"[cyan]{avg_stability:.2f} avg[/cyan], "
                f"[green]{stable_steps} stable[/green], "
                f"[yellow]{unstable_steps} unstable[/yellow]"
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

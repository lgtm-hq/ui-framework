"""CLI entry point for flowscout."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import click
from rich.console import Console
from rich.table import Table

from flowscout import __version__
from flowscout.analysis.graph import ExplorationGraph, ExplorationResult
from flowscout.codegen.playwright_tests import generate_test_suite
from flowscout.core.browser import BrowserManager
from flowscout.core.navigator import Navigator
from flowscout.core.state import ExplorerConfig, ExplorationStrategy
from flowscout.reporting.html import HTMLReporter
from flowscout.reporting.terminal import TerminalReporter
from flowscout.storage.db import FlowscoutDB

console = Console()

DEFAULT_DB_PATH = ".flowscout/history.db"


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
    "--screenshot/--no-screenshot",
    default=False,
    help="Take screenshots of each state.",
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
def explore(
    url: str,
    max_depth: int,
    max_states: int,
    max_actions: int,
    headless: bool,
    timeout: int,
    output_dir: str,
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
) -> None:
    """Explore a web application starting from URL."""
    config = ExplorerConfig(
        start_url=url,
        max_depth=max_depth,
        max_states=max_states,
        max_actions_per_state=max_actions,
        headless=headless,
        timeout_ms=timeout,
        output_dir=output_dir,
        take_screenshots=screenshot,
        strategy=ExplorationStrategy(strategy),
        verbose=verbose,
        smart_mode=smart,
    )

    asyncio.run(
        _run_exploration(
            config,
            generate_tests=generate_tests,
            test_framework=test_framework,
            generate_bdd=bdd,
            generate_narrative=narrative,
            db_path=db_path,
            save_to_db=not no_db,
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
        workspace = base / domain
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
        result = await navigator.explore(config.start_url)

        now = datetime.now(timezone.utc)
        use_smart_workspace = config.smart_mode and generate_tests
        run_dir, workspace_dir = _build_output_dirs(
            config, now, smart_workspace=use_smart_workspace,
        )

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
            console.print(
                f"\n  [bold cyan]Workspace:[/bold cyan] {workspace_dir}"
            )

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
    json_path: str, output: str | None, framework: str, site_model: bool,
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
            model, test_output, framework=test_framework, base_url=result.config.get("start_url", ""),
        )
        console.print(f"  [green]Scenario tests generated:[/green] {test_output}")

        # Also generate POMs if catalogs available
        if result.page_catalogs:
            from flowscout.codegen.page_objects import generate_page_objects

            pom_dir = str(Path(json_path).parent / "pages")
            pom_paths = generate_page_objects(
                result.page_catalogs, pom_dir, framework=test_framework,
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

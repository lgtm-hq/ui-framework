"""Generate command — create test suites from exploration results."""

from __future__ import annotations

import json
from pathlib import Path

import click

from flowscout.analysis.graph import ExplorationResult
from flowscout.cli.app import console, main
from flowscout.codegen.playwright_tests import generate_test_suite


@main.command()  # type: ignore[untyped-decorator]  # Click decorators are untyped
@click.argument("json_path", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output test file path.")
@click.option(
    "--framework",
    type=click.Choice(["pytest", "playwright", "bdd"]),
    default="pytest",
    help="Test framework (pytest, playwright, or bdd for Gherkin output).",
)
@click.option(
    "--format",
    "export_format",
    type=click.Choice(["tests", "markdown", "junit"]),
    default="tests",
    help="Output format: tests (default), markdown summary, or JUnit XML.",
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
    export_format: str,
    site_model: bool,
) -> None:
    """Generate test suite from a JSON exploration result."""
    data = json.loads(Path(json_path).read_text())
    result = ExplorationResult.model_validate(data)

    # Handle non-test export formats first
    if export_format == "markdown":
        from flowscout.reporting.markdown_export import generate_markdown_report

        md_output = output or json_path.replace(".json", "_report.md")
        generate_markdown_report(result, md_output)
        console.print(f"  [green]Markdown report generated:[/green] {md_output}")
        return

    if export_format == "junit":
        from flowscout.reporting.junit_export import generate_junit_report

        junit_output = output or json_path.replace(".json", "_junit.xml")
        generate_junit_report(result, junit_output)
        console.print(f"  [green]JUnit XML generated:[/green] {junit_output}")
        return

    if site_model and framework == "bdd":
        raise click.ClickException(
            "--site-model does not support framework 'bdd'. Use pytest or playwright.",
        )

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
                    "  [green]POM classes generated:"
                    f"[/green] {len(pom_paths)}"
                    f" files in {pom_dir}"
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

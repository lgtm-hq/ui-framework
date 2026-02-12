"""Generate command — create artifacts from exploration or site models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import click

from flowscout.analysis.graph import ExplorationResult
from flowscout.cli.app import console, main
from flowscout.codegen.playwright_tests import generate_test_suite
from flowscout.modeling.site_model import SiteModel


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
    help=(
        "Build a SiteModel from ExplorationResult before generating tests."
        " Deprecated: SiteModel JSON input is auto-detected."
    ),
)
def generate(
    json_path: str,
    output: str | None,
    framework: str,
    export_format: str,
    site_model: bool,
) -> None:
    """Generate artifacts from JSON input.

    Args:
        json_path: Path to either ExplorationResult JSON or SiteModel JSON.
        output: Output path for generated artifact(s).
        framework: Target framework.
        export_format: Export format.
        site_model: Force building a SiteModel from ExplorationResult input.
    """
    data = json.loads(Path(json_path).read_text())
    if site_model and framework == "bdd":
        raise click.ClickException(
            "--site-model does not support framework 'bdd'. Use pytest or playwright.",
        )

    # SiteModel input is auto-detected for Layer 3 generation.
    if _looks_like_site_model_payload(data=data):
        model = SiteModel.model_validate(data)
        _generate_from_site_model(
            model=model,
            json_path=json_path,
            output=output,
            framework=framework,
            export_format=export_format,
        )
        return

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

    if site_model:
        model = SiteModel.from_exploration_result(result=result)
        _generate_from_site_model(
            model=model,
            json_path=json_path,
            output=output,
            framework=framework,
            export_format=export_format,
            base_url=result.config.get("start_url", ""),
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


def _looks_like_site_model_payload(*, data: Any) -> bool:
    """Detect whether payload shape looks like SiteModel JSON."""
    if not isinstance(data, dict):
        return False
    return any(
        key in data
        for key in ("page_types", "navigation_edges", "test_scenarios", "summary")
    )


def _resolve_site_model_outputs(
    *,
    json_path: str,
    output: str | None,
    framework: str,
) -> tuple[str, Path]:
    """Resolve scenario-test output file and POM directory for SiteModel generation."""
    ext = ".py" if framework == "pytest" else ".spec.ts"

    if output is None:
        test_output = Path(json_path).with_name(
            f"{Path(json_path).stem}_scenario_tests{ext}",
        )
        pom_dir = test_output.parent / "pages"
        return str(test_output), pom_dir

    output_path = Path(output)
    if output_path.suffix == "" or output.endswith("/"):
        output_path.mkdir(parents=True, exist_ok=True)
        return str(output_path / f"scenario_tests{ext}"), output_path / "pages"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    return str(output_path), output_path.parent / "pages"


def _infer_model_base_url(*, model: SiteModel) -> str:
    """Infer base URL from representative page URLs in the model."""
    for page_type in model.page_types:
        if not page_type.representative_url:
            continue
        parsed = urlparse(page_type.representative_url)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"
    return ""


def _generate_from_site_model(
    *,
    model: SiteModel,
    json_path: str,
    output: str | None,
    framework: str,
    export_format: str,
    base_url: str = "",
) -> None:
    """Generate Layer 3 artifacts from a SiteModel."""
    if export_format != "tests":
        raise click.ClickException(
            "SiteModel input supports only '--format tests'.",
        )
    if framework == "bdd":
        raise click.ClickException(
            "--site-model does not support framework 'bdd'. Use pytest or playwright.",
        )

    from flowscout.codegen.page_objects import generate_page_objects
    from flowscout.codegen.scenario_tests import generate_scenario_tests
    from flowscout.reporting.terminal import TerminalReporter

    test_output, pom_dir = _resolve_site_model_outputs(
        json_path=json_path,
        output=output,
        framework=framework,
    )
    pom_dir.mkdir(parents=True, exist_ok=True)

    model_base_url = base_url or _infer_model_base_url(model=model)
    catalogs = {
        page_type.page_type_id: page_type.catalog
        for page_type in model.page_types
        if page_type.catalog.entries
    }
    if catalogs:
        pom_paths = generate_page_objects(
            catalogs=catalogs,
            output_dir=str(pom_dir),
            framework=framework,
            base_url=model_base_url,
            shared_components=model.shared_components,
        )
        if pom_paths:
            console.print(
                "  [green]POM classes generated:"
                f"[/green] {len(pom_paths)} files in {pom_dir}",
            )

    generate_scenario_tests(
        site_model=model,
        output_path=test_output,
        framework=framework,
        base_url=model_base_url,
    )
    console.print(f"  [green]Scenario tests generated:[/green] {test_output}")

    terminal = TerminalReporter()
    terminal.print_site_model_summary(model)

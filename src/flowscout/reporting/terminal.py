"""Rich terminal output for live exploration progress."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from flowscout.analysis.expectations import ExpectationResult
    from flowscout.analysis.graph import ExplorationResult
    from flowscout.modeling.site_model import SiteModel
    from flowscout.core.state import ExplorerConfig, PageState
    from flowscout.discovery.actions import Action, ActionResult

# Outcome → (icon, color)
_OUTCOME_STYLE: dict[str, tuple[str, str]] = {
    "navigation": ("->", "green"),
    "dom_change": ("~", "yellow"),
    "visual_change": ("~", "cyan"),
    "no_change": (".", "dim"),
    "validation_error": ("!", "red"),
    "network_error": ("!!", "red bold"),
    "console_error": ("!!", "red"),
    "timeout": ("T", "red"),
    "exception": ("X", "red bold"),
}


class TerminalReporter:
    """Live terminal output using Rich."""

    def __init__(self, *, verbose: bool = False) -> None:
        self.console = Console()
        self.verbose = verbose

    def print_banner(self, url: str, config: ExplorerConfig) -> None:
        """Print startup banner with configuration summary."""
        lines = [
            f"[bold]URL:[/bold] {url}",
            f"[bold]Strategy:[/bold] {config.strategy.value}",
            f"[bold]Max depth:[/bold] {config.max_depth}",
            f"[bold]Max states:[/bold] {config.max_states}",
            f"[bold]Max actions/state:[/bold] {config.max_actions_per_state}",
            f"[bold]Headless:[/bold] {config.headless}",
            f"[bold]Screenshots:[/bold] {config.take_screenshots}",
            f"[bold]Input profile:[/bold] {config.input_profile.value}",
        ]
        if config.smart_mode:
            lines.extend(
                [
                    "[bold magenta]Smart mode:[/bold magenta] ON",
                    (
                        "[magenta]  Saturation stop:[/magenta]"
                        f" {'ON' if config.smart_stop_on_saturation else 'OFF'}"
                    ),
                    (
                        "[magenta]  Min archetypes:[/magenta]"
                        f" {config.smart_min_archetypes_before_stop}"
                    ),
                    (
                        "[magenta]  Min features:[/magenta]"
                        f" {config.smart_min_features_before_stop}"
                    ),
                    (
                        "[magenta]  Signature repeat limit:"
                        f"[/magenta] {config.smart_archetype_instance_limit}"
                    ),
                ]
            )
        panel = Panel(
            "\n".join(lines),
            title="[bold cyan]flowscout[/bold cyan]",
            subtitle="LLM-free web path exploration",
            border_style="cyan",
        )
        self.console.print(panel)
        self.console.print()

    def log_state_discovered(self, state: PageState, *, is_new: bool) -> None:
        """Log when a state is discovered."""
        if is_new:
            self.console.print(
                f"  [green]+[/green] New state [bold]{state.state_id[:8]}[/bold]: "
                f"{state.title or 'untitled'} [dim]({state.url})[/dim]",
            )
        elif self.verbose:
            self.console.print(f"  [dim]= Known state {state.state_id[:8]}[/dim]")

    def log_action_start(self, action: Action, state_id: str) -> None:
        """Log when an action is about to be executed."""
        sid = state_id[:8]
        self.console.print(
            f"  [cyan]>[/cyan] [dim]({sid})[/dim]"
            f" {action.action_type.value}: {action.label}",
        )

    def log_action_result(
        self,
        action: Action,
        result: ActionResult,
        is_new_state: bool,
    ) -> None:
        """Log the result of an action."""
        icon, color = _OUTCOME_STYLE.get(result.outcome.value, ("?", "white"))
        duration = f"{result.duration_ms:.0f}ms"

        text = Text()
        text.append("    ")
        text.append(icon, style=color)
        text.append(f" {result.outcome.value}", style=color)
        text.append(f" ({duration})")

        if is_new_state and result.outcome.value == "navigation":
            text.append(f" → {result.url_after}", style="green dim")

        if result.error_messages:
            text.append(f" errors: {result.error_messages[:2]}", style="red dim")

        if result.message and self.verbose:
            text.append(f" [{result.message[:80]}]", style="dim")

        self.console.print(text)

    def log_info(self, message: str) -> None:
        """Log an informational message."""
        self.console.print(f"  [dim]{message}[/dim]")

    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self.console.print(f"  [yellow]WARNING:[/yellow] {message}")

    def log_archetype(
        self,
        state_id: str,
        archetype: str,
        confidence: float,
        is_novel: bool,
    ) -> None:
        """Log archetype classification for a state."""
        sid = state_id[:8]
        pct = f"{confidence * 100:.0f}%"
        novelty = "[green]new archetype[/green]" if is_novel else "[dim]known[/dim]"
        self.console.print(
            f"  [magenta]@[/magenta] [dim]({sid})[/dim]"
            f" {archetype} ({pct}) — {novelty}",
        )

    def log_coverage_status(self, coverage: dict[str, Any]) -> None:
        """Log current coverage status."""
        archetypes = len(coverage.get("archetypes_seen", {}))
        features = len(coverage.get("features_tested", []))
        sigs = coverage.get("signatures_seen", 0)
        saturated = coverage.get("is_saturated", False)
        status = "[green]saturated[/green]" if saturated else "[dim]exploring[/dim]"
        self.console.print(
            f"  [magenta]Coverage:[/magenta] {archetypes} archetypes, "
            f"{features} features, {sigs} templates — {status}",
        )

    def log_expectation_result(self, result: ExpectationResult) -> None:
        """Log content expectation check result."""
        if result.total_count == 0:
            return
        passed = result.pass_count
        total = result.total_count
        color = "green" if passed == total else "yellow" if passed > 0 else "red"
        self.console.print(
            f"  [magenta]Content:[/magenta]"
            f" [{color}]{passed}/{total}[/{color}]"
            " expectations met",
        )

    def print_summary(self, result: ExplorationResult) -> None:
        """Print the final exploration summary."""
        self.console.print()

        stability_scores = [
            float(action_result.stability_score or 0.0)
            for action_result in result.results
        ]
        average_stability = (
            sum(stability_scores) / len(stability_scores) if stability_scores else 0.0
        )
        stable_steps = sum(1 for score in stability_scores if score >= 0.7)
        unstable_steps = sum(1 for score in stability_scores if score < 0.7)

        # Stats table
        table = Table(title="Exploration Summary", border_style="cyan")
        table.add_column("Metric", style="bold")
        table.add_column("Value", justify="right")

        table.add_row("States discovered", str(result.stats.get("total_states", 0)))
        table.add_row(
            "Actions executed", str(result.stats.get("total_actions_executed", 0))
        )
        table.add_row(
            "Unique actions", str(result.stats.get("total_unique_actions", 0))
        )
        table.add_row("Flows identified", str(len(result.flows)))
        table.add_row("Duration", f"{result.duration_seconds:.1f}s")
        table.add_row("Avg stability", f"{average_stability:.2f}")
        table.add_row("Stable steps (>=0.7)", str(stable_steps))
        table.add_row("Unstable steps (<0.7)", str(unstable_steps))

        self.console.print(table)

        # Outcome breakdown
        outcome_table = Table(title="Outcome Breakdown", border_style="dim")
        outcome_table.add_column("Outcome", style="bold")
        outcome_table.add_column("Count", justify="right")

        for key, value in sorted(result.stats.items()):
            if key.startswith("outcome_"):
                name = key.replace("outcome_", "")
                _, color = _OUTCOME_STYLE.get(name, ("", "white"))
                outcome_table.add_row(Text(name, style=color), str(value))

        if outcome_table.row_count > 0:
            self.console.print(outcome_table)

        # Flows summary
        if result.flows:
            self.console.print()
            flow_table = Table(title="Discovered Flows", border_style="green")
            flow_table.add_column("#", style="dim", width=4)
            flow_table.add_column("Name", style="bold")
            flow_table.add_column("Steps", justify="right", width=6)
            flow_table.add_column("Type", width=8)
            flow_table.add_column("Stability", width=14)
            flow_table.add_column("Description", max_width=55)

            for i, flow in enumerate(result.flows[:20], 1):
                flow_type = "[red]Cycle[/red]" if flow.is_cycle else "Linear"
                stability_text = (
                    f"[green]{flow.stability_score:.2f} stable[/green]"
                    if flow.is_stable
                    else f"[yellow]{flow.stability_score:.2f} unstable[/yellow]"
                )
                flow_table.add_row(
                    str(i),
                    flow.name,
                    str(flow.depth),
                    flow_type,
                    stability_text,
                    flow.description[:55],
                )

            self.console.print(flow_table)

            if len(result.flows) > 20:
                self.console.print(
                    f"  [dim]... and {len(result.flows) - 20} more flows[/dim]"
                )

    def print_site_model_summary(self, model: SiteModel) -> None:
        """Print a site model summary to the terminal."""
        from flowscout.mbt import compute_model_coverage
        from flowscout.modeling.scenarios import FlowScenario

        self.console.print()
        self.console.print(
            Panel(
                f"[bold]{model.summary.total_page_types}[/bold] page types  |  "
                f"[bold]{model.summary.total_navigation_edges}[/bold] edges  |  "
                f"[bold]{model.summary.total_scenarios}[/bold] scenarios",
                title="[bold cyan]Site Model[/bold cyan]",
                border_style="magenta",
            )
        )

        # Page types table
        pt_table = Table(title="Page Types", border_style="magenta")
        pt_table.add_column("Name", style="bold")
        pt_table.add_column("Archetype")
        pt_table.add_column("Instances", justify="right")
        pt_table.add_column("URL Pattern", max_width=50)
        pt_table.add_column("Features")

        for pt in model.page_types:
            pt_table.add_row(
                pt.name,
                pt.archetype.value,
                str(pt.instance_count),
                pt.url_pattern[:50] if pt.url_pattern else "-",
                ", ".join(sorted(pt.features)) if pt.features else "-",
            )
        self.console.print(pt_table)

        # Navigation edges table
        if model.navigation_edges:
            nav_table = Table(title="Navigation Map", border_style="magenta")
            nav_table.add_column("From")
            nav_table.add_column("To")
            nav_table.add_column("Trigger", max_width=40)
            nav_table.add_column("Count", justify="right")

            pt_names = {pt.page_type_id: pt.name for pt in model.page_types}

            for edge in model.navigation_edges:
                from_name = pt_names.get(edge.from_page_type, edge.from_page_type[:8])
                to_name = pt_names.get(edge.to_page_type, edge.to_page_type[:8])
                nav_table.add_row(
                    from_name,
                    to_name,
                    edge.trigger[:40],
                    str(edge.occurrence_count),
                )
            self.console.print(nav_table)

        # Flow templates table
        if model.flow_templates:
            template_table = Table(title="Flow Templates", border_style="green")
            template_table.add_column("Template", style="bold")
            template_table.add_column("Representative", style="dim", max_width=24)
            template_table.add_column("Stability", justify="right", width=10)

            for template in model.flow_templates:
                template_table.add_row(
                    f"{template.name} ({template.occurrence_count} instances)",
                    template.representative_flow_id,
                    f"{template.stability_score:.2f}",
                )

            self.console.print(template_table)

        # Scenarios table
        if model.test_scenarios:
            sc_table = Table(title="Test Scenarios", border_style="green")
            sc_table.add_column("#", width=4)
            sc_table.add_column("Name", style="bold")
            sc_table.add_column("Priority", width=12)
            sc_table.add_column("Steps", justify="right", width=6)
            sc_table.add_column("Tags")

            for i, scenario_data in enumerate(model.test_scenarios, 1):
                sc = (
                    scenario_data
                    if isinstance(scenario_data, FlowScenario)
                    else FlowScenario.model_validate(scenario_data)
                )
                priority_style = {
                    "critical": "red",
                    "important": "yellow",
                    "nice-to-have": "dim",
                }.get(sc.priority, "white")
                sc_table.add_row(
                    str(i),
                    sc.name,
                    Text(sc.priority, style=priority_style),
                    str(len(sc.steps)),
                    ", ".join(sc.tags),
                )
            self.console.print(sc_table)

        coverage = compute_model_coverage(model=model)
        self.console.print()
        self.console.print(
            "  [bold]State coverage:[/bold]"
            f" {coverage.state_coverage:.0f}%"
            f" ({coverage.covered_states}/{coverage.total_states} states)",
        )
        self.console.print(
            "  [bold]Edge coverage:[/bold]"
            f" {coverage.edge_coverage:.0f}%"
            f" ({coverage.covered_edges}/{coverage.total_edges} edges)",
        )
        self.console.print(
            "  [bold]Path coverage:[/bold]"
            f" {coverage.path_coverage:.0f}%"
            f" ({coverage.covered_paths}/{coverage.total_paths} simple paths)",
        )

        if coverage.uncovered_states:
            uncovered_states = ", ".join(coverage.uncovered_states[:8])
            suffix = " ..." if len(coverage.uncovered_states) > 8 else ""
            self.console.print(
                f"  [yellow]Uncovered states:[/yellow] {uncovered_states}{suffix}",
            )

        if coverage.uncovered_edges:
            preview = ", ".join(
                f"{from_state}->{to_state} ({action_type})"
                for from_state, to_state, action_type in coverage.uncovered_edges[:8]
            )
            suffix = " ..." if len(coverage.uncovered_edges) > 8 else ""
            self.console.print(
                f"  [yellow]Uncovered edges:[/yellow] {preview}{suffix}",
            )

        # Coverage notes
        if model.summary.coverage_notes:
            self.console.print()
            for note in model.summary.coverage_notes:
                self.console.print(f"  [dim]{note}[/dim]")

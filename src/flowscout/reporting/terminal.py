"""Rich terminal output for live exploration progress."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from flowscout.analysis.graph import ExplorationResult
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
            f"[bold]Max depth:[/bold] {config.max_depth}  |  "
            f"[bold]Max states:[/bold] {config.max_states}  |  "
            f"[bold]Max actions/state:[/bold] {config.max_actions_per_state}",
            f"[bold]Headless:[/bold] {config.headless}  |  "
            f"[bold]Screenshots:[/bold] {config.take_screenshots}",
        ]
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
            f"  [cyan]>[/cyan] [dim]({sid})[/dim] {action.action_type.value}: {action.label}",
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

    def print_summary(self, result: ExplorationResult) -> None:
        """Print the final exploration summary."""
        self.console.print()

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

        self.console.print(table)

        # Verdict summary
        pass_count = sum(1 for r in result.results if r.verdict == "pass")
        fail_count = sum(1 for r in result.results if r.verdict == "fail")
        warn_count = sum(1 for r in result.results if r.verdict == "warn")
        if pass_count or fail_count or warn_count:
            verdict_line = Text("  Verdicts: ")
            verdict_line.append(f"{pass_count} PASSED", style="green")
            verdict_line.append(", ")
            verdict_line.append(f"{fail_count} FAILED", style="red")
            verdict_line.append(", ")
            verdict_line.append(f"{warn_count} WARNINGS", style="yellow")
            self.console.print(verdict_line)

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
            flow_table.add_column("Verdict", width=8)
            flow_table.add_column("Description", max_width=55)

            for i, flow in enumerate(result.flows[:20], 1):
                flow_type = "[red]Cycle[/red]" if flow.is_cycle else "Linear"
                v = getattr(flow.verdict, "verdict", None)
                if v:
                    v_str = v.value.upper()
                    if v_str == "PASS":
                        verdict_text = "[green]PASS[/green]"
                    elif v_str == "FAIL":
                        verdict_text = "[red]FAIL[/red]"
                    elif v_str == "WARN":
                        verdict_text = "[yellow]WARN[/yellow]"
                    else:
                        verdict_text = f"[dim]{v_str}[/dim]"
                else:
                    verdict_text = "[dim]N/A[/dim]"
                flow_table.add_row(
                    str(i),
                    flow.name,
                    str(flow.depth),
                    flow_type,
                    verdict_text,
                    flow.description[:55],
                )

            self.console.print(flow_table)

            if len(result.flows) > 20:
                self.console.print(
                    f"  [dim]... and {len(result.flows) - 20} more flows[/dim]"
                )

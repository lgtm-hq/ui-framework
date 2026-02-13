"""DOT exporter for SiteModel MBT graphs."""

from __future__ import annotations

from flowscout.modeling.site_model import SiteModel


def render_dot(*, model: SiteModel) -> str:
    """Render SiteModel graph in Graphviz DOT format."""
    lines = [
        "digraph SiteModel {",
        '  rankdir="LR";',
        '  graph [fontname="Helvetica"];',
        '  node [shape="box", style="rounded", fontname="Helvetica"];',
        '  edge [fontname="Helvetica"];',
    ]

    for page_type in model.page_types:
        label = _escape(page_type.name or page_type.page_type_id)
        lines.append(f'  "{page_type.page_type_id}" [label="{label}"];')

    for edge in model.navigation_edges:
        label = _edge_label(
            action_type=edge.action_type.value,
            occurrence_count=edge.occurrence_count,
            trigger=edge.trigger,
            guards=list(getattr(edge, "guards", [])),
        )
        lines.append(
            f'  "{edge.from_page_type}" -> "{edge.to_page_type}" '
            f'[label="{_escape(label)}"];',
        )

    lines.append("}")
    return "\n".join(lines)


def _edge_label(
    *,
    action_type: str,
    occurrence_count: int,
    trigger: str,
    guards: list[str],
) -> str:
    """Build a DOT edge label with action/count metadata."""
    parts = [f"{action_type} ({max(occurrence_count, 1)}x)"]
    cleaned_trigger = trigger.strip()
    if cleaned_trigger:
        parts.append(cleaned_trigger)
    if guards:
        parts.append(f"guard: {', '.join(sorted(set(guards)))}")
    return " | ".join(parts)


def _escape(value: str) -> str:
    """Escape labels for DOT string literals."""
    return value.replace("\\", "\\\\").replace('"', '\\"')

"""Mermaid exporter for SiteModel MBT graphs."""

from __future__ import annotations

import re

from flowscout.modeling.site_model import SiteModel


def render_mermaid(*, model: SiteModel) -> str:
    """Render SiteModel graph in Mermaid ``stateDiagram-v2`` format."""
    lines = ["stateDiagram-v2"]
    alias_map = {
        page_type.page_type_id: _alias(page_type.page_type_id)
        for page_type in model.page_types
    }

    for page_type in model.page_types:
        alias = alias_map[page_type.page_type_id]
        label = _escape_text(page_type.name or page_type.page_type_id)
        lines.append(f'    state "{label}" as {alias}')

    for edge in model.navigation_edges:
        from_alias = alias_map.get(edge.from_page_type, _alias(edge.from_page_type))
        to_alias = alias_map.get(edge.to_page_type, _alias(edge.to_page_type))
        label = _edge_label(
            action_type=edge.action_type.value,
            occurrence_count=edge.occurrence_count,
            trigger=edge.trigger,
            guards=list(getattr(edge, "guards", [])),
        )
        lines.append(f"    {from_alias} --> {to_alias}: {_escape_text(label)}")

    return "\n".join(lines)


def _edge_label(
    *,
    action_type: str,
    occurrence_count: int,
    trigger: str,
    guards: list[str],
) -> str:
    """Build Mermaid transition label including count metadata."""
    parts = [f"{action_type} ({max(occurrence_count, 1)}x)"]
    cleaned_trigger = trigger.strip()
    if cleaned_trigger:
        parts.append(cleaned_trigger)
    if guards:
        parts.append(f"guard: {', '.join(sorted(set(guards)))}")
    return " | ".join(parts)


def _alias(page_type_id: str) -> str:
    """Convert page type IDs to Mermaid-safe aliases."""
    base = re.sub(pattern=r"[^0-9A-Za-z_]", repl="_", string=page_type_id)
    collapsed = re.sub(pattern=r"_+", repl="_", string=base).strip("_")
    if not collapsed:
        return "state_node"
    if collapsed[0].isdigit():
        return f"state_{collapsed}"
    return collapsed


def _escape_text(value: str) -> str:
    """Escape text for Mermaid labels."""
    return value.replace('"', "'")

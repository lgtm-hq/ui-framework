"""GraphWalker JSON exporter for SiteModel."""

from __future__ import annotations

from typing import Any
import json
import re

from flowscout.modeling.site_model import SiteModel


def export_graphwalker_model(
    *,
    model: SiteModel,
    model_name: str = "flowscout-model",
) -> dict[str, Any]:
    """Export a SiteModel as GraphWalker-compatible JSON payload."""
    node_id_map = {
        page_type.page_type_id: f"v_{_safe_id(page_type.page_type_id)}"
        for page_type in model.page_types
    }

    vertices = [
        {
            "id": node_id_map[page_type.page_type_id],
            "name": page_type.name or page_type.page_type_id,
            "properties": {
                "pageTypeId": page_type.page_type_id,
            },
        }
        for page_type in model.page_types
    ]

    edges = []
    for index, edge in enumerate(model.navigation_edges):
        source_vertex = node_id_map.get(
            edge.from_page_type,
            f"v_{_safe_id(edge.from_page_type)}",
        )
        target_vertex = node_id_map.get(
            edge.to_page_type,
            f"v_{_safe_id(edge.to_page_type)}",
        )
        label = _edge_label(
            action_type=edge.action_type.value,
            occurrence_count=edge.occurrence_count,
            trigger=edge.trigger,
        )
        guards = list(getattr(edge, "guards", []))
        edge_payload: dict[str, Any] = {
            "id": f"e_{index}",
            "name": label,
            "sourceVertexId": source_vertex,
            "targetVertexId": target_vertex,
            "weight": max(edge.occurrence_count, 1),
        }
        if guards:
            edge_payload["guard"] = " && ".join(sorted(set(guards)))
        inferred_from = str(getattr(edge, "inferred_from", "")).strip()
        if inferred_from:
            edge_payload["description"] = inferred_from
        edges.append(edge_payload)

    model_payload: dict[str, Any] = {
        "id": f"m_{_safe_id(model_name)}",
        "name": model_name,
        "vertices": vertices,
        "edges": edges,
    }
    if vertices:
        model_payload["startElementId"] = vertices[0]["id"]

    return {"models": [model_payload]}


def render_graphwalker_json(
    *,
    model: SiteModel,
    model_name: str = "flowscout-model",
) -> str:
    """Render SiteModel in GraphWalker JSON format."""
    payload = export_graphwalker_model(
        model=model,
        model_name=model_name,
    )
    return json.dumps(payload, indent=2)


def _edge_label(
    *,
    action_type: str,
    occurrence_count: int,
    trigger: str,
) -> str:
    """Build a readable transition label for GraphWalker edges."""
    base = f"{action_type} ({max(occurrence_count, 1)}x)"
    cleaned_trigger = trigger.strip()
    if not cleaned_trigger:
        return base
    return f"{base} - {cleaned_trigger}"


def _safe_id(value: str) -> str:
    """Convert arbitrary identifiers to GraphWalker-safe IDs."""
    sanitized = re.sub(pattern=r"[^0-9A-Za-z_]", repl="_", string=value.strip())
    compact = re.sub(pattern=r"_+", repl="_", string=sanitized).strip("_")
    return compact or "node"

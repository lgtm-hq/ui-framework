"""Crawl trace sidecar export for machine-readable timeline consumers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flowscout.analysis.graph import ExplorationResult

TRACE_SCHEMA_VERSION = "1.0.0"


def write_crawl_trace(
    *,
    result: ExplorationResult,
    output_path: str | Path,
) -> Path:
    """Write crawl trace JSON sidecar and return the output path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    trace_payload = build_crawl_trace(result=result)
    path.write_text(json.dumps(trace_payload, indent=2))
    return path


def build_crawl_trace(*, result: ExplorationResult) -> dict[str, Any]:
    """Build a machine-readable crawl trace payload."""
    steps = _serialize_steps(result=result)
    states = [state.model_dump(mode="json") for state in result.states.values()]
    actions = [action.model_dump(mode="json") for action in result.actions.values()]
    return {
        "schema_version": TRACE_SCHEMA_VERSION,
        "result_schema_version": result.schema_version or result.version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_states": len(result.states),
            "total_actions": len(result.actions),
            "total_steps": len(result.results),
            "total_flows": len(result.flows),
        },
        "config": {
            "start_url": str(result.config.get("start_url", "")),
            "environment": str(result.config.get("environment", "")),
            "behavior_modes": dict(result.config.get("behavior_modes", {})),
        },
        "states": states,
        "actions": actions,
        "steps": steps,
    }


def _serialize_steps(*, result: ExplorationResult) -> list[dict[str, Any]]:
    """Serialize action execution results into ordered crawl steps."""
    steps: list[dict[str, Any]] = []
    for index, action_result in enumerate(result.results, start=1):
        source_state = result.states.get(action_result.source_state_id)
        target_state = result.states.get(action_result.target_state_id)
        action = result.actions.get(action_result.action_id)
        step: dict[str, Any] = {
            "index": index,
            "action_id": action_result.action_id,
            "source_state_id": action_result.source_state_id,
            "target_state_id": action_result.target_state_id,
            "outcome": action_result.outcome.value,
            "result": action_result.model_dump(mode="json"),
            "source_state": _serialize_state_ref(source_state),
            "target_state": _serialize_state_ref(target_state),
        }
        if action is not None:
            step["action"] = {
                "action_type": action.action_type.value,
                "label": action.label,
                "target_selector": action.target_selector,
                "value": action.value,
                "priority": action.priority,
                "metadata": dict(action.metadata),
            }
        steps.append(step)
    return steps


def _serialize_state_ref(state: Any | None) -> dict[str, Any]:
    """Serialize a compact state reference for transition steps."""
    if state is None:
        return {}
    return {
        "state_id": state.state_id,
        "url": state.url,
        "title": state.title,
        "route_key": state.route_key,
        "view_key": state.view_key,
        "context_key": state.context_key,
    }

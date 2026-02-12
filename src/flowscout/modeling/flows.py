"""Flow-template models and deduplication helpers."""

from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping, Sequence

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from flowscout.analysis.graph import Flow
    from flowscout.discovery.actions import Action


_KNOWN_PAGE_TOKENS: tuple[tuple[str, str], ...] = (
    ("search_results", "Search Results"),
    ("search", "Search"),
    ("listing", "Listing"),
    ("detail", "Detail"),
    ("product", "Product"),
    ("form", "Form"),
    ("landing", "Landing"),
    ("checkout", "Checkout"),
    ("cart", "Cart"),
    ("auth", "Auth"),
    ("login", "Login"),
    ("error", "Error"),
)


@dataclass(frozen=True)
class _FlowGroup:
    key: tuple[str, ...]
    flows: list[Flow]


class FlowTemplate(BaseModel):
    """A deduplicated flow pattern grouped by page-type sequence."""

    template_id: str
    name: str
    page_type_sequence: list[str] = Field(default_factory=list)
    occurrence_count: int = 0
    representative_flow_id: str = ""
    instance_flow_ids: list[str] = Field(default_factory=list)
    action_type_sequence: list[str] = Field(default_factory=list)
    stability_score: float = 0.0


def deduplicate_flows(
    *,
    flows: Sequence[Flow],
    state_to_page_type: Mapping[str, str],
    actions_by_id: Mapping[str, Action] | None = None,
    page_type_names: Mapping[str, str] | None = None,
) -> list[FlowTemplate]:
    """Collapse flows that share the same page-type sequence."""
    if not flows:
        return []

    groups = _group_flows(flows=flows, state_to_page_type=state_to_page_type)
    templates: list[FlowTemplate] = []

    for index, group in enumerate(groups, start=1):
        representative = _select_representative(group.flows)
        occurrence_count = len(group.flows)
        avg_stability = (
            sum(float(flow.stability_score or 0.0) for flow in group.flows)
            / occurrence_count
        )

        templates.append(
            FlowTemplate(
                template_id=f"flow-template-{index}",
                name=_build_template_name(
                    page_type_sequence=group.key,
                    representative_name=representative.name,
                    page_type_names=page_type_names,
                ),
                page_type_sequence=list(group.key),
                occurrence_count=occurrence_count,
                representative_flow_id=representative.flow_id,
                instance_flow_ids=[flow.flow_id for flow in group.flows],
                action_type_sequence=_build_action_type_sequence(
                    action_ids=representative.action_ids,
                    actions_by_id=actions_by_id,
                ),
                stability_score=round(avg_stability, 4),
            )
        )

    templates.sort(
        key=lambda template: (
            -template.occurrence_count,
            -template.stability_score,
            template.name.lower(),
        )
    )
    return templates


def _group_flows(
    *,
    flows: Sequence[Flow],
    state_to_page_type: Mapping[str, str],
) -> list[_FlowGroup]:
    grouped: OrderedDict[tuple[str, ...], list[Flow]] = OrderedDict()

    for flow in flows:
        key = tuple(
            state_to_page_type.get(state_id, state_id) for state_id in flow.state_ids
        )
        if not key:
            key = (flow.flow_id,)
        grouped.setdefault(key, []).append(flow)

    return [_FlowGroup(key=key, flows=group) for key, group in grouped.items()]


def _select_representative(flows: Sequence[Flow]) -> Flow:
    return max(
        flows,
        key=lambda flow: (
            float(flow.stability_score or 0.0),
            len(flow.action_ids),
            len(flow.state_ids),
            flow.flow_id,
        ),
    )


def _build_action_type_sequence(
    *,
    action_ids: Sequence[str],
    actions_by_id: Mapping[str, Action] | None,
) -> list[str]:
    if not action_ids:
        return []
    if not actions_by_id:
        return ["UNKNOWN" for _ in action_ids]

    sequence: list[str] = []
    for action_id in action_ids:
        action = actions_by_id.get(action_id)
        if not action:
            sequence.append("UNKNOWN")
            continue
        sequence.append(action.action_type.value.upper())
    return sequence


def _build_template_name(
    *,
    page_type_sequence: Sequence[str],
    representative_name: str,
    page_type_names: Mapping[str, str] | None,
) -> str:
    labels = [
        _format_page_type_label(page_type_id, page_type_names=page_type_names)
        for page_type_id in page_type_sequence
    ]
    labels = [label for label in labels if label]

    if len(labels) >= 2:
        return f"Browse {labels[0]} \u2192 {labels[-1]}"
    if len(labels) == 1:
        return f"Explore {labels[0]}"
    if representative_name:
        return representative_name
    return "Flow Template"


def _format_page_type_label(
    page_type_id: str,
    *,
    page_type_names: Mapping[str, str] | None,
) -> str:
    if page_type_names and page_type_id in page_type_names:
        return page_type_names[page_type_id]

    normalized = page_type_id.strip().lower()
    if not normalized:
        return ""

    for token, label in _KNOWN_PAGE_TOKENS:
        if token in normalized:
            return label

    text = re.sub(r"[_\-/]+", " ", page_type_id).strip()
    if not text:
        return page_type_id[:8]
    if len(text) > 48:
        text = text[:48].rstrip()
    return text.title()

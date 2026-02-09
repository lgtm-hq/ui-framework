"""Element inventory summaries derived from smart page analysis catalogs."""

from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

_INTERACTIVE_TYPES = frozenset(
    {
        "link",
        "button",
        "select",
        "textarea",
        "tab",
        "menuitem",
        "option",
        "search",
    }
)


def is_interactive_element_type(element_type: str) -> bool:
    """Return True when a catalog element_type represents interactive UI."""
    normalized = (element_type or "").strip().lower()
    return normalized.startswith("input_") or normalized in _INTERACTIVE_TYPES


def summarize_element_inventory(
    *,
    analyses: Mapping[str, Any],
    states_by_id: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build aggregate interactive/content element inventory from smart analyses."""
    interactive_type_counts: Counter[str] = Counter()
    non_interactive_type_counts: Counter[str] = Counter()
    per_page: list[dict[str, Any]] = []

    for state_id, analysis in analyses.items():
        catalog = analysis.get("catalog", {}) if isinstance(analysis, dict) else {}
        entries = catalog.get("entries", []) if isinstance(catalog, dict) else []

        interactive_count = 0
        non_interactive_count = 0
        page_types: Counter[str] = Counter()

        if isinstance(entries, list):
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                element_type = str(entry.get("element_type") or "other").strip().lower()
                if not element_type:
                    element_type = "other"

                page_types[element_type] += 1
                if is_interactive_element_type(element_type):
                    interactive_count += 1
                    interactive_type_counts[element_type] += 1
                else:
                    non_interactive_count += 1
                    non_interactive_type_counts[element_type] += 1

        state = states_by_id.get(state_id) if states_by_id else None
        per_page.append(
            {
                "state_id": state_id,
                "title": getattr(state, "title", "") if state else "",
                "url": getattr(state, "url", "") if state else "",
                "interactive_elements": interactive_count,
                "non_interactive_elements": non_interactive_count,
                "total_elements": interactive_count + non_interactive_count,
                "top_types": _counter_to_rows(page_types, limit=5),
            }
        )

    interactive_total = sum(row["interactive_elements"] for row in per_page)
    non_interactive_total = sum(row["non_interactive_elements"] for row in per_page)
    total_elements = interactive_total + non_interactive_total
    interactive_pct = round(interactive_total / max(total_elements, 1) * 100)

    per_page.sort(
        key=lambda row: (
            -int(row["total_elements"]),
            str(row["state_id"]),
        )
    )

    return {
        "pages_analyzed": len(analyses),
        "pages_with_elements": sum(1 for row in per_page if row["total_elements"] > 0),
        "total_elements": total_elements,
        "interactive_elements": interactive_total,
        "non_interactive_elements": non_interactive_total,
        "interactive_pct": interactive_pct,
        "top_interactive_types": _counter_to_rows(interactive_type_counts),
        "top_non_interactive_types": _counter_to_rows(non_interactive_type_counts),
        "per_page": per_page,
    }


def _counter_to_rows(counter: Counter[str], *, limit: int = 10) -> list[dict[str, Any]]:
    """Convert a Counter to deterministic sorted rows."""
    rows: list[dict[str, Any]] = []
    for element_type, count in sorted(
        counter.items(), key=lambda item: (-item[1], item[0])
    )[:limit]:
        rows.append({"element_type": element_type, "count": count})
    return rows

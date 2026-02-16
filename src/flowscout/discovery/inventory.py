"""Full page element inventory discovery."""

from __future__ import annotations

import logging
from typing import Any

from flowscout.core.inventory import (
    FormField,
    FormStructure,
    InventoryElement,
    PageInventory,
)
from flowscout.core.types import CatalogElement, RawFormField, RawFormStructure

logger = logging.getLogger(__name__)


def build_page_inventory(
    raw: dict[str, Any],
    *,
    url: str,
    state_id: str,
    collect_bounding_boxes: bool = True,
) -> PageInventory:
    """Build a PageInventory from raw page_analysis.js output.

    This function maps the raw JavaScript return value into typed Pydantic
    models. It is designed to be called with the result of
    ``browser.analyze_page_structure()``.
    """
    elements = _build_elements(
        raw.get("element_catalog", []),
        collect_bounding_boxes=collect_bounding_boxes,
    )
    forms = _build_forms(raw.get("form_structures", []))

    return PageInventory(
        url=url,
        state_id=state_id,
        elements=elements,
        forms=forms,
        content_metrics=raw.get("content_metrics", {}),
        zone_hints=raw.get("zone_hints", {}),
        structural_skeleton=raw.get("structural_skeleton", ""),
    )


def _build_elements(
    raw_catalog: list[CatalogElement],
    *,
    collect_bounding_boxes: bool = True,
) -> list[InventoryElement]:
    """Convert raw JS catalog entries to InventoryElement models."""
    elements: list[InventoryElement] = []
    for entry in raw_catalog:
        bbox = entry.get("bounding_box") if collect_bounding_boxes else None
        elements.append(
            InventoryElement(
                selector=entry.get("selector", ""),
                xpath=entry.get("xpath"),
                dom_id=entry.get("dom_id", ""),
                tag=entry.get("tag", ""),
                element_type=entry.get("element_type", ""),
                zone=entry.get("zone", ""),
                label=entry.get("label", ""),
                visible_text=entry.get("visible_text", ""),
                aria_label=entry.get("aria_label") or None,
                aria_role=entry.get("aria_role") or None,
                href=entry.get("href") or None,
                src=entry.get("src") or None,
                name=entry.get("name") or None,
                input_type=entry.get("input_type") or None,
                is_interactive=entry.get("is_interactive", False),
                is_visible=entry.get("is_visible", True),
                bounding_box=bbox,
                computed_styles=entry.get("computed_styles", {}),
                parent_selector=entry.get("parent_selector") or None,
                parent_tag=entry.get("parent_tag") or None,
                data_attributes=entry.get("data_attributes", {}),
                locator_score=entry.get("locator_score", 0.0),
                preferred_selector=entry.get("preferred_selector", ""),
                preferred_strategy=entry.get("preferred_strategy", ""),
            )
        )
    return elements


def _build_forms(
    raw_forms: list[RawFormStructure],
) -> list[FormStructure]:
    """Convert raw JS form structures to FormStructure models."""
    forms: list[FormStructure] = []
    for raw_form in raw_forms:
        fields = _build_form_fields(raw_form.get("fields", []))
        forms.append(
            FormStructure(
                form_selector=raw_form.get("form_selector", ""),
                action=raw_form.get("action") or None,
                method=raw_form.get("method", "GET"),
                fields=fields,
                submit_selector=raw_form.get("submit_selector") or None,
            )
        )
    return forms


def _build_form_fields(
    raw_fields: list[RawFormField],
) -> list[FormField]:
    """Convert raw JS form fields to FormField models."""
    fields: list[FormField] = []
    for raw_field in raw_fields:
        fields.append(
            FormField(
                selector=raw_field.get("selector", ""),
                name=raw_field.get("name") or None,
                input_type=raw_field.get("input_type", "text"),
                label=raw_field.get("label", ""),
                is_required=raw_field.get("is_required", False),
                placeholder=raw_field.get("placeholder") or None,
                options=raw_field.get("options", []),
                validation_pattern=raw_field.get("validation_pattern") or None,
            )
        )
    return fields

"""Pydantic models for full page element inventory."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from flowscout.core.types import BoundingBox


class InventoryElement(BaseModel):
    """A single element in the full page inventory."""

    selector: str
    xpath: str | None = None
    dom_id: str = ""
    tag: str
    element_type: str = ""
    zone: str = ""
    label: str = ""
    visible_text: str = ""
    aria_label: str | None = None
    aria_role: str | None = None
    href: str | None = None
    src: str | None = None
    name: str | None = None
    input_type: str | None = None
    is_interactive: bool = False
    is_visible: bool = True
    bounding_box: BoundingBox | None = None
    computed_styles: dict[str, str] = Field(default_factory=dict)
    parent_selector: str | None = None
    parent_tag: str | None = None
    data_attributes: dict[str, str] = Field(default_factory=dict)
    locator_score: float = 0.0
    preferred_selector: str = ""
    preferred_strategy: str = ""


class FormField(BaseModel):
    """A single field within a form."""

    selector: str
    name: str | None = None
    input_type: str = "text"
    label: str = ""
    is_required: bool = False
    placeholder: str | None = None
    options: list[str] = Field(default_factory=list)
    validation_pattern: str | None = None


class FormStructure(BaseModel):
    """A form element with its fields."""

    form_selector: str
    action: str | None = None
    method: str = "GET"
    fields: list[FormField] = Field(default_factory=list)
    submit_selector: str | None = None


class PageInventory(BaseModel):
    """Complete element inventory for a single page state."""

    url: str
    state_id: str
    elements: list[InventoryElement] = Field(default_factory=list)
    forms: list[FormStructure] = Field(default_factory=list)
    content_metrics: dict[str, int | list[str]] = Field(default_factory=dict)
    zone_hints: dict[str, bool] = Field(default_factory=dict)
    structural_skeleton: str = ""
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

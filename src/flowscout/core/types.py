"""TypedDicts for untyped data returned by page.evaluate() JavaScript calls."""

from __future__ import annotations

from typing import TypedDict


class BoundingBox(TypedDict):
    """Bounding rectangle returned by Element.getBoundingClientRect()."""

    x: float
    y: float
    width: float
    height: float


class RawElement(TypedDict, total=False):
    """Shape of objects returned by the discovery.js sweep.

    ``total=False`` because many fields are optional (null in JS → absent key).
    Only ``selector``, ``tag``, and ``label`` are guaranteed present.
    """

    selector: str
    dom_id: str | None
    tag: str
    input_type: str | None
    role: str | None
    aria_label: str | None
    aria_expanded: str | None
    href: str | None
    name: str | None
    placeholder: str | None
    value: str | None
    required: bool
    disabled: bool
    visible: bool
    label: str
    options: list[str]
    parent_form: str | None
    bbox: BoundingBox | None
    data_attrs: dict[str, str]


class RepeatedGroup(TypedDict):
    """A group of structurally similar sibling elements (page_analysis.js)."""

    parent_selector: str
    count: int
    tag_signature: str
    item_texts: list[str]
    item_selectors: list[str]


class ContentMetrics(TypedDict):
    """Aggregate content metrics for a page (page_analysis.js)."""

    total_text_length: int
    heading_count: int
    h1_texts: list[str]
    h2_texts: list[str]
    image_count: int
    link_count: int
    form_input_count: int
    interactive_count: int


class ZoneHints(TypedDict):
    """Boolean feature flags for page layout zones (page_analysis.js)."""

    has_nav: bool
    has_search_input: bool
    has_pagination: bool
    has_filters: bool
    has_hero: bool
    has_single_heading_focus: bool


class CatalogElement(TypedDict, total=False):
    """An element entry in the element_catalog array (page_analysis.js)."""

    selector: str
    dom_id: str
    tag: str
    label: str
    zone: str
    element_type: str
    aria_role: str
    input_type: str
    is_visible: bool
    bounding_box: BoundingBox | None


class PageAnalysis(TypedDict):
    """Full return value of page_analysis.js — used by smart-mode planner."""

    repeated_groups: list[RepeatedGroup]
    content_metrics: ContentMetrics
    zone_hints: ZoneHints
    structural_skeleton: str
    extracted_entities: list[str]
    element_catalog: list[CatalogElement]


class NetworkError(TypedDict):
    """A captured network error (response with status >= 400)."""

    url: str
    status: str
    method: str

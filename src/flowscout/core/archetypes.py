"""Core archetype models and page analysis helpers shared across layers."""

from __future__ import annotations

import re
from enum import StrEnum, auto
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, Field


class PageArchetype(StrEnum):
    LISTING = auto()
    DETAIL = auto()
    SEARCH_RESULTS = auto()
    FORM = auto()
    LANDING = auto()
    ERROR = auto()
    UNKNOWN = auto()


class ZoneType(StrEnum):
    NAVIGATION = auto()
    HEADER = auto()
    SEARCH = auto()
    FILTER = auto()
    MAIN_CONTENT = auto()
    SIDEBAR = auto()
    PAGINATION = auto()
    FOOTER = auto()
    FORM = auto()


_ZONE_MAP: dict[str, ZoneType] = {
    "navigation": ZoneType.NAVIGATION,
    "header": ZoneType.HEADER,
    "search": ZoneType.SEARCH,
    "filter": ZoneType.FILTER,
    "main_content": ZoneType.MAIN_CONTENT,
    "sidebar": ZoneType.SIDEBAR,
    "pagination": ZoneType.PAGINATION,
    "footer": ZoneType.FOOTER,
    "form": ZoneType.FORM,
}


class RepeatedStructure(BaseModel):
    """A group of structurally similar siblings on a page."""

    container_selector: str
    item_count: int
    tag_signature: str
    item_selectors: list[str] = Field(default_factory=list)
    extracted_texts: list[str] = Field(default_factory=list)


class ContentDensity(BaseModel):
    """Quantitative content metrics for a page."""

    total_text_length: int = 0
    heading_count: int = 0
    image_count: int = 0
    link_count: int = 0
    form_input_count: int = 0
    interactive_count: int = 0
    text_to_interactive_ratio: float = 0.0


class ContentZone(BaseModel):
    """A classified zone on the page."""

    zone_type: ZoneType
    selector: str = ""
    element_count: int = 0
    confidence: float = 1.0


class CatalogEntry(BaseModel):
    """A single element in the page catalog."""

    selector: str
    dom_id: str = ""
    tag: str
    label: str
    zone_type: ZoneType = ZoneType.MAIN_CONTENT
    element_type: str = ""
    aria_role: str = ""
    input_type: str = ""
    is_visible: bool = True
    semantic_name: str = ""
    bounding_box: dict[str, float] | None = None


class PageCatalog(BaseModel):
    """All cataloged elements for a page, grouped by zone."""

    archetype: PageArchetype = PageArchetype.UNKNOWN
    url_pattern: str = ""
    entries: list[CatalogEntry] = Field(default_factory=list)


class PageAnalysis(BaseModel):
    """Complete page analysis result."""

    archetype: PageArchetype = PageArchetype.UNKNOWN
    archetype_confidence: float = 0.0
    structural_signature: str = ""
    zones: list[ContentZone] = Field(default_factory=list)
    repeated_structures: list[RepeatedStructure] = Field(default_factory=list)
    content_density: ContentDensity = Field(default_factory=ContentDensity)
    extracted_entities: list[str] = Field(default_factory=list)
    has_search: bool = False
    has_pagination: bool = False
    has_filters: bool = False
    heading_hierarchy: list[str] = Field(default_factory=list)
    catalog: PageCatalog = Field(default_factory=PageCatalog)


class ArchetypeInstance(BaseModel):
    """A single occurrence of an archetype during exploration."""

    state_id: str
    url: str
    archetype: PageArchetype
    structural_signature: str
    content_summary: str = ""


class ArchetypeRegistry:
    """Tracks structural signatures and archetype instances across exploration."""

    def __init__(self, saturation_threshold: int = 3) -> None:
        self._instances: dict[str, list[ArchetypeInstance]] = {}
        self._saturation_threshold = saturation_threshold

    def register(self, state_id: str, analysis: PageAnalysis, url: str = "") -> bool:
        """Register a page analysis.

        Returns True if this is a novel structural signature.
        """
        sig = analysis.structural_signature
        instance = ArchetypeInstance(
            state_id=state_id,
            url=url,
            archetype=analysis.archetype,
            structural_signature=sig,
            content_summary=", ".join(analysis.extracted_entities[:3]),
        )
        if sig not in self._instances:
            self._instances[sig] = [instance]
            return True
        self._instances[sig].append(instance)
        return False

    def is_saturated(self, signature: str) -> bool:
        """Check if a structural signature has been seen enough times."""
        return len(self._instances.get(signature, [])) >= self._saturation_threshold

    def instance_count(self, signature: str) -> int:
        """Return the number of instances for a given signature."""
        return len(self._instances.get(signature, []))

    def all_signatures(self) -> dict[str, int]:
        """Return a summary of all signatures and their instance counts."""
        return {sig: len(instances) for sig, instances in self._instances.items()}

    def archetype_distribution(self) -> dict[str, int]:
        """Return archetype → total instance count."""
        dist: dict[str, int] = {}
        for instances in self._instances.values():
            for inst in instances:
                key = inst.archetype.value
                dist[key] = dist.get(key, 0) + 1
        return dist


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify_archetype(raw: dict[str, Any]) -> tuple[PageArchetype, float]:
    """Score-based archetype classification from raw page analysis data.

    Returns (archetype, confidence) where confidence is winner_score / total.
    """
    scores: dict[PageArchetype, float] = {a: 0.0 for a in PageArchetype}

    repeated = raw.get("repeated_groups", [])
    metrics = raw.get("content_metrics", {})
    zones = raw.get("zone_hints", {})
    total_text = metrics.get("total_text_length", 0)
    heading_count = metrics.get("heading_count", 0)
    form_input_count = metrics.get("form_input_count", 0)
    interactive_count = metrics.get("interactive_count", 0)
    image_count = metrics.get("image_count", 0)
    link_count = metrics.get("link_count", 0)

    # --- LISTING ---
    max_group_count = max((g.get("count", 0) for g in repeated), default=0)
    if max_group_count >= 4:
        scores[PageArchetype.LISTING] += 30
    if max_group_count >= 10:
        scores[PageArchetype.LISTING] += 20
    if zones.get("has_pagination"):
        scores[PageArchetype.LISTING] += 15
    if zones.get("has_filters"):
        scores[PageArchetype.LISTING] += 10
    if link_count >= 10:
        scores[PageArchetype.LISTING] += 5

    # --- DETAIL ---
    # Only score as detail if it's NOT dominated by form inputs or hero sections
    if (
        zones.get("has_single_heading_focus")
        and form_input_count < 3
        and not zones.get("has_hero")
    ):
        scores[PageArchetype.DETAIL] += 30
    if (
        image_count >= 1
        and image_count <= 4
        and total_text > 500
        and form_input_count < 3
    ):
        scores[PageArchetype.DETAIL] += 20
    if (
        interactive_count > 0
        and total_text / max(interactive_count, 1) > 50
        and form_input_count < 3
    ):
        scores[PageArchetype.DETAIL] += 15
    if (
        heading_count >= 2
        and heading_count <= 6
        and total_text > 300
        and form_input_count < 3
    ):
        scores[PageArchetype.DETAIL] += 10

    # --- SEARCH_RESULTS ---
    if zones.get("has_search_input"):
        scores[PageArchetype.SEARCH_RESULTS] += 20
    if zones.get("has_search_input") and max_group_count >= 3:
        scores[PageArchetype.SEARCH_RESULTS] += 25
    if zones.get("has_pagination") and zones.get("has_search_input"):
        scores[PageArchetype.SEARCH_RESULTS] += 10

    # --- FORM ---
    if form_input_count >= 3:
        scores[PageArchetype.FORM] += 30
    if form_input_count >= 6:
        scores[PageArchetype.FORM] += 15
    if form_input_count >= 1 and form_input_count < 3:
        scores[PageArchetype.FORM] += 10

    # --- LANDING ---
    if zones.get("has_hero"):
        scores[PageArchetype.LANDING] += 30
    if max_group_count >= 2 and max_group_count <= 5 and zones.get("has_hero"):
        scores[PageArchetype.LANDING] += 15
    if heading_count >= 3 and zones.get("has_nav"):
        scores[PageArchetype.LANDING] += 10

    # --- ERROR ---
    h1_texts = metrics.get("h1_texts", [])
    h2_texts = metrics.get("h2_texts", [])
    all_headings = " ".join(h1_texts + h2_texts).lower()
    if any(w in all_headings for w in ("404", "not found", "error", "oops")):
        scores[PageArchetype.ERROR] += 50

    # Pick winner
    total = sum(scores.values())
    if total == 0:
        return PageArchetype.UNKNOWN, 0.0

    winner = max(scores, key=lambda a: scores[a])
    confidence = scores[winner] / total
    return winner, round(confidence, 3)


def compute_structural_signature(skeleton: str) -> str:
    """Compute a 16-char hex hash of a content-blind DOM skeleton."""
    return sha256(skeleton.encode()).hexdigest()[:16]


def _to_zone_type(zone_str: str) -> ZoneType:
    """Map a JS zone string to ZoneType."""
    return _ZONE_MAP.get(zone_str, ZoneType.MAIN_CONTENT)


def _generate_semantic_name(selector: str, label: str, tag: str) -> str:
    """Generate a clean Python property name from selector/label/tag."""
    # Prefer label if short enough
    text = label if label and len(label) <= 40 else ""
    if not text:
        # Try extracting from selector
        m = re.search(r"\[aria-label=['\"]([^'\"]+)['\"]", selector)
        if m:
            text = m.group(1)
        elif "#" in selector:
            text = selector.split("#")[-1].split("]")[0]
        else:
            text = selector

    # Clean to valid Python identifier
    clean = re.sub(r"[^\w\s]", "", text.lower())
    clean = re.sub(r"\s+", "_", clean.strip())
    clean = re.sub(r"_+", "_", clean)
    clean = clean.strip("_")

    if not clean or not clean[0].isalpha():
        clean = f"{tag}_{clean}" if clean else tag

    return clean[:40]


def build_page_analysis(raw: dict[str, Any]) -> PageAnalysis:
    """Build a complete PageAnalysis from raw JS page_analysis output."""
    archetype, confidence = classify_archetype(raw)

    skeleton = raw.get("structural_skeleton", "")
    sig = compute_structural_signature(skeleton) if skeleton else ""

    # Repeated structures
    repeated = []
    for g in raw.get("repeated_groups", []):
        repeated.append(
            RepeatedStructure(
                container_selector=g.get("parent_selector", ""),
                item_count=g.get("count", 0),
                tag_signature=g.get("tag_signature", ""),
                item_selectors=g.get("item_selectors", []),
                extracted_texts=g.get("item_texts", []),
            )
        )

    # Content density
    metrics = raw.get("content_metrics", {})
    interactive = metrics.get("interactive_count", 0)
    text_len = metrics.get("total_text_length", 0)
    density = ContentDensity(
        total_text_length=text_len,
        heading_count=metrics.get("heading_count", 0),
        image_count=metrics.get("image_count", 0),
        link_count=metrics.get("link_count", 0),
        form_input_count=metrics.get("form_input_count", 0),
        interactive_count=interactive,
        text_to_interactive_ratio=(
            round(text_len / interactive, 2) if interactive > 0 else 0.0
        ),
    )

    zones = raw.get("zone_hints", {})

    # Heading hierarchy
    headings = metrics.get("h1_texts", []) + metrics.get("h2_texts", [])

    # Element catalog
    catalog_entries = []
    for entry in raw.get("element_catalog", []):
        zone = _to_zone_type(entry.get("zone", "main_content"))
        semantic = _generate_semantic_name(
            entry.get("selector", ""),
            entry.get("label", ""),
            entry.get("tag", ""),
        )
        catalog_entries.append(
            CatalogEntry(
                selector=entry.get("selector", ""),
                dom_id=entry.get("dom_id", ""),
                tag=entry.get("tag", ""),
                label=entry.get("label", ""),
                zone_type=zone,
                element_type=entry.get("element_type", ""),
                aria_role=entry.get("aria_role", ""),
                input_type=entry.get("input_type", ""),
                is_visible=entry.get("is_visible", True),
                semantic_name=semantic,
                bounding_box=entry.get("bounding_box"),
            )
        )

    # Build zone list from catalog
    zone_counts: dict[ZoneType, int] = {}
    for e in catalog_entries:
        zone_counts[e.zone_type] = zone_counts.get(e.zone_type, 0) + 1

    zone_list = [
        ContentZone(zone_type=zt, element_count=count)
        for zt, count in zone_counts.items()
    ]

    catalog = PageCatalog(
        archetype=archetype,
        url_pattern="",
        entries=catalog_entries,
    )

    return PageAnalysis(
        archetype=archetype,
        archetype_confidence=confidence,
        structural_signature=sig,
        zones=zone_list,
        repeated_structures=repeated,
        content_density=density,
        extracted_entities=raw.get("extracted_entities", []),
        has_search=zones.get("has_search_input", False),
        has_pagination=zones.get("has_pagination", False),
        has_filters=zones.get("has_filters", False),
        heading_hierarchy=headings,
        catalog=catalog,
    )

"""Site model — groups states into page types, maps navigation,
synthesizes scenarios."""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from pydantic import BaseModel, Field

from flowscout.analysis.archetype import (
    PageAnalysis,
    PageArchetype,
    PageCatalog,
)
from flowscout.discovery.actions import ActionType, OutcomeType

if TYPE_CHECKING:
    from flowscout.analysis.graph import ExplorationResult

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class PageType(BaseModel):
    """A group of states sharing the same structural signature."""

    page_type_id: str
    name: str
    archetype: PageArchetype = PageArchetype.UNKNOWN
    url_pattern: str = ""
    structural_signature: str = ""
    instance_count: int = 0
    representative_url: str = ""
    representative_state_id: str = ""
    catalog: PageCatalog = Field(default_factory=PageCatalog)
    features: set[str] = Field(default_factory=set)
    instance_urls: list[str] = Field(default_factory=list)


class NavigationEdge(BaseModel):
    """A transition from one page type to another."""

    from_page_type: str
    to_page_type: str
    trigger: str = ""
    action_type: ActionType = ActionType.CLICK
    outcome: OutcomeType = OutcomeType.NAVIGATION
    occurrence_count: int = 1
    example_action_id: str = ""


class SiteModelSummary(BaseModel):
    """Summary statistics for the site model."""

    total_page_types: int = 0
    total_navigation_edges: int = 0
    total_scenarios: int = 0
    coverage_notes: list[str] = Field(default_factory=list)
    archetype_distribution: dict[str, int] = Field(default_factory=dict)


class SiteModel(BaseModel):
    """Complete site model — the top-level deliverable of Stream 2."""

    page_types: list[PageType] = Field(default_factory=list)
    navigation_edges: list[NavigationEdge] = Field(default_factory=list)
    test_scenarios: list[Any] = Field(default_factory=list)
    summary: SiteModelSummary = Field(default_factory=SiteModelSummary)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

# Patterns for URL segments that are likely dynamic parameters.
_DYNAMIC_SEGMENT = re.compile(
    r"^("
    r"\d+|"  # numeric IDs
    r"[0-9a-f]{8,}|"  # hex hashes
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"  # UUIDs
    r")$",
    re.IGNORECASE,
)


class SiteModelBuilder:
    """Builds a SiteModel from an ExplorationResult and optional PageAnalyses."""

    def build(
        self,
        result: ExplorationResult,
        analyses: dict[str, PageAnalysis] | None = None,
    ) -> SiteModel:
        """Build the complete site model.

        Args:
            result: ExplorationResult from Stream 1.
            analyses: Per-state PageAnalysis dict from SmartPlanner.
                      If None, falls back to URL-path grouping.
        """
        page_types = self._build_page_types(result, analyses)
        state_to_pt = self._build_state_lookup(page_types, analyses, result)
        nav_edges = self._build_navigation_edges(result, state_to_pt)

        # Scenario synthesis (imported lazily to avoid circular deps)
        from flowscout.smart.scenarios import ScenarioSynthesizer

        synthesizer = ScenarioSynthesizer()
        scenarios = synthesizer.synthesize(page_types, nav_edges)

        summary = self._build_summary(page_types, nav_edges, scenarios)

        return SiteModel(
            page_types=page_types,
            navigation_edges=nav_edges,
            test_scenarios=scenarios,
            summary=summary,
        )

    # -- Step 1: group states into page types --------------------------------

    def _build_page_types(
        self,
        result: ExplorationResult,
        analyses: dict[str, PageAnalysis] | None,
    ) -> list[PageType]:
        if analyses:
            return self._build_page_types_from_analyses(result, analyses)
        return self._build_page_types_from_urls(result)

    def _build_page_types_from_analyses(
        self,
        result: ExplorationResult,
        analyses: dict[str, PageAnalysis],
    ) -> list[PageType]:
        """Group states by structural_signature from smart analyses."""
        sig_groups: dict[str, list[str]] = defaultdict(list)
        for state_id, analysis in analyses.items():
            sig = analysis.structural_signature
            if sig:
                sig_groups[sig].append(state_id)

        page_types: list[PageType] = []
        for sig, state_ids in sig_groups.items():
            # Pick representative (first state with this signature)
            rep_id = state_ids[0]
            rep_state = result.states.get(rep_id)
            rep_analysis = analyses[rep_id]

            if not rep_state:
                continue

            # Collect all instance URLs
            instance_urls = []
            titles = []
            for sid in state_ids:
                st = result.states.get(sid)
                if st:
                    instance_urls.append(st.url)
                    if st.title:
                        titles.append(st.title)

            name = _infer_page_type_name(
                rep_analysis.archetype,
                instance_urls,
                rep_analysis.heading_hierarchy,
                titles,
            )

            features: set[str] = set()
            if rep_analysis.has_search:
                features.add("has_search")
            if rep_analysis.has_pagination:
                features.add("has_pagination")
            if rep_analysis.has_filters:
                features.add("has_filters")
            if rep_analysis.content_density.form_input_count >= 3:
                features.add("has_form")
            if rep_analysis.repeated_structures:
                features.add("has_repeated_content")

            page_types.append(
                PageType(
                    page_type_id=sig,
                    name=name,
                    archetype=rep_analysis.archetype,
                    url_pattern=_infer_url_pattern(instance_urls),
                    structural_signature=sig,
                    instance_count=len(state_ids),
                    representative_url=rep_state.url,
                    representative_state_id=rep_id,
                    catalog=rep_analysis.catalog,
                    features=features,
                    instance_urls=instance_urls,
                )
            )

        return page_types

    def _build_page_types_from_urls(
        self,
        result: ExplorationResult,
    ) -> list[PageType]:
        """Fallback: group states by URL path structure when no analyses available."""
        template_groups: dict[str, list[str]] = defaultdict(list)

        for state_id, state in result.states.items():
            template = _url_to_template(state.url)
            template_groups[template].append(state_id)

        page_types: list[PageType] = []
        for template, state_ids in template_groups.items():
            rep_id = state_ids[0]
            rep_state = result.states[rep_id]
            instance_urls = [
                result.states[sid].url for sid in state_ids if sid in result.states
            ]
            titles = [
                result.states[sid].title
                for sid in state_ids
                if sid in result.states and result.states[sid].title
            ]

            name = _infer_page_type_name(
                PageArchetype.UNKNOWN,
                instance_urls,
                [],
                titles,
            )

            page_types.append(
                PageType(
                    page_type_id=template,
                    name=name,
                    archetype=PageArchetype.UNKNOWN,
                    url_pattern=_infer_url_pattern(instance_urls),
                    instance_count=len(state_ids),
                    representative_url=rep_state.url,
                    representative_state_id=rep_id,
                    instance_urls=instance_urls,
                )
            )

        return page_types

    # -- Step 2: state → page type lookup ------------------------------------

    def _build_state_lookup(
        self,
        page_types: list[PageType],
        analyses: dict[str, PageAnalysis] | None,
        result: ExplorationResult,
    ) -> dict[str, str]:
        """Create state_id → page_type_id mapping."""
        lookup: dict[str, str] = {}

        if analyses:
            # Map by structural signature
            sig_to_pt: dict[str, str] = {
                pt.structural_signature: pt.page_type_id for pt in page_types
            }
            for state_id, analysis in analyses.items():
                sig = analysis.structural_signature
                if sig in sig_to_pt:
                    lookup[state_id] = sig_to_pt[sig]
        else:
            # Map by URL template
            template_to_pt: dict[str, str] = {
                pt.page_type_id: pt.page_type_id for pt in page_types
            }
            for state_id, state in result.states.items():
                template = _url_to_template(state.url)
                if template in template_to_pt:
                    lookup[state_id] = template_to_pt[template]

        return lookup

    # -- Step 3: navigation edges --------------------------------------------

    def _build_navigation_edges(
        self,
        result: ExplorationResult,
        state_to_pt: dict[str, str],
    ) -> list[NavigationEdge]:
        """Build page-type-level navigation edges from action results."""
        # Aggregate by (from_pt, to_pt, action_type) for deduplication
        edge_key = tuple[str, str, str]
        edge_data: dict[edge_key, dict[str, Any]] = {}

        for action_result in result.results:
            # Skip non-transitions
            if action_result.outcome in (
                OutcomeType.NO_CHANGE,
                OutcomeType.TIMEOUT,
                OutcomeType.EXCEPTION,
            ):
                continue

            from_pt = state_to_pt.get(action_result.source_state_id)
            to_pt = state_to_pt.get(action_result.target_state_id)

            if not from_pt or not to_pt or from_pt == to_pt:
                continue

            action = result.actions.get(action_result.action_id)
            if not action:
                continue

            key = (from_pt, to_pt, action.action_type.value)
            if key not in edge_data:
                edge_data[key] = {
                    "trigger": action.label,
                    "action_type": action.action_type,
                    "outcome": action_result.outcome,
                    "count": 0,
                    "example_action_id": action_result.action_id,
                }
            edge_data[key]["count"] += 1

        edges = [
            NavigationEdge(
                from_page_type=key[0],
                to_page_type=key[1],
                trigger=data["trigger"],
                action_type=data["action_type"],
                outcome=data["outcome"],
                occurrence_count=data["count"],
                example_action_id=data["example_action_id"],
            )
            for key, data in edge_data.items()
        ]

        return edges

    # -- Step 4: summary ----------------------------------------------------

    def _build_summary(
        self,
        page_types: list[PageType],
        nav_edges: list[NavigationEdge],
        scenarios: list[Any],
    ) -> SiteModelSummary:
        notes: list[str] = []

        # Check for orphan page types (no outgoing edges)
        pt_ids = {pt.page_type_id for pt in page_types}
        from_pts = {e.from_page_type for e in nav_edges}
        orphans = pt_ids - from_pts
        for pt in page_types:
            if pt.page_type_id in orphans and len(page_types) > 1:
                notes.append(f"'{pt.name}' has no outgoing navigation edges")

        # Check for features without scenarios
        for pt in page_types:
            if "has_search" in pt.features:
                has_search_scenario = any(
                    getattr(s, "template", "") == "search" for s in scenarios
                )
                if not has_search_scenario:
                    notes.append(
                        f"Search found on '{pt.name}' but no search scenario generated"
                    )

        # Archetype distribution
        arch_dist: dict[str, int] = defaultdict(int)
        for pt in page_types:
            arch_dist[pt.archetype.value] += pt.instance_count

        return SiteModelSummary(
            total_page_types=len(page_types),
            total_navigation_edges=len(nav_edges),
            total_scenarios=len(scenarios),
            coverage_notes=notes,
            archetype_distribution=dict(arch_dist),
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _infer_page_type_name(
    archetype: PageArchetype,
    urls: list[str],
    heading_hierarchy: list[str],
    titles: list[str],
) -> str:
    """Derive a human-readable name for a page type."""
    # Try to find a common meaningful word from titles
    subject = _common_subject_from_titles(titles)

    archetype_label = {
        PageArchetype.LISTING: "Listing",
        PageArchetype.DETAIL: "Detail",
        PageArchetype.SEARCH_RESULTS: "Search Results",
        PageArchetype.FORM: "Form",
        PageArchetype.LANDING: "Landing",
        PageArchetype.ERROR: "Error",
        PageArchetype.UNKNOWN: "Page",
    }.get(archetype, "Page")

    if subject:
        return f"{subject} {archetype_label}"

    # Try headings
    if heading_hierarchy:
        # Use first heading as subject
        h1 = heading_hierarchy[0].strip()
        if h1 and len(h1) <= 30:
            return f"{h1} {archetype_label}"

    # Try URL path
    if urls:
        path_subject = _subject_from_url(urls[0])
        if path_subject:
            return f"{path_subject} {archetype_label}"

    return archetype_label


def _common_subject_from_titles(titles: list[str]) -> str:
    """Find a meaningful common word across page titles."""
    if not titles:
        return ""

    # Tokenize and find common words (excluding stop words)
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "for",
        "on",
        "at",
        "by",
        "is",
        "it",
        "page",
        "home",
        "|",
        "-",
        "—",
    }

    word_counts: dict[str, int] = defaultdict(int)
    for title in titles:
        words = set(re.findall(r"\b\w+\b", title))
        for word in words:
            lower = word.lower()
            if lower not in stop_words and len(lower) > 2:
                word_counts[lower] = word_counts.get(lower, 0) + 1

    if not word_counts:
        return ""

    # Find words that appear in most titles
    threshold = max(1, len(titles) // 2)
    common = [w for w, c in word_counts.items() if c >= threshold]
    if not common:
        return ""

    # Pick the most frequent, then title-case it
    best = max(common, key=lambda w: word_counts[w])
    return best.capitalize()


def _subject_from_url(url: str) -> str:
    """Extract a subject word from a URL path."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    if not path or path == "/":
        return ""

    segments = [s for s in path.split("/") if s]
    # Use the last meaningful non-dynamic segment
    for seg in reversed(segments):
        if not _DYNAMIC_SEGMENT.match(seg):
            # Clean: replace dashes/underscores, title-case
            clean = re.sub(r"[-_]", " ", seg).strip()
            if clean and len(clean) <= 30:
                return clean.title()

    return ""


def _infer_url_pattern(urls: list[str]) -> str:
    """Derive a regex pattern matching all instance URLs."""
    if not urls:
        return ""
    if len(urls) == 1:
        return re.escape(urls[0])

    # Parse all URLs
    parsed = [urlparse(u) for u in urls]

    # All should share the same scheme + netloc
    scheme = parsed[0].scheme
    netloc = parsed[0].netloc

    # Split paths into segments
    path_lists = [p.path.rstrip("/").split("/") for p in parsed]

    # Find max segment count
    max_len = max(len(p) for p in path_lists)

    pattern_parts: list[str] = []
    for i in range(max_len):
        segments_at_i = {p[i] for p in path_lists if i < len(p)}
        if len(segments_at_i) == 1:
            # All same → literal
            pattern_parts.append(re.escape(segments_at_i.pop()))
        else:
            # Varying → wildcard
            pattern_parts.append("[^/]+")

    path_pattern = "/".join(pattern_parts)

    # Check query params
    query_parts = {p.query for p in parsed}
    if len(query_parts) == 1 and query_parts.pop():
        return f"{scheme}://{netloc}/{path_pattern}\\?.*"

    return f"{scheme}://{netloc}/{path_pattern}"


def _url_to_template(url: str) -> str:
    """Convert a URL to a path template for grouping (fallback mode)."""
    parsed = urlparse(url)
    segments = parsed.path.rstrip("/").split("/")
    template_parts = []
    for seg in segments:
        if _DYNAMIC_SEGMENT.match(seg):
            template_parts.append("{id}")
        else:
            template_parts.append(seg)
    return f"{parsed.scheme}://{parsed.netloc}{'/'.join(template_parts)}"

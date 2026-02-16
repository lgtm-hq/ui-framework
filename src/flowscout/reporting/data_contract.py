"""Typed report data contract for the SPA dashboard.

Defines the JSON shape that the SolidJS SPA reads via
``window.__REPORT_DATA__``. The ``build_report_data()`` builder reuses
existing helper functions in ``html.py`` and packages everything into a
single validated ``ReportData`` Pydantic model.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Sub-models — each corresponds to a top-level section of the report
# ---------------------------------------------------------------------------


class ReportMeta(BaseModel):
    """Crawl run metadata."""

    start_url: str = ""
    started_at: str = ""
    finished_at: str = ""
    duration_seconds: float = 0.0
    strategy: str = "priority"
    version: str = ""
    schema_version: str = ""
    environment: str = ""
    input_profile: str = "safe"


class CrawlSummary(BaseModel):
    """High-level stats for the dashboard landing."""

    total_states: int = 0
    total_actions: int = 0
    total_results: int = 0
    total_flows: int = 0
    total_test_steps: int = 0
    flow_counts: dict[str, int] = Field(default_factory=dict)
    step_verdicts: dict[str, int] = Field(default_factory=dict)
    coverage: dict[str, Any] = Field(default_factory=dict)
    site_structure: dict[str, int] = Field(default_factory=dict)
    top_issues: list[ReportIssue] = Field(default_factory=list)
    blocked_summary: dict[str, Any] = Field(default_factory=dict)


class ReportIssue(BaseModel):
    """An actionable issue surfaced on the dashboard."""

    priority: str = "medium"
    title: str = ""
    detail: str = ""
    link_kind: str = ""
    link_value: str = ""


class PageReportEntry(BaseModel):
    """A single catalog element inside a page drilldown."""

    label: str = ""
    selector: str = ""
    dom_id: str = ""
    element_type: str = ""
    zone_type: str = ""
    tag: str = ""
    aria_role: str = ""
    input_type: str = ""
    is_visible: bool = True
    is_interactive: bool = False
    screenshot_link: str | None = None
    screenshot_source: str = ""


class PageReport(BaseModel):
    """Per-state page breakdown with element inventory."""

    state_id: str
    state_short: str = ""
    title: str = ""
    url: str = ""
    depth: int = 0
    interactive: int = 0
    non_interactive: int = 0
    total: int = 0
    visible: int = 0
    hidden: int = 0
    catalog_entry_count: int = 0
    entries_truncated: bool = False
    entries: list[PageReportEntry] = Field(default_factory=list)
    top_types: list[dict[str, Any]] = Field(default_factory=list)
    top_zones: list[dict[str, Any]] = Field(default_factory=list)


class FlowInstanceReport(BaseModel):
    """One instance of a flow template."""

    flow_id: str
    name: str = ""
    status: str = "warn"
    stability_score: float = 0.0
    depth: int = 0
    tags: list[str] = Field(default_factory=list)


class FlowTemplateReport(BaseModel):
    """A deduplicated flow template card."""

    template_id: str
    anchor_id: str = ""
    name: str = ""
    occurrence_count: int = 0
    stability_score: float = 0.0
    stability_pct: int = 0
    stability_bucket: str = "stable"
    template_type: str = "unknown"
    tags: list[str] = Field(default_factory=list)
    stable_count: int = 0
    fail_count: int = 0
    warn_count: int = 0
    representative_rows: list[dict[str, Any]] = Field(default_factory=list)
    instances: list[FlowInstanceReport] = Field(default_factory=list)


class FlowInstanceCard(BaseModel):
    """Flat instance card for the instance-centric view."""

    instance_id: str
    template_id: str
    template_name: str = ""
    flow_id: str
    flow_name: str = ""
    status: str = "warn"
    stability_score: float = 0.0
    stability_pct: int = 0
    depth: int = 0
    tags: list[str] = Field(default_factory=list)
    summary: str = ""


class GraphNode(BaseModel):
    """A node in the site-map graph."""

    id: str
    label: str = ""
    archetype: str = ""
    instance_count: int = 0
    url_pattern: str = ""
    quality_score: int = 0
    anchor_id: str = ""


class GraphEdge(BaseModel):
    """An edge in the site-map graph."""

    source: str
    target: str
    action_type: str = ""
    action_label: str = ""
    occurrence_count: int = 0
    outcome: str = ""
    uncovered: bool = False
    flow_id: str = ""
    template_id: str = ""


class GraphData(BaseModel):
    """Site-map graph for visualization."""

    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)


class CoverageMetric(BaseModel):
    """A single coverage dimension (state/edge/path)."""

    pct: int = 0
    covered: int = 0
    total: int = 0
    uncovered: list[Any] = Field(default_factory=list)


class CoverageReport(BaseModel):
    """Coverage metrics from MBT analysis."""

    state: CoverageMetric = Field(default_factory=CoverageMetric)
    edge: CoverageMetric = Field(default_factory=CoverageMetric)
    path: CoverageMetric = Field(default_factory=CoverageMetric)
    actions: list[str] = Field(default_factory=list)
    matrix_rows: list[dict[str, Any]] = Field(default_factory=list)
    page_coverage: list[dict[str, Any]] = Field(default_factory=list)


class TimelineEntry(BaseModel):
    """A single row in the execution timeline."""

    index: int = 0
    source_state_id: str = ""
    target_state_id: str = ""
    source_state_short: str = ""
    target_state_short: str = ""
    source_page: str = ""
    target_page: str = ""
    action_id: str = ""
    action_label: str = ""
    action_type: str = ""
    target_selector: str = ""
    dom_id: str = ""
    outcome: str = ""
    outcome_display: str = ""
    verdict: str = "warn"
    confidence_pct: int = 0
    duration_ms: int = 0
    url_before: str = ""
    url_after: str = ""
    message: str = ""
    error_messages: list[str] = Field(default_factory=list)
    console_errors: list[str] = Field(default_factory=list)
    transition_kind: str = ""
    transition_detail: str = ""
    navigation_status: int | None = None
    network_errors: list[dict[str, Any]] = Field(default_factory=list)
    redirect_chain: list[dict[str, Any]] = Field(default_factory=list)
    screenshot_link: str | None = None
    input_source: str = ""
    input_profile: str = ""
    display: dict[str, str] = Field(default_factory=dict)
    flow_context: dict[str, Any] = Field(default_factory=dict)


class LocatorHealthRow(BaseModel):
    """Locator quality per page type."""

    name: str = ""
    anchor_id: str = ""
    quality_score: int = 0
    instance_count: int = 0
    fragile_count: int = 0
    recommendation: str = ""


class FlakyAction(BaseModel):
    """An action with inconsistent outcomes."""

    source_page: str = ""
    action_label: str = ""
    outcomes: list[str] = Field(default_factory=list)
    occurrences: int = 0
    flow_id: str = ""
    template_id: str = ""


class LowStabilityStep(BaseModel):
    """An execution step with low confidence."""

    step_index: int = 0
    source_page: str = ""
    action_label: str = ""
    confidence_pct: int = 0
    confidence_reason: str = ""
    detail: str = ""
    flow_id: str = ""
    flow_name: str = ""
    flow_step: int = 0
    template_id: str = ""
    severity: str = "low"


class QualityReport(BaseModel):
    """Locator health, flaky actions, and recommendations."""

    locator_health_rows: list[LocatorHealthRow] = Field(default_factory=list)
    flaky_actions: list[FlakyAction] = Field(default_factory=list)
    low_stability_steps: list[LowStabilityStep] = Field(default_factory=list)
    recommendations: list[ReportIssue] = Field(default_factory=list)
    locator_issue_count: int = 0
    flaky_action_count: int = 0
    low_stability_count: int = 0
    locator_quality_rows: list[dict[str, Any]] = Field(default_factory=list)
    locator_recommendations: list[str] = Field(default_factory=list)


class BlockedPage(BaseModel):
    """A state blocked by WAF/403/captcha."""

    state_id: str
    state_short: str = ""
    title: str = ""
    url: str = ""
    reason: str = ""
    reason_label: str = ""
    detail: str = ""
    screenshot_link: str | None = None


class PageObjectCard(BaseModel):
    """Per-page-type object card with locators and code preview."""

    page_type_id: str
    anchor_id: str = ""
    name: str = ""
    class_name: str = ""
    archetype: str = ""
    url_pattern: str = ""
    instance_count: int = 0
    quality_score: int = 0
    quality_tone: str = "good"
    is_changed: bool = False
    locator_rows: list[dict[str, Any]] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    code_preview: dict[str, str] = Field(default_factory=dict)


class CrossRunComparison(BaseModel):
    """Diff against a previous exploration run."""

    has_previous_run: bool = False
    previous_run_id: str = ""
    previous_started_at: str = ""
    new_pages: int = 0
    disappeared_pages: int = 0
    changed_locators: int = 0
    new_page_examples: list[str] = Field(default_factory=list)
    disappeared_page_examples: list[str] = Field(default_factory=list)
    locator_changes: list[dict[str, Any]] = Field(default_factory=list)
    changed_page_type_ids: list[str] = Field(default_factory=list)


class InputProvenance(BaseModel):
    """Summary of generated input value sources."""

    profile: str = "safe"
    fill_actions: int = 0
    source_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    samples: list[dict[str, str]] = Field(default_factory=list)


class DiscoveryTimelineRow(BaseModel):
    """Per-state discovery progression row."""

    order: int = 0
    state_id: str = ""
    state_short: str = ""
    title: str = ""
    url: str = ""
    depth: int = 0
    interactive: int = 0
    non_interactive: int = 0
    total: int = 0
    new_elements: int = 0


class UrlInventoryRow(BaseModel):
    """URL-level aggregated element inventory."""

    title: str = ""
    url: str = ""
    interactive_elements: int = 0
    non_interactive_elements: int = 0
    total_elements: int = 0
    state_count: int = 0
    state_ids: list[str] = Field(default_factory=list)
    state_ids_short: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Top-level report data
# ---------------------------------------------------------------------------


class ReportData(BaseModel):
    """Complete typed report data contract for the SPA dashboard."""

    meta: ReportMeta = Field(default_factory=ReportMeta)
    summary: CrawlSummary = Field(default_factory=CrawlSummary)
    pages: dict[str, PageReport] = Field(default_factory=dict)
    flow_templates: list[FlowTemplateReport] = Field(default_factory=list)
    flow_instances: list[FlowInstanceCard] = Field(default_factory=list)
    graph: GraphData = Field(default_factory=GraphData)
    coverage: CoverageReport = Field(default_factory=CoverageReport)
    timeline: list[TimelineEntry] = Field(default_factory=list)
    quality: QualityReport = Field(default_factory=QualityReport)
    blocked_pages: list[BlockedPage] = Field(default_factory=list)
    page_objects: list[PageObjectCard] = Field(default_factory=list)
    cross_run: CrossRunComparison = Field(default_factory=CrossRunComparison)
    input_provenance: InputProvenance = Field(default_factory=InputProvenance)
    discovery_timeline: list[DiscoveryTimelineRow] = Field(default_factory=list)
    url_inventory: list[UrlInventoryRow] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Builder — converts ExplorationResult into ReportData
# ---------------------------------------------------------------------------


def build_report_data(
    result: Any,
    *,
    report_dir: Path | None = None,
) -> ReportData:
    """Build typed report data from an ExplorationResult.

    Delegates to existing ``ReportDataBuilder`` in ``html.py`` for data
    computation, then maps the untyped dict into the typed contract.
    """
    from flowscout.reporting.html import ReportDataBuilder

    effective_report_dir = report_dir or Path.cwd()
    builder = ReportDataBuilder(result, report_dir=effective_report_dir)
    ctx = builder.build()

    return _map_context_to_report_data(ctx, result=result)


def _map_context_to_report_data(
    ctx: dict[str, Any],
    *,
    result: Any,
) -> ReportData:
    """Map the untyped template context dict to the typed ReportData model."""
    from flowscout import __version__

    meta = ReportMeta(
        start_url=str(ctx.get("start_url", "")),
        started_at=str(ctx.get("started_at", "")),
        finished_at=str(getattr(result, "finished_at", "")),
        duration_seconds=float(ctx.get("duration", 0.0)),
        strategy=str(ctx.get("config_strategy", "priority")),
        version=str(__version__),
        schema_version=str(getattr(result, "schema_version", "")),
        environment=str(result.config.get("environment", "")),
        input_profile=str(result.config.get("input_profile", "safe")),
    )

    flow_counts = ctx.get("flow_counts", {})
    coverage_data = ctx.get("coverage", {})
    step_verdicts = ctx.get("step_verdicts_summary", {})
    site_structure = ctx.get("site_structure_summary", {})
    blocked_summary = ctx.get("blocked_summary", {})
    top_issues_raw = ctx.get("dashboard_top_issues", [])

    summary = CrawlSummary(
        total_states=len(result.states),
        total_actions=len(result.actions),
        total_results=len(result.results),
        total_flows=len(result.flows),
        total_test_steps=int(ctx.get("total_test_steps", 0)),
        flow_counts=dict(flow_counts),
        step_verdicts=dict(step_verdicts),
        coverage=dict(coverage_data),
        site_structure=dict(site_structure),
        top_issues=[
            ReportIssue(**issue) for issue in top_issues_raw if isinstance(issue, dict)
        ],
        blocked_summary=dict(blocked_summary),
    )

    # Pages (element drilldown)
    pages: dict[str, PageReport] = {}
    drilldown_map = ctx.get("element_drilldown_map", {})
    for state_id, drilldown in drilldown_map.items():
        entries = [
            PageReportEntry(**entry)
            for entry in drilldown.get("entries", [])
            if isinstance(entry, dict)
        ]
        pages[state_id] = PageReport(
            state_id=str(drilldown.get("state_id", state_id)),
            state_short=str(drilldown.get("state_short", state_id[:8])),
            title=str(drilldown.get("title", "")),
            url=str(drilldown.get("url", "")),
            depth=int(drilldown.get("depth", 0)),
            interactive=int(drilldown.get("interactive", 0)),
            non_interactive=int(drilldown.get("non_interactive", 0)),
            total=int(drilldown.get("total", 0)),
            visible=int(drilldown.get("visible", 0)),
            hidden=int(drilldown.get("hidden", 0)),
            catalog_entry_count=int(drilldown.get("catalog_entry_count", 0)),
            entries_truncated=bool(drilldown.get("entries_truncated", False)),
            entries=entries,
            top_types=list(drilldown.get("top_types", [])),
            top_zones=list(drilldown.get("top_zones", [])),
        )

    # Flow templates
    flow_template_cards_raw = ctx.get("flow_template_cards", [])
    flow_templates = [
        FlowTemplateReport(
            template_id=str(card.get("template_id", "")),
            anchor_id=str(card.get("anchor_id", "")),
            name=str(card.get("name", "")),
            occurrence_count=int(card.get("occurrence_count", 0)),
            stability_score=float(card.get("stability_score", 0.0)),
            stability_pct=int(card.get("stability_pct", 0)),
            stability_bucket=str(card.get("stability_bucket", "stable")),
            template_type=str(card.get("template_type", "unknown")),
            tags=list(card.get("tags", [])),
            stable_count=int(card.get("stable_count", 0)),
            fail_count=int(card.get("fail_count", 0)),
            warn_count=int(card.get("warn_count", 0)),
            representative_rows=list(card.get("representative_rows", [])),
            instances=[
                FlowInstanceReport(**inst)
                for inst in card.get("instances", [])
                if isinstance(inst, dict)
            ],
        )
        for card in flow_template_cards_raw
        if isinstance(card, dict)
    ]

    # Flow instance cards
    flow_instance_cards_raw = ctx.get("flow_instance_cards", [])
    flow_instances = [
        FlowInstanceCard(**card)
        for card in flow_instance_cards_raw
        if isinstance(card, dict)
    ]

    # Graph
    graph_raw = ctx.get("graph_json", {})
    graph = GraphData(
        nodes=[
            GraphNode(**node)
            for node in graph_raw.get("nodes", [])
            if isinstance(node, dict)
        ],
        edges=[
            GraphEdge(**edge)
            for edge in graph_raw.get("edges", [])
            if isinstance(edge, dict)
        ],
    )

    # Coverage (MBT)
    mbt_raw = ctx.get("mbt_coverage", {})
    coverage = CoverageReport(
        page_coverage=list(ctx.get("page_coverage_map", [])),
    )
    if mbt_raw:
        for dimension in ("state", "edge", "path"):
            dim_data = mbt_raw.get(dimension, {})
            if isinstance(dim_data, dict):
                setattr(
                    coverage,
                    dimension,
                    CoverageMetric(
                        pct=int(dim_data.get("pct", 0)),
                        covered=int(dim_data.get("covered", 0)),
                        total=int(dim_data.get("total", 0)),
                        uncovered=list(dim_data.get("uncovered", [])),
                    ),
                )
        coverage.actions = list(mbt_raw.get("actions", []))
        coverage.matrix_rows = list(mbt_raw.get("matrix_rows", []))

    # Timeline
    human_rows = ctx.get("human_execution_rows", [])
    execution_step_map = ctx.get("execution_step_map", {})
    timeline = [
        TimelineEntry(
            index=int(row.get("index", 0)),
            source_state_id=str(row.get("source_state_id", "")),
            target_state_id=str(row.get("target_state_id", "")),
            source_state_short=str(row.get("source_state_short", "")),
            target_state_short=str(row.get("target_state_short", "")),
            source_page=str(row.get("source_page", "")),
            target_page=str(row.get("target_page", "")),
            action_id=str(row.get("action_id", "")),
            action_label=str(row.get("action_label", "")),
            action_type=str(row.get("action_type", "")),
            target_selector=str(row.get("target_selector", "")),
            dom_id=str(row.get("dom_id", "")),
            outcome=str(row.get("outcome", "")),
            outcome_display=str(row.get("outcome_display", "")),
            verdict=str(row.get("verdict", "warn")),
            confidence_pct=int(row.get("confidence_pct", 0)),
            duration_ms=int(row.get("duration_ms", 0)),
            url_before=str(row.get("url_before", "")),
            url_after=str(row.get("url_after", "")),
            message=str(row.get("message", "")),
            error_messages=list(row.get("error_messages", [])),
            console_errors=list(row.get("console_errors", [])),
            transition_kind=str(row.get("transition_kind", "")),
            transition_detail=str(row.get("transition_detail", "")),
            navigation_status=row.get("navigation_status"),
            network_errors=list(row.get("network_errors", [])),
            redirect_chain=list(row.get("redirect_chain", [])),
            screenshot_link=row.get("screenshot_link"),
            input_source=str(row.get("input_source", "")),
            input_profile=str(row.get("input_profile", "")),
            display=dict(row.get("display", {})),
            flow_context=dict(execution_step_map.get(int(row.get("index", 0)), {})),
        )
        for row in human_rows
        if isinstance(row, dict)
    ]

    # Quality
    quality_raw = ctx.get("quality_insights", {})
    quality = QualityReport(
        locator_health_rows=[
            LocatorHealthRow(**row)
            for row in quality_raw.get("locator_health_rows", [])
            if isinstance(row, dict)
        ],
        flaky_actions=[
            FlakyAction(**row)
            for row in quality_raw.get("flaky_actions", [])
            if isinstance(row, dict)
        ],
        low_stability_steps=[
            LowStabilityStep(**row)
            for row in quality_raw.get("low_stability_steps", [])
            if isinstance(row, dict)
        ],
        recommendations=[
            ReportIssue(**row)
            for row in quality_raw.get("recommendations", [])
            if isinstance(row, dict)
        ],
        locator_issue_count=int(quality_raw.get("locator_issue_count", 0)),
        flaky_action_count=int(quality_raw.get("flaky_action_count", 0)),
        low_stability_count=int(quality_raw.get("low_stability_count", 0)),
        locator_quality_rows=list(ctx.get("locator_quality_rows", [])),
        locator_recommendations=list(ctx.get("locator_recommendations", [])),
    )

    # Blocked pages
    blocked_raw = ctx.get("blocked_states", [])
    blocked_pages = [BlockedPage(**row) for row in blocked_raw if isinstance(row, dict)]

    # Page objects
    page_object_cards_raw = ctx.get("page_object_cards", [])
    page_objects = [
        PageObjectCard(**card)
        for card in page_object_cards_raw
        if isinstance(card, dict)
    ]

    # Cross-run comparison
    cross_run_raw = ctx.get("cross_run_comparison", {})
    cross_run = (
        CrossRunComparison(**cross_run_raw) if cross_run_raw else CrossRunComparison()
    )

    # Input provenance
    input_prov_raw = ctx.get("input_provenance", {})
    input_provenance = (
        InputProvenance(**input_prov_raw) if input_prov_raw else InputProvenance()
    )

    # Discovery timeline
    discovery_raw = ctx.get("discovery_timeline", [])
    discovery_timeline = [
        DiscoveryTimelineRow(**row) for row in discovery_raw if isinstance(row, dict)
    ]

    # URL inventory
    url_inv_raw = ctx.get("url_inventory_rows", [])
    url_inventory = [
        UrlInventoryRow(**row) for row in url_inv_raw if isinstance(row, dict)
    ]

    return ReportData(
        meta=meta,
        summary=summary,
        pages=pages,
        flow_templates=flow_templates,
        flow_instances=flow_instances,
        graph=graph,
        coverage=coverage,
        timeline=timeline,
        quality=quality,
        blocked_pages=blocked_pages,
        page_objects=page_objects,
        cross_run=cross_run,
        input_provenance=input_provenance,
        discovery_timeline=discovery_timeline,
        url_inventory=url_inventory,
    )

"""Tests for the ReportData data contract and builder."""

from pathlib import Path

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.state import PageBlockReason, PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.reporting.data_contract import (
    BlockedPage,
    CrawlSummary,
    CrossRunComparison,
    FlowInstanceCard,
    FlowInstanceReport,
    FlowTemplateReport,
    GraphData,
    GraphEdge,
    GraphNode,
    InputProvenance,
    PageObjectCard,
    PageReport,
    PageReportEntry,
    ReportData,
    ReportIssue,
    ReportMeta,
    TimelineEntry,
    build_report_data,
)


def _make_state(
    state_id: str = "abc123def456",
    url: str = "https://example.com",
    title: str = "Example",
    depth: int = 0,
    **kwargs: object,
) -> PageState:
    defaults = {
        "state_id": state_id,
        "url": url,
        "title": title,
        "fingerprint": state_id.ljust(64, "0"),
        "depth": depth,
        "dom_structure_hash": "dom1",
        "visible_text_hash": "text1",
        "form_state_hash": "form1",
    }
    defaults.update(kwargs)
    return PageState.model_validate(defaults)


def _make_action(
    action_id: str = "act1",
    action_type: ActionType = ActionType.CLICK,
    selector: str = "button#test",
    label: str = "Click: Test",
) -> Action:
    return Action(
        action_id=action_id,
        action_type=action_type,
        target_selector=selector,
        label=label,
    )


def _make_result(
    action_id: str = "act1",
    source: str = "abc123def456",
    target: str = "abc123def456",
    outcome: OutcomeType = OutcomeType.NO_CHANGE,
) -> ActionResult:
    return ActionResult(
        action_id=action_id,
        source_state_id=source,
        target_state_id=target,
        outcome=outcome,
        stability_score=0.9,
    )


def _make_exploration_result(**kwargs: object) -> ExplorationResult:
    defaults: dict[str, object] = {
        "config": {"start_url": "https://example.com", "strategy": "priority"},
        "started_at": "2026-01-01T00:00:00Z",
        "finished_at": "2026-01-01T00:01:00Z",
        "duration_seconds": 60.0,
    }
    defaults.update(kwargs)
    return ExplorationResult.model_validate(defaults)


class TestSubModels:
    def test_report_meta_defaults(self) -> None:
        meta = ReportMeta()
        assert meta.start_url == ""
        assert meta.strategy == "priority"

    def test_crawl_summary_defaults(self) -> None:
        summary = CrawlSummary()
        assert summary.total_states == 0
        assert summary.top_issues == []

    def test_report_issue_roundtrip(self) -> None:
        issue = ReportIssue(
            priority="high",
            title="Fix locators",
            detail="3 fragile locators",
            link_kind="page_object",
            link_value="home-page",
        )
        data = issue.model_dump()
        restored = ReportIssue.model_validate(data)
        assert restored.priority == "high"
        assert restored.title == "Fix locators"

    def test_page_report_entry_fields(self) -> None:
        entry = PageReportEntry(
            label="Submit",
            selector="button.submit",
            element_type="button",
            is_interactive=True,
        )
        assert entry.is_visible is True
        assert entry.is_interactive is True

    def test_graph_data_structure(self) -> None:
        graph = GraphData(
            nodes=[GraphNode(id="p1", label="Home")],
            edges=[GraphEdge(source="p1", target="p2", action_type="click")],
        )
        assert len(graph.nodes) == 1
        assert graph.edges[0].action_type == "click"

    def test_timeline_entry_defaults(self) -> None:
        entry = TimelineEntry(index=1, outcome="navigation")
        assert entry.verdict == "warn"
        assert entry.navigation_status is None

    def test_blocked_page_fields(self) -> None:
        page = BlockedPage(
            state_id="blocked1",
            reason="access_denied",
            reason_label="Access Denied",
        )
        assert page.screenshot_link is None

    def test_flow_template_report(self) -> None:
        template = FlowTemplateReport(
            template_id="t1",
            name="Login Flow",
            occurrence_count=3,
            instances=[
                FlowInstanceReport(flow_id="f1", status="pass"),
                FlowInstanceReport(flow_id="f2", status="fail"),
            ],
        )
        assert template.occurrence_count == 3
        assert len(template.instances) == 2

    def test_flow_instance_card(self) -> None:
        card = FlowInstanceCard(
            instance_id="t1-f1",
            template_id="t1",
            flow_id="f1",
            status="pass",
            stability_pct=95,
        )
        assert card.stability_pct == 95

    def test_cross_run_comparison_defaults(self) -> None:
        comparison = CrossRunComparison()
        assert comparison.has_previous_run is False
        assert comparison.new_pages == 0

    def test_input_provenance_defaults(self) -> None:
        prov = InputProvenance()
        assert prov.profile == "safe"
        assert prov.fill_actions == 0

    def test_page_object_card(self) -> None:
        card = PageObjectCard(
            page_type_id="pt1",
            name="Home",
            quality_score=85,
            quality_tone="good",
        )
        assert card.quality_tone == "good"


class TestReportData:
    def test_defaults_valid(self) -> None:
        data = ReportData()
        assert data.meta.start_url == ""
        assert data.summary.total_states == 0
        assert data.pages == {}
        assert data.flow_templates == []
        assert data.timeline == []
        assert data.blocked_pages == []

    def test_json_roundtrip(self) -> None:
        data = ReportData(
            meta=ReportMeta(start_url="https://example.com", version="1.0.0"),
            summary=CrawlSummary(total_states=5, total_flows=3),
        )
        json_str = data.model_dump_json()
        restored = ReportData.model_validate_json(json_str)
        assert restored.meta.start_url == "https://example.com"
        assert restored.summary.total_states == 5
        assert restored.summary.total_flows == 3

    def test_full_structure_serializable(self) -> None:
        data = ReportData(
            meta=ReportMeta(start_url="https://example.com"),
            summary=CrawlSummary(
                total_states=2,
                top_issues=[ReportIssue(title="Fix it")],
            ),
            pages={
                "state1": PageReport(
                    state_id="state1",
                    entries=[
                        PageReportEntry(label="Btn", selector="button"),
                    ],
                ),
            },
            graph=GraphData(
                nodes=[GraphNode(id="p1", label="Home")],
                edges=[GraphEdge(source="p1", target="p2")],
            ),
            blocked_pages=[
                BlockedPage(state_id="b1", reason="captcha"),
            ],
            timeline=[TimelineEntry(index=1, outcome="navigation")],
        )
        dumped = data.model_dump()
        assert dumped["meta"]["start_url"] == "https://example.com"
        assert len(dumped["pages"]) == 1
        assert len(dumped["graph"]["nodes"]) == 1
        assert len(dumped["blocked_pages"]) == 1
        assert len(dumped["timeline"]) == 1


class TestBuildReportData:
    def test_empty_result_produces_valid_data(self) -> None:
        result = _make_exploration_result()
        data = build_report_data(result)

        assert isinstance(data, ReportData)
        assert data.meta.start_url == "https://example.com"
        assert data.summary.total_states == 0
        assert data.summary.total_flows == 0
        assert data.pages == {}
        assert data.timeline == []

    def test_with_states_and_actions(self, tmp_path: Path) -> None:
        state = _make_state()
        action = _make_action()
        action_result = _make_result()

        result = _make_exploration_result(
            states={"abc123def456": state.model_dump()},
            actions={"act1": action.model_dump()},
            results=[action_result.model_dump()],
        )
        data = build_report_data(result, report_dir=tmp_path)

        assert data.summary.total_states == 1
        assert data.summary.total_actions == 1
        assert data.summary.total_results == 1
        assert len(data.timeline) == 1
        assert data.timeline[0].outcome == "no_change"

    def test_with_flows(self, tmp_path: Path) -> None:
        state = _make_state()
        action = _make_action()
        action_result = _make_result()

        flow = Flow(
            flow_id="flow1",
            name="Test flow",
            description="A test flow",
            state_ids=["abc123def456"],
            action_ids=["act1"],
            outcomes=[OutcomeType.NO_CHANGE],
            depth=1,
            stability_score=0.9,
            is_stable=True,
        )

        result = _make_exploration_result(
            states={"abc123def456": state.model_dump()},
            actions={"act1": action.model_dump()},
            results=[action_result.model_dump()],
            flows=[flow.model_dump()],
        )
        data = build_report_data(result, report_dir=tmp_path)

        assert data.summary.total_flows == 1
        assert data.summary.flow_counts["pass"] == 1

    def test_with_blocked_states(self, tmp_path: Path) -> None:
        blocked = _make_state(
            state_id="blocked123456",
            title="Blocked",
            block_reason=PageBlockReason.ACCESS_DENIED,
            block_detail="HTTP 403",
        )
        result = _make_exploration_result(
            states={"blocked123456": blocked.model_dump()},
        )
        data = build_report_data(result, report_dir=tmp_path)

        assert len(data.blocked_pages) == 1
        assert data.blocked_pages[0].reason == "access_denied"

    def test_meta_populated(self) -> None:
        result = _make_exploration_result()
        data = build_report_data(result)

        assert data.meta.started_at == "2026-01-01T00:00:00Z"
        assert data.meta.duration_seconds == 60.0
        assert data.meta.strategy == "priority"
        assert data.meta.version != ""

    def test_coverage_populated(self, tmp_path: Path) -> None:
        state = _make_state()
        action = _make_action()
        action_result = _make_result()

        result = _make_exploration_result(
            states={"abc123def456": state.model_dump()},
            actions={"act1": action.model_dump()},
            results=[action_result.model_dump()],
        )
        data = build_report_data(result, report_dir=tmp_path)

        page_cov = data.summary.coverage.get("page", {})
        assert isinstance(page_cov, dict)
        assert "total" in page_cov

    def test_cross_run_defaults(self, tmp_path: Path) -> None:
        result = _make_exploration_result()
        data = build_report_data(result, report_dir=tmp_path)

        assert data.cross_run.has_previous_run is False

    def test_serializes_to_json(self, tmp_path: Path) -> None:
        result = _make_exploration_result()
        data = build_report_data(result, report_dir=tmp_path)

        json_str = data.model_dump_json()
        restored = ReportData.model_validate_json(json_str)
        assert restored.meta.start_url == "https://example.com"


class TestBuildIntegration:
    def test_inject_report_data_replaces_placeholder(self) -> None:
        from flowscout.reporting.build import inject_report_data

        shell = (
            '<script>window.__REPORT_DATA__ = "__REPORT_DATA_PLACEHOLDER__";</script>'
        )
        result_html = inject_report_data(html_shell=shell, report_json='{"meta":{}}')
        assert '"__REPORT_DATA_PLACEHOLDER__"' not in result_html
        assert '{"meta":{}}' in result_html

    def test_get_dashboard_shell_returns_html(self) -> None:
        from flowscout.reporting.build import get_dashboard_shell

        shell = get_dashboard_shell()
        assert "<html" in shell.lower()
        assert "__REPORT_DATA_PLACEHOLDER__" in shell

    def test_spa_report_generation(self, tmp_path: Path) -> None:
        from flowscout.reporting.html import HTMLReporter

        state = _make_state()
        action = _make_action()
        action_result = _make_result()

        result = _make_exploration_result(
            states={"abc123def456": state.model_dump()},
            actions={"act1": action.model_dump()},
            results=[action_result.model_dump()],
        )

        output_path = str(tmp_path / "report.html")
        reporter = HTMLReporter()
        reporter.generate(result, output_path)

        spa_path = tmp_path / "report-spa.html"
        data_path = tmp_path / "report-data.json"

        assert spa_path.exists(), "SPA report should be generated"
        assert data_path.exists(), "report-data.json should be generated"

        spa_html = spa_path.read_text()
        assert '"__REPORT_DATA_PLACEHOLDER__"' not in spa_html
        assert "https://example.com" in spa_html

        data_json = data_path.read_text()
        restored = ReportData.model_validate_json(data_json)
        assert restored.meta.start_url == "https://example.com"
        assert restored.summary.total_states == 1

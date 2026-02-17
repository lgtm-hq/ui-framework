import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import Summary from "../../components/tabs/Summary";
import type { ReportData } from "../../types";

function makeData(overrides: Partial<ReportData> = {}): ReportData {
  return {
    meta: {
      start_url: "https://example.com",
      started_at: "2026-01-15T10:00:00Z",
      finished_at: "2026-01-15T10:05:00Z",
      duration_seconds: 300,
      strategy: "priority-bfs",
      version: "2.0.0",
      schema_version: "2.0.0",
      environment: "chromium",
      input_profile: "default",
    },
    summary: {
      total_states: 8,
      total_actions: 24,
      total_results: 24,
      total_flows: 5,
      total_test_steps: 15,
      flow_counts: { pass: 3, fail: 1, warn: 1 },
      step_verdicts: {},
      coverage: {
        page: { tested: 6, total: 8, pct: 75 },
        interaction: { executed: 20, total: 24, pct: 83 },
        pass_rate: { passed: 3, total: 5, pct: 60 },
      },
      site_structure: {
        page_type_count: 4,
        navigation_path_count: 6,
        flow_template_count: 3,
        blocked_page_count: 0,
      },
      top_issues: [],
      blocked_summary: {},
    },
    pages: {},
    flow_templates: [],
    flow_instances: [],
    graph: { nodes: [], edges: [] },
    coverage: {
      state: { pct: 0, covered: 0, total: 0, uncovered: [] },
      edge: { pct: 0, covered: 0, total: 0, uncovered: [] },
      path: { pct: 0, covered: 0, total: 0, uncovered: [] },
      actions: [],
      matrix_rows: [],
      page_coverage: [],
    },
    timeline: [],
    quality: {
      locator_health_rows: [],
      flaky_actions: [],
      low_stability_steps: [],
      recommendations: [],
      locator_issue_count: 0,
      flaky_action_count: 0,
      low_stability_count: 0,
      locator_quality_rows: [],
      locator_recommendations: [],
    },
    blocked_pages: [],
    page_objects: [],
    cross_run: {
      has_previous_run: false,
      previous_run_id: "",
      previous_started_at: "",
      new_pages: 0,
      disappeared_pages: 0,
      changed_locators: 0,
      new_page_examples: [],
      disappeared_page_examples: [],
      locator_changes: [],
      changed_page_type_ids: [],
    },
    input_provenance: { profile: "", fill_actions: 0, source_breakdown: [], samples: [] },
    discovery_timeline: [],
    url_inventory: [],
    ...overrides,
  };
}

describe("Summary", () => {
  it("renders the start URL", () => {
    render(() => <Summary data={makeData()} />);
    expect(screen.getByText("https://example.com")).toBeInTheDocument();
  });

  it("renders stat cards with values", () => {
    render(() => <Summary data={makeData()} />);
    expect(screen.getByText("8")).toBeInTheDocument(); // States
    expect(screen.getByText("24")).toBeInTheDocument(); // Actions
    expect(screen.getByText("5")).toBeInTheDocument(); // Flows
    expect(screen.getByText("15")).toBeInTheDocument(); // Test Steps
  });

  it("renders coverage percentages", () => {
    render(() => <Summary data={makeData()} />);
    expect(screen.getByText("75%")).toBeInTheDocument();
    expect(screen.getByText("83%")).toBeInTheDocument();
    expect(screen.getByText("60%")).toBeInTheDocument();
  });

  it("renders verdict badges", () => {
    render(() => <Summary data={makeData()} />);
    expect(screen.getByText("pass: 3")).toBeInTheDocument();
    expect(screen.getByText("fail: 1")).toBeInTheDocument();
    expect(screen.getByText("warn: 1")).toBeInTheDocument();
  });

  it("renders site structure section", () => {
    render(() => <Summary data={makeData()} />);
    expect(screen.getByText("Site Structure")).toBeInTheDocument();
    expect(screen.getByText(/4 page types/)).toBeInTheDocument();
  });

  it("shows top issues when present", () => {
    const data = makeData();
    data.summary.top_issues = [
      { priority: "high", title: "Broken login", detail: "Form submit fails", link_kind: "", link_value: "" },
    ];
    render(() => <Summary data={data} />);
    expect(screen.getByText("Top Issues")).toBeInTheDocument();
    expect(screen.getByText("Broken login")).toBeInTheDocument();
  });

  it("hides top issues section when empty", () => {
    render(() => <Summary data={makeData()} />);
    expect(screen.queryByText("Top Issues")).not.toBeInTheDocument();
  });
});

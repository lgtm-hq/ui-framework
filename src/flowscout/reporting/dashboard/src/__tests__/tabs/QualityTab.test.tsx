import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import QualityTab from "../../components/tabs/quality/QualityTab";
import type { ReportData } from "../../types";

function makeData(overrides: Partial<ReportData> = {}): ReportData {
  return {
    meta: {
      start_url: "",
      started_at: "",
      finished_at: "",
      duration_seconds: 0,
      strategy: "",
      version: "",
      schema_version: "",
      environment: "",
      input_profile: "",
    },
    summary: {
      total_states: 0,
      total_actions: 0,
      total_results: 0,
      total_flows: 0,
      total_test_steps: 0,
      flow_counts: {},
      step_verdicts: {},
      coverage: {},
      site_structure: {},
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

describe("QualityTab", () => {
  it("renders the heading", () => {
    render(() => <QualityTab data={makeData()} />);
    expect(screen.getByText("Quality Signals")).toBeInTheDocument();
  });

  it("renders stat cards at zero with empty data", () => {
    render(() => <QualityTab data={makeData()} />);
    const zeros = screen.getAllByText("0");
    expect(zeros.length).toBeGreaterThanOrEqual(3);
  });

  it("renders stat cards with counts", () => {
    const data = makeData();
    data.quality.locator_issue_count = 2;
    data.quality.flaky_action_count = 1;
    data.quality.low_stability_count = 3;
    render(() => <QualityTab data={data} />);
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("1")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("shows recommendations when present", () => {
    const data = makeData();
    data.quality.recommendations = [
      { priority: "high", title: "Add data-testid", detail: "Fragile selectors detected", link_kind: "", link_value: "" },
    ];
    render(() => <QualityTab data={data} />);
    expect(screen.getByText("Recommendations")).toBeInTheDocument();
    expect(screen.getByText("Add data-testid")).toBeInTheDocument();
  });

  it("hides recommendation section when empty", () => {
    render(() => <QualityTab data={makeData()} />);
    expect(screen.queryByText("Recommendations")).not.toBeInTheDocument();
  });

  it("shows locator health table when rows exist", () => {
    const data = makeData();
    data.quality.locator_health_rows = [
      { name: "Home", anchor_id: "home", quality_score: 85, instance_count: 3, fragile_count: 1, recommendation: "Add IDs" },
    ];
    render(() => <QualityTab data={data} />);
    expect(screen.getByText("Locator Health")).toBeInTheDocument();
    expect(screen.getByText("Home")).toBeInTheDocument();
    expect(screen.getByText("85%")).toBeInTheDocument();
  });

  it("shows flaky actions when present", () => {
    const data = makeData();
    data.quality.flaky_actions = [
      { source_page: "Login", action_label: "Submit", outcomes: ["navigation", "timeout"], occurrences: 5, flow_id: "", template_id: "" },
    ];
    render(() => <QualityTab data={data} />);
    expect(screen.getByRole("heading", { name: "Flaky Actions" })).toBeInTheDocument();
    expect(screen.getByText("Login")).toBeInTheDocument();
  });

  it("shows blocked pages when present", () => {
    const data = makeData();
    data.blocked_pages = [
      { state_id: "s1", state_short: "s1", title: "Admin Panel", url: "/admin", reason: "403", reason_label: "Forbidden", detail: "Access denied", screenshot_link: null },
    ];
    render(() => <QualityTab data={data} />);
    expect(screen.getByText("Blocked Pages")).toBeInTheDocument();
    expect(screen.getByText("Admin Panel")).toBeInTheDocument();
  });

  it("hides all optional sections when data is empty", () => {
    render(() => <QualityTab data={makeData()} />);
    expect(screen.queryByText("Recommendations")).not.toBeInTheDocument();
    expect(screen.queryByText("Locator Health")).not.toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "Flaky Actions" })).not.toBeInTheDocument();
    expect(screen.queryByText("Low Stability Steps")).not.toBeInTheDocument();
    expect(screen.queryByText("Blocked Pages")).not.toBeInTheDocument();
  });
});

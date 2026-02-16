/** Reactive report data store. */

import { createSignal } from "solid-js";
import type { ReportData } from "../types";

function loadReportData(): ReportData {
  const raw = window.__REPORT_DATA__;
  if (typeof raw === "string") {
    try {
      return JSON.parse(raw) as ReportData;
    } catch {
      console.error("Failed to parse __REPORT_DATA__");
      return emptyReportData();
    }
  }
  return raw ?? emptyReportData();
}

function emptyReportData(): ReportData {
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
    input_provenance: {
      profile: "",
      fill_actions: 0,
      source_breakdown: [],
      samples: [],
    },
    discovery_timeline: [],
    url_inventory: [],
  };
}

const [reportData] = createSignal<ReportData>(loadReportData());

export { reportData };

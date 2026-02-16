/** TypeScript types matching the Python ReportData contract. */

export interface ReportMeta {
  start_url: string;
  started_at: string;
  finished_at: string;
  duration_seconds: number;
  strategy: string;
  version: string;
  schema_version: string;
  environment: string;
  input_profile: string;
}

export interface ReportIssue {
  priority: string;
  title: string;
  detail: string;
  link_kind: string;
  link_value: string;
}

export interface CrawlSummary {
  total_states: number;
  total_actions: number;
  total_results: number;
  total_flows: number;
  total_test_steps: number;
  flow_counts: Record<string, number>;
  step_verdicts: Record<string, number>;
  coverage: Record<string, unknown>;
  site_structure: Record<string, number>;
  top_issues: ReportIssue[];
  blocked_summary: Record<string, unknown>;
}

export interface PageReportEntry {
  label: string;
  selector: string;
  dom_id: string;
  element_type: string;
  zone_type: string;
  tag: string;
  aria_role: string;
  input_type: string;
  is_visible: boolean;
  is_interactive: boolean;
  screenshot_link: string | null;
  screenshot_source: string;
}

export interface PageReport {
  state_id: string;
  state_short: string;
  title: string;
  url: string;
  depth: number;
  interactive: number;
  non_interactive: number;
  total: number;
  visible: number;
  hidden: number;
  catalog_entry_count: number;
  entries_truncated: boolean;
  entries: PageReportEntry[];
  top_types: Array<{ name: string; count: number }>;
  top_zones: Array<{ name: string; count: number }>;
}

export interface FlowInstanceReport {
  flow_id: string;
  name: string;
  status: string;
  stability_score: number;
  depth: number;
  tags: string[];
}

export interface FlowTemplateReport {
  template_id: string;
  anchor_id: string;
  name: string;
  occurrence_count: number;
  stability_score: number;
  stability_pct: number;
  stability_bucket: string;
  template_type: string;
  tags: string[];
  stable_count: number;
  fail_count: number;
  warn_count: number;
  representative_rows: Record<string, unknown>[];
  instances: FlowInstanceReport[];
}

export interface FlowInstanceCard {
  instance_id: string;
  template_id: string;
  template_name: string;
  flow_id: string;
  flow_name: string;
  status: string;
  stability_score: number;
  stability_pct: number;
  depth: number;
  tags: string[];
  summary: string;
}

export interface GraphNode {
  id: string;
  label: string;
  archetype: string;
  instance_count: number;
  url_pattern: string;
  quality_score: number;
  anchor_id: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  action_type: string;
  action_label: string;
  occurrence_count: number;
  outcome: string;
  uncovered: boolean;
  flow_id: string;
  template_id: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface CoverageMetric {
  pct: number;
  covered: number;
  total: number;
  uncovered: unknown[];
}

export interface CoverageReport {
  state: CoverageMetric;
  edge: CoverageMetric;
  path: CoverageMetric;
  actions: string[];
  matrix_rows: Record<string, unknown>[];
  page_coverage: Record<string, unknown>[];
}

export interface TimelineEntry {
  index: number;
  source_state_id: string;
  target_state_id: string;
  source_state_short: string;
  target_state_short: string;
  source_page: string;
  target_page: string;
  action_id: string;
  action_label: string;
  action_type: string;
  target_selector: string;
  dom_id: string;
  outcome: string;
  outcome_display: string;
  verdict: string;
  confidence_pct: number;
  duration_ms: number;
  url_before: string;
  url_after: string;
  message: string;
  error_messages: string[];
  console_errors: string[];
  transition_kind: string;
  transition_detail: string;
  navigation_status: number | null;
  network_errors: Record<string, unknown>[];
  redirect_chain: Record<string, unknown>[];
  screenshot_link: string | null;
  input_source: string;
  input_profile: string;
  display: Record<string, string>;
  flow_context: Record<string, unknown>;
}

export interface LocatorHealthRow {
  name: string;
  anchor_id: string;
  quality_score: number;
  instance_count: number;
  fragile_count: number;
  recommendation: string;
}

export interface FlakyAction {
  source_page: string;
  action_label: string;
  outcomes: string[];
  occurrences: number;
  flow_id: string;
  template_id: string;
}

export interface LowStabilityStep {
  step_index: number;
  source_page: string;
  action_label: string;
  confidence_pct: number;
  confidence_reason: string;
  detail: string;
  flow_id: string;
  flow_name: string;
  flow_step: number;
  template_id: string;
  severity: string;
}

export interface QualityReport {
  locator_health_rows: LocatorHealthRow[];
  flaky_actions: FlakyAction[];
  low_stability_steps: LowStabilityStep[];
  recommendations: ReportIssue[];
  locator_issue_count: number;
  flaky_action_count: number;
  low_stability_count: number;
  locator_quality_rows: Record<string, unknown>[];
  locator_recommendations: string[];
}

export interface BlockedPage {
  state_id: string;
  state_short: string;
  title: string;
  url: string;
  reason: string;
  reason_label: string;
  detail: string;
  screenshot_link: string | null;
}

export interface PageObjectCard {
  page_type_id: string;
  anchor_id: string;
  name: string;
  class_name: string;
  archetype: string;
  url_pattern: string;
  instance_count: number;
  quality_score: number;
  quality_tone: string;
  is_changed: boolean;
  locator_rows: Record<string, unknown>[];
  recommendations: string[];
  code_preview: Record<string, string>;
}

export interface CrossRunComparison {
  has_previous_run: boolean;
  previous_run_id: string;
  previous_started_at: string;
  new_pages: number;
  disappeared_pages: number;
  changed_locators: number;
  new_page_examples: string[];
  disappeared_page_examples: string[];
  locator_changes: Record<string, unknown>[];
  changed_page_type_ids: string[];
}

export interface InputProvenance {
  profile: string;
  fill_actions: number;
  source_breakdown: Array<{ source: string; count: number }>;
  samples: Array<{ label: string; source: string }>;
}

export interface DiscoveryTimelineRow {
  order: number;
  state_id: string;
  state_short: string;
  title: string;
  url: string;
  depth: number;
  interactive: number;
  non_interactive: number;
  total: number;
  new_elements: number;
}

export interface UrlInventoryRow {
  title: string;
  url: string;
  interactive_elements: number;
  non_interactive_elements: number;
  total_elements: number;
  state_count: number;
  state_ids: string[];
  state_ids_short: string[];
}

/** Top-level report data contract. */
export interface ReportData {
  meta: ReportMeta;
  summary: CrawlSummary;
  pages: Record<string, PageReport>;
  flow_templates: FlowTemplateReport[];
  flow_instances: FlowInstanceCard[];
  graph: GraphData;
  coverage: CoverageReport;
  timeline: TimelineEntry[];
  quality: QualityReport;
  blocked_pages: BlockedPage[];
  page_objects: PageObjectCard[];
  cross_run: CrossRunComparison;
  input_provenance: InputProvenance;
  discovery_timeline: DiscoveryTimelineRow[];
  url_inventory: UrlInventoryRow[];
}

declare global {
  interface Window {
    __REPORT_DATA__: ReportData | string;
  }
}

/** Execution timeline with filters. */

import { createSignal, createMemo } from "solid-js";
import type { ReportData, TimelineEntry } from "../../types";
import { outcomeIcon, verdictColor } from "../../lib/format";
import DataTable from "../ui/DataTable";
import FilterBar from "../ui/FilterBar";
import Badge from "../ui/Badge";
import type { Column } from "../ui/DataTable";

interface Props {
  data: ReportData;
}

const OUTCOME_OPTIONS = [
  { value: "all", label: "all outcomes" },
  { value: "navigation", label: "navigation" },
  { value: "dom_change", label: "dom_change" },
  { value: "no_change", label: "no_change" },
  { value: "timeout", label: "timeout" },
  { value: "network_error", label: "network_error" },
  { value: "exception", label: "exception" },
];

const VERDICT_OPTIONS = [
  { value: "all", label: "all verdicts" },
  { value: "pass", label: "pass" },
  { value: "warn", label: "warn" },
];

type Row = TimelineEntry & Record<string, unknown>;

const COLUMNS: Column<Row>[] = [
  { key: "index", header: "#", align: "center" },
  {
    key: "source_page",
    header: "Source",
    render: (r) => (
      <span title={r.source_state_id}>{r.display?.source_page ?? r.source_page}</span>
    ),
  },
  {
    key: "action_label",
    header: "Action",
    render: (r) => (
      <span title={r.target_selector}>{r.display?.action ?? r.action_label}</span>
    ),
  },
  {
    key: "target_page",
    header: "Target",
    render: (r) => (
      <span title={r.target_state_id}>{r.display?.target_page ?? r.target_page}</span>
    ),
  },
  {
    key: "outcome",
    header: "Outcome",
    render: (r) => (
      <Badge tone={r.outcome === "navigation" || r.outcome === "dom_change" ? "pass" : r.outcome === "timeout" || r.outcome === "exception" ? "fail" : "neutral"}>
        {outcomeIcon(r.outcome)} {r.display?.outcome ?? r.outcome}
      </Badge>
    ),
  },
  {
    key: "confidence_pct",
    header: "Confidence",
    align: "right",
    render: (r) => (
      <span style={{ color: verdictColor(r.verdict) }}>{r.confidence_pct}%</span>
    ),
  },
];

export default function Timeline(props: Props) {
  const [outcomeFilter, setOutcomeFilter] = createSignal("all");
  const [verdictFilter, setVerdictFilter] = createSignal("all");

  const entries = createMemo(() => {
    let rows = props.data.timeline;
    if (outcomeFilter() !== "all") {
      rows = rows.filter((r) => r.outcome === outcomeFilter());
    }
    if (verdictFilter() !== "all") {
      rows = rows.filter((r) => r.verdict === verdictFilter());
    }
    return rows;
  });

  return (
    <div class="space-y-4">
      <header>
        <h2 class="text-lg font-semibold text-text-primary">Crawl Timeline</h2>
        <p class="text-sm text-text-secondary">{props.data.timeline.length} steps executed</p>
      </header>

      <FilterBar
        filters={[
          {
            name: "outcome",
            label: "Filter by outcome",
            options: OUTCOME_OPTIONS,
            value: outcomeFilter,
            onChange: setOutcomeFilter,
          },
          {
            name: "verdict",
            label: "Filter by verdict",
            options: VERDICT_OPTIONS,
            value: verdictFilter,
            onChange: setVerdictFilter,
          },
        ]}
      />

      <DataTable
        columns={COLUMNS}
        data={entries() as Row[]}
        emptyMessage="No matching timeline entries."
        caption="Crawl execution timeline"
      />
    </div>
  );
}

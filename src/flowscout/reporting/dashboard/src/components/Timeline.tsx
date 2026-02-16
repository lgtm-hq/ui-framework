/** Execution timeline with filters. */

import { createSignal, createMemo, For, Show } from "solid-js";
import type { ReportData, TimelineEntry } from "../types";
import { outcomeIcon, verdictColor } from "../lib/format";

interface Props {
  data: ReportData;
}

const OUTCOME_FILTERS = [
  "all",
  "navigation",
  "dom_change",
  "no_change",
  "timeout",
  "network_error",
  "exception",
] as const;

export default function Timeline(props: Props) {
  const [outcomeFilter, setOutcomeFilter] = createSignal<string>("all");
  const [verdictFilter, setVerdictFilter] = createSignal<string>("all");

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
    <div class="timeline">
      <header>
        <h2>Crawl Timeline</h2>
        <p>{props.data.timeline.length} steps executed</p>
      </header>

      <div class="timeline-filters">
        <select value={outcomeFilter()} onChange={(e) => setOutcomeFilter(e.currentTarget.value)}>
          <For each={OUTCOME_FILTERS}>{(o) => <option value={o}>{o}</option>}</For>
        </select>
        <select value={verdictFilter()} onChange={(e) => setVerdictFilter(e.currentTarget.value)}>
          <option value="all">all verdicts</option>
          <option value="pass">pass</option>
          <option value="warn">warn</option>
        </select>
      </div>

      <Show
        when={entries().length > 0}
        fallback={<p class="empty">No matching timeline entries.</p>}
      >
        <table class="timeline-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Source</th>
              <th>Action</th>
              <th>Target</th>
              <th>Outcome</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            <For each={entries()}>
              {(entry: TimelineEntry) => (
                <tr>
                  <td>{entry.index}</td>
                  <td title={entry.source_state_id}>
                    {entry.display?.source_page ?? entry.source_page}
                  </td>
                  <td title={entry.target_selector}>
                    {entry.display?.action ?? entry.action_label}
                  </td>
                  <td title={entry.target_state_id}>
                    {entry.display?.target_page ?? entry.target_page}
                  </td>
                  <td>
                    <span class={`outcome outcome-${entry.outcome}`}>
                      {outcomeIcon(entry.outcome)} {entry.display?.outcome ?? entry.outcome}
                    </span>
                  </td>
                  <td>
                    <span style={{ color: verdictColor(entry.verdict) }}>
                      {entry.confidence_pct}%
                    </span>
                  </td>
                </tr>
              )}
            </For>
          </tbody>
        </table>
      </Show>
    </div>
  );
}

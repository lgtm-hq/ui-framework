/** Dashboard overview — stats, pass rate, top issues. */

import { For, Show } from "solid-js";
import type { ReportData } from "../types";
import { formatDuration, formatPercent, pluralize, verdictColor } from "../lib/format";

interface Props {
  data: ReportData;
}

export default function Summary(props: Props) {
  const s = () => props.data.summary;
  const m = () => props.data.meta;
  const coverage = () => {
    const c = s().coverage as Record<string, Record<string, number>>;
    return {
      page: c?.page ?? { tested: 0, total: 0, pct: 0 },
      interaction: c?.interaction ?? { executed: 0, total: 0, pct: 0 },
      pass_rate: c?.pass_rate ?? { passed: 0, total: 0, pct: 0 },
    };
  };
  const structure = () => s().site_structure;

  return (
    <div class="summary">
      <header class="summary-header">
        <h2>Crawl Summary</h2>
        <p class="summary-url">{m().start_url}</p>
        <p class="summary-meta">
          {formatDuration(m().duration_seconds)} &middot; {m().strategy} strategy &middot;{" "}
          {m().environment} &middot; {m().input_profile} profile
        </p>
      </header>

      <div class="stat-grid">
        <StatCard label="States" value={s().total_states} />
        <StatCard label="Actions" value={s().total_actions} />
        <StatCard label="Flows" value={s().total_flows} />
        <StatCard label="Test Steps" value={s().total_test_steps} />
      </div>

      <div class="coverage-grid">
        <CoverageCard
          label="Page Coverage"
          pct={coverage().page.pct}
          detail={`${coverage().page.tested} / ${coverage().page.total} pages`}
        />
        <CoverageCard
          label="Interaction Coverage"
          pct={coverage().interaction.pct}
          detail={`${coverage().interaction.executed} / ${coverage().interaction.total} actions`}
        />
        <CoverageCard
          label="Pass Rate"
          pct={coverage().pass_rate.pct}
          detail={`${coverage().pass_rate.passed} / ${coverage().pass_rate.total} flows`}
        />
      </div>

      <div class="verdict-row">
        <For each={["pass", "fail", "warn"] as const}>
          {(v) => (
            <span class="verdict-badge" style={{ color: verdictColor(v) }}>
              {v}: {s().flow_counts[v] ?? 0}
            </span>
          )}
        </For>
      </div>

      <Show when={structure().page_type_count}>
        <div class="structure-summary">
          <h3>Site Structure</h3>
          <p>
            {pluralize(structure().page_type_count ?? 0, "page type")},{" "}
            {pluralize(structure().navigation_path_count ?? 0, "navigation path")},{" "}
            {pluralize(structure().flow_template_count ?? 0, "flow template")}
          </p>
          <Show when={(structure().blocked_page_count ?? 0) > 0}>
            <p class="blocked-note">
              {pluralize(structure().blocked_page_count ?? 0, "blocked page")}
            </p>
          </Show>
        </div>
      </Show>

      <Show when={s().top_issues.length > 0}>
        <div class="top-issues">
          <h3>Top Issues</h3>
          <ul>
            <For each={s().top_issues}>
              {(issue) => (
                <li class={`issue-${issue.priority}`}>
                  <strong>{issue.title}</strong>
                  <span>{issue.detail}</span>
                </li>
              )}
            </For>
          </ul>
        </div>
      </Show>
    </div>
  );
}

function StatCard(props: { label: string; value: number }) {
  return (
    <div class="stat-card">
      <div class="stat-value">{props.value}</div>
      <div class="stat-label">{props.label}</div>
    </div>
  );
}

function CoverageCard(props: { label: string; pct: number; detail: string }) {
  return (
    <div class="coverage-card">
      <div class="coverage-pct">{formatPercent(props.pct)}</div>
      <div class="coverage-label">{props.label}</div>
      <div class="coverage-detail">{props.detail}</div>
    </div>
  );
}

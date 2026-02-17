/** Dashboard overview — stats, pass rate, top issues. */

import { For, Show } from "solid-js";
import type { ReportData } from "../../types";
import { formatDuration, formatPercent, pluralize } from "../../lib/format";
import StatCard from "../ui/StatCard";
import Badge from "../ui/Badge";
import SectionCard from "../ui/SectionCard";

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
    <div class="space-y-6">
      <header>
        <h2 class="text-lg font-semibold text-text-primary">Crawl Summary</h2>
        <p class="mt-1 text-sm text-brand">{m().start_url}</p>
        <p class="mt-0.5 text-xs text-text-secondary">
          {formatDuration(m().duration_seconds)} &middot; {m().strategy} strategy &middot;{" "}
          {m().environment} &middot; {m().input_profile} profile
        </p>
      </header>

      <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <StatCard label="States" value={s().total_states} />
        <StatCard label="Actions" value={s().total_actions} />
        <StatCard label="Flows" value={s().total_flows} />
        <StatCard label="Test Steps" value={s().total_test_steps} />
      </div>

      <div class="grid grid-cols-3 gap-3">
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

      <div class="flex gap-3">
        <For each={["pass", "fail", "warn"] as const}>
          {(v) => (
            <Badge tone={v}>
              {v}: {s().flow_counts[v] ?? 0}
            </Badge>
          )}
        </For>
      </div>

      <Show when={structure().page_type_count}>
        <SectionCard title="Site Structure">
          <p class="text-sm text-text-secondary">
            {pluralize(structure().page_type_count ?? 0, "page type")},{" "}
            {pluralize(structure().navigation_path_count ?? 0, "navigation path")},{" "}
            {pluralize(structure().flow_template_count ?? 0, "flow template")}
          </p>
          <Show when={(structure().blocked_page_count ?? 0) > 0}>
            <p class="text-sm text-warning">
              {pluralize(structure().blocked_page_count ?? 0, "blocked page")}
            </p>
          </Show>
        </SectionCard>
      </Show>

      <Show when={s().top_issues.length > 0}>
        <SectionCard title="Top Issues">
          <ul class="space-y-2">
            <For each={s().top_issues}>
              {(issue) => (
                <li class="flex items-start gap-2 text-sm">
                  <Badge tone={issue.priority === "high" ? "danger" : issue.priority === "medium" ? "warn" : "info"}>
                    {issue.priority}
                  </Badge>
                  <div>
                    <strong class="text-text-primary">{issue.title}</strong>
                    <span class="ml-1 text-text-secondary">{issue.detail}</span>
                  </div>
                </li>
              )}
            </For>
          </ul>
        </SectionCard>
      </Show>
    </div>
  );
}

function CoverageCard(props: { label: string; pct: number; detail: string }) {
  return (
    <div class="rounded-lg border border-border bg-bg-surface p-4 text-center">
      <div class="text-2xl font-bold text-brand">{formatPercent(props.pct)}</div>
      <div class="mt-1 text-xs font-medium text-text-primary">{props.label}</div>
      <div class="mt-0.5 text-xs text-text-secondary">{props.detail}</div>
    </div>
  );
}

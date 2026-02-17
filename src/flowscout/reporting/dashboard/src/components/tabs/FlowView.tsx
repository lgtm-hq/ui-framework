/** Flow list with template drill-down. */

import { For, Show } from "solid-js";
import type { ReportData, FlowTemplateReport } from "../../types";
import Badge from "../ui/Badge";
import EmptyState from "../ui/EmptyState";

interface Props {
  data: ReportData;
}

export default function FlowView(props: Props) {
  return (
    <div class="space-y-4">
      <header>
        <h2 class="text-lg font-semibold text-text-primary">Test Flows</h2>
        <p class="text-sm text-text-secondary">
          {props.data.flow_templates.length} flow templates, {props.data.flow_instances.length}{" "}
          instances
        </p>
      </header>

      <Show
        when={props.data.flow_templates.length > 0}
        fallback={<EmptyState message="No flow templates discovered." />}
      >
        <div class="space-y-3">
          <For each={props.data.flow_templates}>
            {(template: FlowTemplateReport) => (
              <div
                class="rounded-lg border border-border bg-bg-surface p-4"
                id={template.anchor_id}
              >
                <div class="flex items-center justify-between">
                  <h3 class="text-sm font-semibold text-text-primary">{template.name}</h3>
                  <Badge tone={template.stability_bucket === "stable" ? "pass" : template.stability_bucket === "unstable" ? "fail" : "warn"}>
                    {template.stability_pct}%
                  </Badge>
                </div>
                <div class="mt-2 flex gap-3 text-xs text-text-secondary">
                  <span>{template.occurrence_count} instances</span>
                  <Badge tone="pass">{template.stable_count} pass</Badge>
                  <Badge tone="fail">{template.fail_count} fail</Badge>
                  <Badge tone="warn">{template.warn_count} warn</Badge>
                </div>
                <Show when={template.tags.length > 0}>
                  <div class="mt-2 flex flex-wrap gap-1">
                    <For each={template.tags}>
                      {(tag) => <Badge tone="info">{tag}</Badge>}
                    </For>
                  </div>
                </Show>
                <div class="mt-3 space-y-1">
                  <For each={template.instances}>
                    {(inst) => (
                      <div class="flex items-center justify-between rounded bg-bg-base px-3 py-1.5 text-sm">
                        <span class="text-text-primary">{inst.name}</span>
                        <Badge tone={inst.status === "pass" ? "pass" : inst.status === "fail" ? "fail" : "warn"}>
                          {inst.status}
                        </Badge>
                      </div>
                    )}
                  </For>
                </div>
              </div>
            )}
          </For>
        </div>
      </Show>
    </div>
  );
}

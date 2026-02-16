/** Flow list with template drill-down. */

import { For, Show } from "solid-js";
import type { ReportData, FlowTemplateReport } from "../types";
import { verdictColor } from "../lib/format";

interface Props {
  data: ReportData;
}

export default function FlowView(props: Props) {
  return (
    <div class="flow-view">
      <header>
        <h2>Test Flows</h2>
        <p>
          {props.data.flow_templates.length} flow templates, {props.data.flow_instances.length}{" "}
          instances
        </p>
      </header>

      <Show
        when={props.data.flow_templates.length > 0}
        fallback={<p class="empty">No flow templates discovered.</p>}
      >
        <div class="flow-template-list">
          <For each={props.data.flow_templates}>
            {(template: FlowTemplateReport) => (
              <div class="flow-template-card" id={template.anchor_id}>
                <div class="flow-template-header">
                  <h3>{template.name}</h3>
                  <span class={`stability-badge stability-${template.stability_bucket}`}>
                    {template.stability_pct}%
                  </span>
                </div>
                <div class="flow-template-meta">
                  <span>{template.occurrence_count} instances</span>
                  <span style={{ color: verdictColor("pass") }}>{template.stable_count} pass</span>
                  <span style={{ color: verdictColor("fail") }}>{template.fail_count} fail</span>
                  <span style={{ color: verdictColor("warn") }}>{template.warn_count} warn</span>
                </div>
                <Show when={template.tags.length > 0}>
                  <div class="flow-tags">
                    <For each={template.tags}>{(tag) => <span class="tag">{tag}</span>}</For>
                  </div>
                </Show>
                <div class="flow-instances">
                  <For each={template.instances}>
                    {(inst) => (
                      <div class={`flow-instance flow-${inst.status}`}>
                        <span class="flow-instance-name">{inst.name}</span>
                        <span
                          class="flow-instance-status"
                          style={{ color: verdictColor(inst.status) }}
                        >
                          {inst.status}
                        </span>
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

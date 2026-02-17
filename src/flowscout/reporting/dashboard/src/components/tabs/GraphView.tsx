/** Site-map graph visualization placeholder. */

import { For, Show } from "solid-js";
import type { ReportData } from "../../types";
import Badge from "../ui/Badge";
import SectionCard from "../ui/SectionCard";
import EmptyState from "../ui/EmptyState";

interface Props {
  data: ReportData;
}

export default function GraphView(props: Props) {
  const graph = () => props.data.graph;

  return (
    <div class="space-y-4">
      <header>
        <h2 class="text-lg font-semibold text-text-primary">Site Map</h2>
        <p class="text-sm text-text-secondary">
          {graph().nodes.length} page types, {graph().edges.length} transitions
        </p>
      </header>

      <Show
        when={graph().nodes.length > 0}
        fallback={<EmptyState message="No site structure data available." />}
      >
        <div id="graph-container" class="space-y-4">
          <SectionCard title="Page Types">
            <div class="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
              <For each={graph().nodes}>
                {(node) => (
                  <div class="rounded-md border border-border/50 bg-bg-base p-3">
                    <strong class="text-sm text-text-primary">{node.label}</strong>
                    <div class="mt-1 flex flex-wrap gap-1 text-xs">
                      <Badge tone="info">{node.archetype}</Badge>
                      <span class="text-text-secondary">{node.instance_count} instances</span>
                      <Show when={node.quality_score > 0}>
                        <span class="text-text-secondary">Quality: {node.quality_score}%</span>
                      </Show>
                    </div>
                  </div>
                )}
              </For>
            </div>
          </SectionCard>

          <SectionCard title="Transitions">
            <div class="space-y-1">
              <For each={graph().edges}>
                {(edge) => (
                  <div class="flex items-center justify-between rounded-md bg-bg-base px-3 py-2 text-sm">
                    <span class="text-text-primary">
                      {edge.source} &rarr; {edge.target}
                    </span>
                    <div class="flex items-center gap-2">
                      <span class="text-text-secondary">{edge.action_label}</span>
                      <Badge tone={edge.outcome === "navigation" ? "pass" : "neutral"}>
                        {edge.outcome}
                      </Badge>
                      <Show when={edge.uncovered}>
                        <Badge tone="danger">Uncovered</Badge>
                      </Show>
                    </div>
                  </div>
                )}
              </For>
            </div>
          </SectionCard>
        </div>
      </Show>
    </div>
  );
}

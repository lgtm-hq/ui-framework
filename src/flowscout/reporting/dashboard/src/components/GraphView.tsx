/** Site-map graph visualization placeholder.

vis-network will be added as a dependency in the build step.
For now this renders a structured node/edge list.
*/

import { For, Show } from "solid-js";
import type { ReportData } from "../types";

interface Props {
  data: ReportData;
}

export default function GraphView(props: Props) {
  const graph = () => props.data.graph;

  return (
    <div class="graph-view">
      <header>
        <h2>Site Map</h2>
        <p>
          {graph().nodes.length} page types, {graph().edges.length} transitions
        </p>
      </header>

      <Show
        when={graph().nodes.length > 0}
        fallback={<p class="empty">No site structure data available.</p>}
      >
        <div id="graph-container" class="graph-canvas">
          <div class="graph-fallback">
            <h3>Page Types</h3>
            <div class="graph-node-list">
              <For each={graph().nodes}>
                {(node) => (
                  <div class="graph-node-card">
                    <strong>{node.label}</strong>
                    <span class="archetype">{node.archetype}</span>
                    <span class="instances">{node.instance_count} instances</span>
                    <Show when={node.quality_score > 0}>
                      <span class="quality">Quality: {node.quality_score}%</span>
                    </Show>
                  </div>
                )}
              </For>
            </div>

            <h3>Transitions</h3>
            <div class="graph-edge-list">
              <For each={graph().edges}>
                {(edge) => (
                  <div class={`graph-edge-card ${edge.uncovered ? "uncovered" : ""}`}>
                    <span>
                      {edge.source} &rarr; {edge.target}
                    </span>
                    <span class="edge-action">{edge.action_label}</span>
                    <span class="edge-outcome">{edge.outcome}</span>
                    <Show when={edge.uncovered}>
                      <span class="uncovered-badge">Uncovered</span>
                    </Show>
                  </div>
                )}
              </For>
            </div>
          </div>
        </div>
      </Show>
    </div>
  );
}

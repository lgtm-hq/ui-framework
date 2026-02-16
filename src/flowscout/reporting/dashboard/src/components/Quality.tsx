/** Quality signals — locator health, flaky actions, recommendations. */

import { For, Show } from "solid-js";
import type { ReportData } from "../types";
import { verdictColor } from "../lib/format";

interface Props {
  data: ReportData;
}

export default function Quality(props: Props) {
  const q = () => props.data.quality;

  return (
    <div class="quality">
      <header>
        <h2>Quality Signals</h2>
      </header>

      <div class="quality-stats">
        <QualityStat
          label="Locator Issues"
          value={q().locator_issue_count}
          tone={q().locator_issue_count > 0 ? "warn" : "good"}
        />
        <QualityStat
          label="Flaky Actions"
          value={q().flaky_action_count}
          tone={q().flaky_action_count > 0 ? "warn" : "good"}
        />
        <QualityStat
          label="Low Stability"
          value={q().low_stability_count}
          tone={q().low_stability_count > 0 ? "warn" : "good"}
        />
      </div>

      <Show when={q().recommendations.length > 0}>
        <section class="quality-section">
          <h3>Recommendations</h3>
          <ul class="recommendations-list">
            <For each={q().recommendations}>
              {(rec) => (
                <li class={`recommendation priority-${rec.priority}`}>
                  <strong>{rec.title}</strong>
                  <span>{rec.detail}</span>
                </li>
              )}
            </For>
          </ul>
        </section>
      </Show>

      <Show when={q().locator_health_rows.length > 0}>
        <section class="quality-section">
          <h3>Locator Health</h3>
          <table class="quality-table">
            <thead>
              <tr>
                <th>Page Type</th>
                <th>Score</th>
                <th>Instances</th>
                <th>Fragile</th>
                <th>Recommendation</th>
              </tr>
            </thead>
            <tbody>
              <For each={q().locator_health_rows}>
                {(row) => (
                  <tr>
                    <td>{row.name}</td>
                    <td>{row.quality_score}%</td>
                    <td>{row.instance_count}</td>
                    <td>{row.fragile_count}</td>
                    <td>{row.recommendation}</td>
                  </tr>
                )}
              </For>
            </tbody>
          </table>
        </section>
      </Show>

      <Show when={q().flaky_actions.length > 0}>
        <section class="quality-section">
          <h3>Flaky Actions</h3>
          <table class="quality-table">
            <thead>
              <tr>
                <th>Page</th>
                <th>Action</th>
                <th>Outcomes</th>
                <th>Occurrences</th>
              </tr>
            </thead>
            <tbody>
              <For each={q().flaky_actions}>
                {(action) => (
                  <tr>
                    <td>{action.source_page}</td>
                    <td>{action.action_label}</td>
                    <td>{action.outcomes.join(", ")}</td>
                    <td>{action.occurrences}</td>
                  </tr>
                )}
              </For>
            </tbody>
          </table>
        </section>
      </Show>

      <Show when={q().low_stability_steps.length > 0}>
        <section class="quality-section">
          <h3>Low Stability Steps</h3>
          <table class="quality-table">
            <thead>
              <tr>
                <th>Step</th>
                <th>Page</th>
                <th>Action</th>
                <th>Confidence</th>
                <th>Severity</th>
              </tr>
            </thead>
            <tbody>
              <For each={q().low_stability_steps}>
                {(step) => (
                  <tr>
                    <td>{step.step_index}</td>
                    <td>{step.source_page}</td>
                    <td>{step.action_label}</td>
                    <td>
                      <span
                        style={{
                          color: verdictColor(step.confidence_pct >= 60 ? "warn" : "fail"),
                        }}
                      >
                        {step.confidence_pct}%
                      </span>
                    </td>
                    <td>{step.severity}</td>
                  </tr>
                )}
              </For>
            </tbody>
          </table>
        </section>
      </Show>

      <Show when={props.data.blocked_pages.length > 0}>
        <section class="quality-section" id="blocked-pages">
          <h3>Blocked Pages</h3>
          <table class="quality-table">
            <thead>
              <tr>
                <th>URL</th>
                <th>Reason</th>
                <th>Detail</th>
              </tr>
            </thead>
            <tbody>
              <For each={props.data.blocked_pages}>
                {(page) => (
                  <tr>
                    <td title={page.url}>{page.title}</td>
                    <td>{page.reason_label}</td>
                    <td>{page.detail}</td>
                  </tr>
                )}
              </For>
            </tbody>
          </table>
        </section>
      </Show>
    </div>
  );
}

function QualityStat(props: { label: string; value: number; tone: string }) {
  return (
    <div class={`quality-stat quality-${props.tone}`}>
      <div class="quality-stat-value">{props.value}</div>
      <div class="quality-stat-label">{props.label}</div>
    </div>
  );
}

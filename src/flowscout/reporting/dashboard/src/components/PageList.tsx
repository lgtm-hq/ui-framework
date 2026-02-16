/** Page objects — per-page-type inventory with locators and code preview. */

import { createSignal, For, Show } from "solid-js";
import type { ReportData, PageObjectCard } from "../types";

interface Props {
  data: ReportData;
}

export default function PageList(props: Props) {
  const [expanded, setExpanded] = createSignal<string | null>(null);

  const toggle = (id: string) => {
    setExpanded(expanded() === id ? null : id);
  };

  return (
    <div class="page-list">
      <header>
        <h2>Page Objects</h2>
        <p>{props.data.page_objects.length} page types</p>
      </header>

      <Show
        when={props.data.page_objects.length > 0}
        fallback={<p class="empty">No page objects available.</p>}
      >
        <div class="page-object-list">
          <For each={props.data.page_objects}>
            {(card: PageObjectCard) => (
              <div class="page-object-card" id={card.anchor_id}>
                <div class="page-object-header" onClick={() => toggle(card.page_type_id)}>
                  <div class="page-object-title">
                    <h3>
                      {card.name}
                      <Show when={card.is_changed}>
                        <span class="changed-badge">Changed</span>
                      </Show>
                    </h3>
                    <span class="archetype">{card.archetype}</span>
                  </div>
                  <div class="page-object-meta">
                    <span class={`quality-badge quality-${card.quality_tone}`}>
                      {card.quality_score}%
                    </span>
                    <span>{card.instance_count} instances</span>
                  </div>
                </div>

                <Show when={expanded() === card.page_type_id}>
                  <div class="page-object-detail">
                    <Show when={card.url_pattern}>
                      <p class="url-pattern">{card.url_pattern}</p>
                    </Show>

                    <Show when={card.recommendations.length > 0}>
                      <div class="recommendations">
                        <For each={card.recommendations}>
                          {(rec) => <p class="rec-item">{rec}</p>}
                        </For>
                      </div>
                    </Show>

                    <Show when={card.locator_rows.length > 0}>
                      <table class="locator-table">
                        <thead>
                          <tr>
                            <th>Selector</th>
                            <th>Stability</th>
                            <th>Zone</th>
                            <th>Exercised</th>
                          </tr>
                        </thead>
                        <tbody>
                          <For each={card.locator_rows}>
                            {(row) => (
                              <tr>
                                <td class="selector-cell">
                                  <code>{String(row.selector ?? "")}</code>
                                </td>
                                <td>{String(row.stability ?? "")}</td>
                                <td>{String(row.zone ?? "")}</td>
                                <td>{row.exercised ? "Yes" : "No"}</td>
                              </tr>
                            )}
                          </For>
                        </tbody>
                      </table>
                    </Show>

                    <Show when={card.code_preview?.python}>
                      <details class="code-preview">
                        <summary>Python Page Object</summary>
                        <pre>
                          <code>{card.code_preview.python}</code>
                        </pre>
                      </details>
                    </Show>

                    <Show when={card.code_preview?.typescript}>
                      <details class="code-preview">
                        <summary>TypeScript Page Object</summary>
                        <pre>
                          <code>{card.code_preview.typescript}</code>
                        </pre>
                      </details>
                    </Show>
                  </div>
                </Show>
              </div>
            )}
          </For>
        </div>
      </Show>
    </div>
  );
}

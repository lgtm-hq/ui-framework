/** Page objects — per-page-type inventory with locators and code preview. */

import { For, Show } from "solid-js";
import type { ReportData, PageObjectCard } from "../../types";
import Accordion from "../ui/Accordion";
import Badge from "../ui/Badge";
import CodeBlock from "../ui/CodeBlock";
import DataTable from "../ui/DataTable";
import EmptyState from "../ui/EmptyState";
import type { Column } from "../ui/DataTable";

interface Props {
  data: ReportData;
}

type LocatorRow = Record<string, unknown>;

const LOCATOR_COLUMNS: Column<LocatorRow>[] = [
  {
    key: "selector",
    header: "Selector",
    render: (r) => <code class="font-mono text-xs">{String(r.selector ?? "")}</code>,
  },
  { key: "stability", header: "Stability" },
  { key: "zone", header: "Zone" },
  {
    key: "exercised",
    header: "Exercised",
    render: (r) => (
      <Badge tone={r.exercised ? "pass" : "neutral"}>
        {r.exercised ? "Yes" : "No"}
      </Badge>
    ),
  },
];

export default function PageList(props: Props) {
  return (
    <div class="space-y-4">
      <header>
        <h2 class="text-lg font-semibold text-text-primary">Page Objects</h2>
        <p class="text-sm text-text-secondary">{props.data.page_objects.length} page types</p>
      </header>

      <Show
        when={props.data.page_objects.length > 0}
        fallback={<EmptyState message="No page objects available." />}
      >
        <div class="space-y-3">
          <For each={props.data.page_objects}>
            {(card: PageObjectCard) => (
              <Accordion
                id={card.anchor_id}
                header={
                  <div class="flex w-full items-center justify-between pr-2">
                    <div>
                      <span class="text-sm font-semibold text-text-primary">
                        {card.name}
                      </span>
                      <Show when={card.is_changed}>
                        <Badge tone="warn" class="ml-2">Changed</Badge>
                      </Show>
                      <span class="ml-2 text-xs text-text-secondary">{card.archetype}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <Badge tone={card.quality_tone === "good" ? "pass" : card.quality_tone === "poor" ? "fail" : "warn"}>
                        {card.quality_score}%
                      </Badge>
                      <span class="text-xs text-text-secondary">{card.instance_count} instances</span>
                    </div>
                  </div>
                }
              >
                <div class="space-y-3">
                  <Show when={card.url_pattern}>
                    <p class="text-xs text-text-secondary font-mono">{card.url_pattern}</p>
                  </Show>

                  <Show when={card.recommendations.length > 0}>
                    <div class="space-y-1">
                      <For each={card.recommendations}>
                        {(rec) => <p class="text-xs text-warning">{rec}</p>}
                      </For>
                    </div>
                  </Show>

                  <Show when={card.locator_rows.length > 0}>
                    <DataTable
                      columns={LOCATOR_COLUMNS}
                      data={card.locator_rows}
                      caption={`Locators for ${card.name}`}
                    />
                  </Show>

                  <Show when={card.code_preview?.python}>
                    <CodeBlock
                      code={card.code_preview.python}
                      label="Python Page Object"
                      collapsible
                    />
                  </Show>

                  <Show when={card.code_preview?.typescript}>
                    <CodeBlock
                      code={card.code_preview.typescript}
                      label="TypeScript Page Object"
                      collapsible
                    />
                  </Show>
                </div>
              </Accordion>
            )}
          </For>
        </div>
      </Show>
    </div>
  );
}

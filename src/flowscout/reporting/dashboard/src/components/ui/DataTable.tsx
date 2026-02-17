/** Generic table with typed columns, empty state, and consistent styling. */

import { For, Show } from "solid-js";
import type { JSX } from "solid-js";
import { cn } from "../../lib/cn";
import EmptyState from "./EmptyState";

interface Column<T> {
  key: string;
  header: string;
  render?: (row: T, index: number) => JSX.Element;
  align?: "left" | "center" | "right";
  class?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  emptyMessage?: string;
  class?: string;
  caption?: string;
  rowClass?: (row: T, index: number) => string;
}

const ALIGN_CLASS: Record<string, string> = {
  left: "text-left",
  center: "text-center",
  right: "text-right",
};

export type { Column, DataTableProps };

export default function DataTable<T extends Record<string, unknown>>(props: DataTableProps<T>) {
  return (
    <Show
      when={props.data.length > 0}
      fallback={<EmptyState message={props.emptyMessage ?? "No data available."} />}
    >
      <div class={cn("overflow-x-auto", props.class)}>
        <table class="w-full border-collapse">
          <Show when={props.caption}>
            <caption class="sr-only">{props.caption}</caption>
          </Show>
          <thead>
            <tr>
              <For each={props.columns}>
                {(col) => (
                  <th
                    class={cn(
                      "border-b border-border px-3 py-2 text-xs font-medium uppercase tracking-wider text-text-secondary",
                      ALIGN_CLASS[col.align ?? "left"],
                      col.class,
                    )}
                  >
                    {col.header}
                  </th>
                )}
              </For>
            </tr>
          </thead>
          <tbody>
            <For each={props.data}>
              {(row, i) => (
                <tr class={cn("border-b border-border/30", props.rowClass?.(row, i()))}>
                  <For each={props.columns}>
                    {(col) => (
                      <td
                        class={cn(
                          "px-3 py-2 text-sm text-text-primary",
                          ALIGN_CLASS[col.align ?? "left"],
                          col.class,
                        )}
                      >
                        {col.render
                          ? col.render(row, i())
                          : String(row[col.key] ?? "")}
                      </td>
                    )}
                  </For>
                </tr>
              )}
            </For>
          </tbody>
        </table>
      </div>
    </Show>
  );
}

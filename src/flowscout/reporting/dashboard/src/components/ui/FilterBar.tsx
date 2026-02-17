/** Generic filter row with select dropdowns. */

import { For } from "solid-js";
import { cn } from "../../lib/cn";

interface FilterOption {
  value: string;
  label: string;
}

interface FilterConfig {
  name: string;
  label: string;
  options: FilterOption[];
  value: () => string;
  onChange: (value: string) => void;
}

interface FilterBarProps {
  filters: FilterConfig[];
  class?: string;
}

export default function FilterBar(props: FilterBarProps) {
  return (
    <div class={cn("flex flex-wrap gap-2", props.class)}>
      <For each={props.filters}>
        {(filter) => (
          <select
            aria-label={filter.label}
            value={filter.value()}
            onChange={(e) => filter.onChange(e.currentTarget.value)}
            class="rounded-md border border-border bg-bg-base px-3 py-1.5 text-sm text-text-primary focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand/25"
          >
            <For each={filter.options}>
              {(opt) => <option value={opt.value}>{opt.label}</option>}
            </For>
          </select>
        )}
      </For>
    </div>
  );
}

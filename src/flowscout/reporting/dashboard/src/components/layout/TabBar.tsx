/** Tab navigation bar with accessible tab roles. */

import { For } from "solid-js";
import { cn } from "../../lib/cn";

interface Tab {
  id: string;
  label: string;
}

interface TabBarProps {
  tabs: Tab[];
  activeTab: () => string;
  onTabChange: (id: string) => void;
}

export default function TabBar(props: TabBarProps) {
  return (
    <div class="flex flex-wrap gap-1" role="tablist">
      <For each={props.tabs}>
        {(tab) => (
          <button
            role="tab"
            aria-selected={props.activeTab() === tab.id}
            class={cn(
              "rounded-md px-3 py-1.5 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/50",
              props.activeTab() === tab.id
                ? "bg-brand/15 text-brand"
                : "text-text-secondary hover:text-text-primary hover:bg-bg-overlay/50",
            )}
            onClick={() => props.onTabChange(tab.id)}
          >
            {tab.label}
          </button>
        )}
      </For>
    </div>
  );
}

/** Theme selector wired to turbo-themes data-theme attribute. */

import { For } from "solid-js";
import { cn } from "../../lib/cn";
import { AVAILABLE_THEMES, currentTheme, setTheme } from "../../lib/theme";

interface ThemeSwitcherProps {
  class?: string;
}

export default function ThemeSwitcher(props: ThemeSwitcherProps) {
  return (
    <select
      aria-label="Color theme"
      value={currentTheme()}
      onChange={(e) => setTheme(e.currentTarget.value)}
      class={cn(
        "rounded-md border border-border bg-bg-base px-2 py-1 text-xs text-text-secondary focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand/25",
        props.class,
      )}
    >
      <For each={[...AVAILABLE_THEMES]}>
        {(theme) => <option value={theme.id}>{theme.label}</option>}
      </For>
    </select>
  );
}

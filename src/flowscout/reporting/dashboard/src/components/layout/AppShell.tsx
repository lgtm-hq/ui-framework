/** App shell with brand header, theme switcher, and tab bar. */

import { Show } from "solid-js";
import type { JSX } from "solid-js";
import ThemeSwitcher from "../ui/ThemeSwitcher";

interface AppShellProps {
  version?: string;
  tabBar: JSX.Element;
  children: JSX.Element;
}

export default function AppShell(props: AppShellProps) {
  return (
    <div class="min-h-screen bg-bg-base text-text-primary">
      <nav class="sticky top-0 z-10 border-b border-border bg-bg-surface/95 backdrop-blur-sm">
        <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-2">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <strong class="text-sm font-bold text-text-primary">Flowscout</strong>
              <Show when={props.version}>
                <span class="rounded bg-bg-overlay px-1.5 py-0.5 text-xs text-text-secondary">
                  v{props.version}
                </span>
              </Show>
            </div>
            {props.tabBar}
          </div>
          <ThemeSwitcher />
        </div>
      </nav>
      <main class="mx-auto max-w-7xl px-4 py-6" role="tabpanel">
        {props.children}
      </main>
    </div>
  );
}

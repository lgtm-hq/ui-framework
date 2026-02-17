/** Expand/collapse panel with accessible header trigger. */

import { createSignal, Show } from "solid-js";
import type { JSX } from "solid-js";
import { cn } from "../../lib/cn";

interface AccordionProps {
  header: JSX.Element;
  children: JSX.Element;
  defaultOpen?: boolean;
  class?: string;
  id?: string;
}

export default function Accordion(props: AccordionProps) {
  const [open, setOpen] = createSignal(props.defaultOpen ?? false);
  const panelId = () => props.id ? `${props.id}-panel` : undefined;
  const triggerId = () => props.id ? `${props.id}-trigger` : undefined;

  const toggle = () => setOpen(!open());

  return (
    <div class={cn("rounded-lg border border-border overflow-hidden", props.class)}>
      <button
        id={triggerId()}
        type="button"
        class="flex w-full cursor-pointer items-center justify-between px-4 py-3 bg-bg-surface hover:bg-bg-overlay transition-colors text-left"
        aria-expanded={open()}
        aria-controls={panelId()}
        onClick={toggle}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            toggle();
          }
        }}
      >
        <div class="flex-1">{props.header}</div>
        <svg
          class={cn("h-4 w-4 text-text-secondary transition-transform", open() && "rotate-180")}
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
      <Show when={open()}>
        <div
          id={panelId()}
          role="region"
          aria-labelledby={triggerId()}
          class="border-t border-border/50 px-4 py-3"
        >
          {props.children}
        </div>
      </Show>
    </div>
  );
}

/** Titled section wrapper for grouping related content. */

import { cn } from "../../lib/cn";
import type { JSX } from "solid-js";

interface SectionCardProps {
  title: string;
  children: JSX.Element;
  id?: string;
  class?: string;
  headerRight?: JSX.Element;
}

export default function SectionCard(props: SectionCardProps) {
  return (
    <section
      id={props.id}
      class={cn("rounded-lg border border-border/50 bg-bg-surface/50 p-4 space-y-3", props.class)}
    >
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-semibold text-text-primary">{props.title}</h3>
        {props.headerRight}
      </div>
      {props.children}
    </section>
  );
}

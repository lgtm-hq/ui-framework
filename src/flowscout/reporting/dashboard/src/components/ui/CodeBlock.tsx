/** Formatted code display with optional collapsible wrapper. */

import { Show } from "solid-js";
import { cn } from "../../lib/cn";

interface CodeBlockProps {
  code: string;
  language?: string;
  label?: string;
  collapsible?: boolean;
  defaultOpen?: boolean;
  class?: string;
}

export default function CodeBlock(props: CodeBlockProps) {
  const codeContent = () => (
    <div
      class={cn(
        "rounded-lg bg-bg-base border border-border overflow-hidden",
        props.class,
      )}
    >
      <Show when={props.label && !props.collapsible}>
        <div class="border-b border-border/50 px-4 py-1.5 text-xs text-text-secondary">
          {props.label}
        </div>
      </Show>
      <pre class="overflow-x-auto p-4">
        <code class="font-mono text-sm text-text-primary">{props.code}</code>
      </pre>
    </div>
  );

  return (
    <Show when={props.collapsible} fallback={codeContent()}>
      <details open={props.defaultOpen} class="group">
        <summary class="cursor-pointer text-sm text-text-secondary hover:text-text-primary transition-colors">
          {props.label ?? props.language ?? "Code"}
        </summary>
        <div class="mt-2">{codeContent()}</div>
      </details>
    </Show>
  );
}

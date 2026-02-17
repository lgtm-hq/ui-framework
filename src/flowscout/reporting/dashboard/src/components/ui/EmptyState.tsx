/** Consistent "no data" placeholder. */

import { cn } from "../../lib/cn";

interface EmptyStateProps {
  message: string;
  icon?: string;
  class?: string;
}

export default function EmptyState(props: EmptyStateProps) {
  return (
    <div
      class={cn(
        "flex flex-col items-center justify-center gap-2 py-12 text-center text-text-secondary",
        props.class,
      )}
    >
      {props.icon && <span class="text-2xl">{props.icon}</span>}
      <p class="text-sm">{props.message}</p>
    </div>
  );
}

/** Numeric stat display card. */

import { cn } from "../../lib/cn";

type StatTone = "default" | "good" | "warn" | "danger";

interface StatCardProps {
  label: string;
  value: number | string;
  tone?: StatTone;
  class?: string;
}

const TONE_BORDER: Record<StatTone, string> = {
  default: "border-l-brand",
  good: "border-l-success",
  warn: "border-l-warning",
  danger: "border-l-danger",
};

export default function StatCard(props: StatCardProps) {
  const tone = () => props.tone ?? "default";

  return (
    <div
      class={cn(
        "rounded-lg border border-border bg-bg-surface p-4 text-center border-l-4",
        TONE_BORDER[tone()],
        props.class,
      )}
    >
      <div class="text-2xl font-bold text-text-primary">{props.value}</div>
      <div class="mt-1 text-xs text-text-secondary">{props.label}</div>
    </div>
  );
}

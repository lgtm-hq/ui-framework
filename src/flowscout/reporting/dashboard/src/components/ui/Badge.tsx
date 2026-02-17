/** Inline label for verdicts, statuses, outcomes, and tags. */

import { cn } from "../../lib/cn";
import type { JSX } from "solid-js";

type BadgeTone = "pass" | "fail" | "warn" | "info" | "neutral" | "danger";

interface BadgeProps {
  children: JSX.Element;
  tone?: BadgeTone;
  class?: string;
}

const TONE_CLASSES: Record<BadgeTone, string> = {
  pass: "bg-pass/15 text-pass",
  fail: "bg-fail/15 text-fail",
  warn: "bg-warn/15 text-warn",
  info: "bg-info/15 text-info",
  danger: "bg-danger/15 text-danger",
  neutral: "bg-muted/15 text-muted",
};

export default function Badge(props: BadgeProps) {
  return (
    <span
      class={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        TONE_CLASSES[props.tone ?? "neutral"],
        props.class,
      )}
    >
      {props.children}
    </span>
  );
}

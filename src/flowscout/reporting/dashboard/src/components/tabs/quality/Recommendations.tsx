/** Quality recommendations list. */

import { For, Show } from "solid-js";
import type { ReportIssue } from "../../../types";
import SectionCard from "../../ui/SectionCard";
import Badge from "../../ui/Badge";

interface Props {
  recommendations: ReportIssue[];
}

const PRIORITY_TONE = {
  high: "danger",
  medium: "warn",
  low: "info",
} as const;

export default function Recommendations(props: Props) {
  return (
    <Show when={props.recommendations.length > 0}>
      <SectionCard title="Recommendations">
        <ul class="space-y-2">
          <For each={props.recommendations}>
            {(rec) => (
              <li class="flex items-start gap-2 text-sm">
                <Badge tone={PRIORITY_TONE[rec.priority as keyof typeof PRIORITY_TONE] ?? "neutral"}>
                  {rec.priority}
                </Badge>
                <div>
                  <strong class="text-text-primary">{rec.title}</strong>
                  <span class="ml-1 text-text-secondary">{rec.detail}</span>
                </div>
              </li>
            )}
          </For>
        </ul>
      </SectionCard>
    </Show>
  );
}

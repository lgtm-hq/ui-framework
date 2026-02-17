/** Quality stat cards row. */

import type { QualityReport } from "../../../types";
import StatCard from "../../ui/StatCard";

interface Props {
  quality: QualityReport;
}

export default function QualityStats(props: Props) {
  const tone = (count: number) => (count > 0 ? "warn" as const : "good" as const);

  return (
    <div class="grid grid-cols-3 gap-3">
      <StatCard
        label="Locator Issues"
        value={props.quality.locator_issue_count}
        tone={tone(props.quality.locator_issue_count)}
      />
      <StatCard
        label="Flaky Actions"
        value={props.quality.flaky_action_count}
        tone={tone(props.quality.flaky_action_count)}
      />
      <StatCard
        label="Low Stability"
        value={props.quality.low_stability_count}
        tone={tone(props.quality.low_stability_count)}
      />
    </div>
  );
}

/** Quality signals tab — orchestrates quality sub-components. */

import type { ReportData } from "../../../types";
import QualityStats from "./QualityStats";
import Recommendations from "./Recommendations";
import LocatorHealth from "./LocatorHealth";
import FlakyActions from "./FlakyActions";
import LowStability from "./LowStability";
import BlockedPages from "./BlockedPages";

interface Props {
  data: ReportData;
}

export default function QualityTab(props: Props) {
  return (
    <div class="space-y-6">
      <header>
        <h2 class="text-lg font-semibold text-text-primary">Quality Signals</h2>
      </header>

      <QualityStats quality={props.data.quality} />
      <Recommendations recommendations={props.data.quality.recommendations} />
      <LocatorHealth rows={props.data.quality.locator_health_rows} />
      <FlakyActions actions={props.data.quality.flaky_actions} />
      <LowStability steps={props.data.quality.low_stability_steps} />
      <BlockedPages pages={props.data.blocked_pages} />
    </div>
  );
}

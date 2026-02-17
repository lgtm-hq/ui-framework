/** Low stability steps table. */

import { Show } from "solid-js";
import type { LowStabilityStep } from "../../../types";
import SectionCard from "../../ui/SectionCard";
import DataTable from "../../ui/DataTable";
import Badge from "../../ui/Badge";
import type { Column } from "../../ui/DataTable";

interface Props {
  steps: LowStabilityStep[];
}

type Row = LowStabilityStep & Record<string, unknown>;

const COLUMNS: Column<Row>[] = [
  { key: "step_index", header: "Step", align: "center" },
  { key: "source_page", header: "Page" },
  { key: "action_label", header: "Action" },
  {
    key: "confidence_pct",
    header: "Confidence",
    render: (r) => (
      <Badge tone={r.confidence_pct >= 60 ? "warn" : "fail"}>
        {r.confidence_pct}%
      </Badge>
    ),
  },
  { key: "severity", header: "Severity" },
];

export default function LowStability(props: Props) {
  return (
    <Show when={props.steps.length > 0}>
      <SectionCard title="Low Stability Steps">
        <DataTable
          columns={COLUMNS}
          data={props.steps as Row[]}
          caption="Steps with low confidence scores"
        />
      </SectionCard>
    </Show>
  );
}

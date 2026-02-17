/** Locator health table. */

import { Show } from "solid-js";
import type { LocatorHealthRow } from "../../../types";
import SectionCard from "../../ui/SectionCard";
import DataTable from "../../ui/DataTable";
import type { Column } from "../../ui/DataTable";

interface Props {
  rows: LocatorHealthRow[];
}

type Row = LocatorHealthRow & Record<string, unknown>;

const COLUMNS: Column<Row>[] = [
  { key: "name", header: "Page Type" },
  { key: "quality_score", header: "Score", render: (r) => <>{r.quality_score}%</> },
  { key: "instance_count", header: "Instances", align: "right" },
  { key: "fragile_count", header: "Fragile", align: "right" },
  { key: "recommendation", header: "Recommendation" },
];

export default function LocatorHealth(props: Props) {
  return (
    <Show when={props.rows.length > 0}>
      <SectionCard title="Locator Health">
        <DataTable
          columns={COLUMNS}
          data={props.rows as Row[]}
          caption="Locator health by page type"
        />
      </SectionCard>
    </Show>
  );
}

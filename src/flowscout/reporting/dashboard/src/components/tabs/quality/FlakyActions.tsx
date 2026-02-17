/** Flaky actions table. */

import { Show } from "solid-js";
import type { FlakyAction } from "../../../types";
import SectionCard from "../../ui/SectionCard";
import DataTable from "../../ui/DataTable";
import type { Column } from "../../ui/DataTable";

interface Props {
  actions: FlakyAction[];
}

type Row = FlakyAction & Record<string, unknown>;

const COLUMNS: Column<Row>[] = [
  { key: "source_page", header: "Page" },
  { key: "action_label", header: "Action" },
  { key: "outcomes", header: "Outcomes", render: (r) => <>{r.outcomes.join(", ")}</> },
  { key: "occurrences", header: "Occurrences", align: "right" },
];

export default function FlakyActions(props: Props) {
  return (
    <Show when={props.actions.length > 0}>
      <SectionCard title="Flaky Actions">
        <DataTable
          columns={COLUMNS}
          data={props.actions as Row[]}
          caption="Actions with inconsistent outcomes"
        />
      </SectionCard>
    </Show>
  );
}

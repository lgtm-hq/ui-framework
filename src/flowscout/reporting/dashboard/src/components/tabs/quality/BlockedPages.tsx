/** Blocked pages table. */

import { Show } from "solid-js";
import type { BlockedPage } from "../../../types";
import SectionCard from "../../ui/SectionCard";
import DataTable from "../../ui/DataTable";
import type { Column } from "../../ui/DataTable";

interface Props {
  pages: BlockedPage[];
}

type Row = BlockedPage & Record<string, unknown>;

const COLUMNS: Column<Row>[] = [
  { key: "title", header: "URL", render: (r) => <span title={r.url}>{r.title}</span> },
  { key: "reason_label", header: "Reason" },
  { key: "detail", header: "Detail" },
];

export default function BlockedPages(props: Props) {
  return (
    <Show when={props.pages.length > 0}>
      <SectionCard title="Blocked Pages" id="blocked-pages">
        <DataTable
          columns={COLUMNS}
          data={props.pages as Row[]}
          caption="Pages blocked by WAF, captcha, or auth"
        />
      </SectionCard>
    </Show>
  );
}

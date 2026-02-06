import { useState } from "react";

import type { EnrichedCase } from "../lib/flow-utils";
import { JourneyRow } from "./JourneyRow";

interface JourneyListProps {
  readonly cases: EnrichedCase[];
  readonly onSelectCase: (caseId: string) => void;
  readonly selectedCaseId: string | null;
}

const INITIAL_VISIBLE = 12;

export function JourneyList(props: JourneyListProps) {
  const [showAll, setShowAll] = useState(false);
  const visible = showAll ? props.cases : props.cases.slice(0, INITIAL_VISIBLE);
  const hasMore = props.cases.length > INITIAL_VISIBLE;

  return (
    <section className="overflow-hidden rounded-xl border border-brass/15 bg-surface">
      <div className="flex items-center justify-between border-b border-brass/10 px-4 py-2.5">
        <h3 className="font-sans text-[10px] font-semibold uppercase tracking-[0.2em] text-warm-gray/50">
          Journeys
        </h3>
        <span className="font-mono text-[10px] text-warm-gray/30">{props.cases.length}</span>
      </div>

      <div className="divide-y divide-brass/8">
        {visible.map((enriched) => (
          <JourneyRow
            key={enriched.testCase.case_id}
            testCase={enriched.testCase}
            segments={enriched.segments}
            isSelected={enriched.testCase.case_id === props.selectedCaseId}
            onSelect={() => {
              props.onSelectCase(enriched.testCase.case_id);
            }}
          />
        ))}
      </div>

      {props.cases.length === 0 ? (
        <p className="px-4 py-6 text-center text-xs text-warm-gray/40">
          No journeys found for current filters.
        </p>
      ) : null}

      {hasMore && !showAll ? (
        <div className="border-t border-brass/8 px-4 py-3 text-center">
          <button
            className="rounded-lg border border-brass/20 bg-surface-light px-3 py-1.5 font-mono text-[10px] font-medium text-warm-gray/60 transition hover:border-brass/40 hover:text-warm-gray"
            onClick={() => {
              setShowAll(true);
            }}
            type="button"
          >
            Show all {props.cases.length}
          </button>
        </div>
      ) : null}
    </section>
  );
}

import { useEffect } from "react";

import type { CaseFlowSegment } from "../lib/flow-utils";
import { describeState } from "../lib/flow-utils";
import type { FlowAction, FlowState, GeneratedTestCase } from "../types";
import { StepTimeline } from "./StepTimeline";

interface JourneyDetailPanelProps {
  readonly testCase: GeneratedTestCase | null;
  readonly caseFlowSegments: CaseFlowSegment[];
  readonly statesById: Record<string, FlowState>;
  readonly actionsById: Record<string, FlowAction>;
  readonly showTechnicalIds: boolean;
  readonly onClose: () => void;
}

export function JourneyDetailPanel(props: JourneyDetailPanelProps) {
  const { testCase, onClose } = props;

  useEffect(() => {
    if (!testCase) return;
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };
    document.addEventListener("keydown", handleKey);
    return () => {
      document.removeEventListener("keydown", handleKey);
    };
  }, [testCase, onClose]);

  if (!props.testCase) return null;

  const start = describeState({
    state: props.statesById[props.testCase.start_state_id],
    fallbackId: props.testCase.start_state_id,
  });
  const end = describeState({
    state: props.statesById[props.testCase.end_state_id],
    fallbackId: props.testCase.end_state_id,
  });
  const startLabel = props.testCase.start_state_label ?? `${start.title} (${start.path})`;
  const endLabel = props.testCase.end_state_label ?? `${end.title} (${end.path})`;
  const isPositive = props.testCase.case_type === "positive";

  return (
    <aside className="animate-slide-in-right flex w-[60%] shrink-0 flex-col overflow-hidden border-l border-brass/15 bg-surface">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 border-b border-brass/10 p-4">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span
              className={`rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${
                isPositive ? "bg-sage/15 text-sage" : "bg-brass/15 text-brass"
              }`}
            >
              {props.testCase.case_type}
            </span>
            {props.showTechnicalIds ? (
              <span className="font-mono text-[10px] text-warm-gray/30">
                {props.testCase.case_id}
              </span>
            ) : null}
          </div>
          <h3 className="mt-2 font-display text-lg font-bold text-brass">{props.testCase.title}</h3>
          <p className="mt-1 text-xs text-warm-gray/70">{props.testCase.expected_result}</p>
          <div className="mt-2 space-y-0.5 text-[11px] text-warm-gray/60">
            <p>
              <span className="font-medium text-warm-gray/80">Start:</span> {startLabel}
            </p>
            <p>
              <span className="font-medium text-warm-gray/80">End:</span> {endLabel}
            </p>
          </div>
        </div>
        <button
          className="shrink-0 rounded-lg border border-brass/20 bg-surface-light px-2.5 py-1.5 font-mono text-[10px] font-medium text-warm-gray/60 transition hover:border-brass/40 hover:text-warm-gray"
          onClick={props.onClose}
          type="button"
        >
          ×
        </button>
      </div>

      {/* Body — scrollable timeline */}
      <div className="flex-1 overflow-auto p-4">
        <h4 className="mb-4 font-sans text-[10px] font-semibold uppercase tracking-[0.2em] text-warm-gray/50">
          Journey Timeline
        </h4>
        <StepTimeline segments={props.caseFlowSegments} showTechnicalIds={props.showTechnicalIds} />
      </div>
    </aside>
  );
}

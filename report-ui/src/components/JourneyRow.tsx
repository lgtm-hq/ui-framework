import type { CaseFlowSegment } from "../lib/flow-utils";
import { outcomeDotColor, verdictColor, verdictLabel, worstOutcome } from "../lib/flow-utils";
import type { GeneratedTestCase } from "../types";

interface JourneyRowProps {
  readonly testCase: GeneratedTestCase;
  readonly segments: CaseFlowSegment[];
  readonly isSelected: boolean;
  readonly onSelect: () => void;
}

function OutcomeIcon(props: { readonly outcome: string }) {
  if (props.outcome === "execution_error" || props.outcome === "validation_error") {
    return (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="shrink-0">
        <circle
          cx="8"
          cy="8"
          r="7"
          stroke="currentColor"
          strokeWidth="1.5"
          className="text-sienna"
        />
        <line
          x1="8"
          y1="4.5"
          x2="8"
          y2="9"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          className="text-sienna"
        />
        <circle cx="8" cy="11.5" r="0.75" fill="currentColor" className="text-sienna" />
      </svg>
    );
  }
  if (props.outcome === "success") {
    return (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="shrink-0">
        <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" className="text-sage" />
        <polyline
          points="5,8.5 7,10.5 11,5.5"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="text-sage"
        />
      </svg>
    );
  }
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="shrink-0">
      <circle
        cx="8"
        cy="8"
        r="4"
        stroke="currentColor"
        strokeWidth="1.5"
        className="text-warm-gray/50"
      />
    </svg>
  );
}

export function JourneyRow(props: JourneyRowProps) {
  const worst = worstOutcome(props.segments);
  const dotClass = outcomeDotColor[worst] ?? "bg-warm-gray/40";

  return (
    <button
      className={`flex w-full items-center gap-3 px-3 py-3 text-left transition ${
        props.isSelected
          ? "border-l-2 border-brass bg-brass/10"
          : "border-l-2 border-transparent hover:bg-surface/40"
      }`}
      onClick={props.onSelect}
      type="button"
    >
      <OutcomeIcon outcome={worst} />

      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium text-warm-gray">{props.testCase.title}</p>
        <p className="mt-0.5 font-mono text-[10px] text-warm-gray/40">
          {props.segments.length} step{props.segments.length !== 1 ? "s" : ""}
        </p>
      </div>

      {props.segments.some((s) => s.verdictValue) ? (
        <span
          className={`shrink-0 rounded-full px-1.5 py-0.5 font-mono text-[8px] font-semibold uppercase text-white ${
            verdictColor[
              props.segments.some((s) => s.verdictValue === "fail")
                ? "fail"
                : props.segments.some((s) => s.verdictValue === "warn")
                  ? "warn"
                  : "pass"
            ] ?? "bg-warm-gray/30"
          }`}
        >
          {verdictLabel[
            props.segments.some((s) => s.verdictValue === "fail")
              ? "fail"
              : props.segments.some((s) => s.verdictValue === "warn")
                ? "warn"
                : "pass"
          ] ?? "?"}
        </span>
      ) : (
        <span className={`h-2 w-2 shrink-0 rounded-full ${dotClass}`} />
      )}
    </button>
  );
}

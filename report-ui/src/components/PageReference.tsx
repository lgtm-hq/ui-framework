import { compactPath } from "../lib/flow-utils";
import type { FlowState } from "../types";

interface PageReferenceProps {
  readonly states: FlowState[];
  readonly showTechnicalIds: boolean;
}

export function PageReference(props: PageReferenceProps) {
  if (props.states.length === 0) {
    return null;
  }

  return (
    <details className="group">
      <summary className="cursor-pointer font-sans text-[10px] font-semibold uppercase tracking-[0.2em] text-warm-gray/50 transition hover:text-brass/70">
        Pages ({props.states.length})
      </summary>
      <div className="mt-3 max-h-64 space-y-1.5 overflow-auto">
        {props.states.map((state) => (
          <div
            key={state.state_id}
            className="flex items-baseline gap-2 rounded-lg border border-brass/8 bg-surface px-3 py-2 text-xs"
          >
            <span className="shrink-0 rounded bg-brass/10 px-1.5 py-0.5 font-mono text-[9px] text-brass/60">
              d{state.depth}
            </span>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-medium text-warm-gray">{state.title || "(untitled)"}</p>
              <p className="mt-0.5 truncate font-mono text-[10px] text-warm-gray/40">
                {compactPath(state.url)}
              </p>
            </div>
            {props.showTechnicalIds ? (
              <span className="shrink-0 font-mono text-[9px] text-warm-gray/20">
                {state.state_id}
              </span>
            ) : null}
          </div>
        ))}
      </div>
    </details>
  );
}

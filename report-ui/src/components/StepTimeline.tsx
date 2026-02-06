import type { CaseFlowSegment } from "../lib/flow-utils";
import { StepTimelineNode } from "./StepTimelineNode";

interface StepTimelineProps {
  readonly segments: CaseFlowSegment[];
  readonly showTechnicalIds: boolean;
}

function MapPinIcon(props: { readonly className?: string }) {
  return (
    <svg width="12" height="14" viewBox="0 0 12 14" fill="none" className={props.className}>
      <path
        d="M6 0.5C3.24 0.5 1 2.74 1 5.5C1 9.25 6 13.5 6 13.5C6 13.5 11 9.25 11 5.5C11 2.74 8.76 0.5 6 0.5Z"
        fill="currentColor"
      />
      <circle cx="6" cy="5.5" r="2" fill="#0C0E14" />
    </svg>
  );
}

export function StepTimeline(props: StepTimelineProps) {
  if (props.segments.length === 0) {
    return (
      <p className="text-xs text-warm-gray/40">
        No structured flow map available for this journey.
      </p>
    );
  }

  const firstSegment = props.segments[0];

  return (
    <div className="grid gap-4">
      {/* Origin node */}
      <div className="relative pl-8">
        {props.segments.length > 0 ? (
          <div className="timeline-line absolute bottom-0 left-[11px] top-6 w-px border-l border-dashed border-brass/20" />
        ) : null}
        <div className="absolute left-[5px] top-1.5 text-brass">
          <MapPinIcon />
        </div>
        <div className="rounded-lg border border-brass/20 bg-brass/5 p-3">
          <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-brass/70">Origin</p>
          <p className="mt-1 text-sm font-medium text-warm-gray">{firstSegment.sourceTitle}</p>
          <p className="mt-0.5 font-mono text-[10px] text-warm-gray/40">
            {firstSegment.sourcePath}
          </p>
        </div>
      </div>

      {props.segments.map((segment, index) => (
        <StepTimelineNode
          key={`${segment.signature}-${index}`}
          segment={segment}
          stepIndex={index}
          isLast={index === props.segments.length - 1}
          showTechnicalIds={props.showTechnicalIds}
        />
      ))}
    </div>
  );
}

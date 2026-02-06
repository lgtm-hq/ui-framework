import type { CaseFlowSegment } from "../lib/flow-utils";
import { outcomeColor, verdictColor, verdictLabel } from "../lib/flow-utils";

interface StepTimelineNodeProps {
  readonly segment: CaseFlowSegment;
  readonly stepIndex: number;
  readonly isLast: boolean;
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

export function StepTimelineNode(props: StepTimelineNodeProps) {
  const pillClass = outcomeColor[props.segment.outcome] ?? "bg-warm-gray/30";
  const hasDetails =
    props.segment.details &&
    props.segment.details !== "No details available" &&
    props.segment.details.trim() !== "";
  const isError =
    props.segment.outcome === "execution_error" || props.segment.outcome === "validation_error";

  return (
    <div className="relative pl-8">
      {!props.isLast ? (
        <div className="timeline-line absolute bottom-0 left-[11px] top-8 w-px border-l border-dashed border-brass/20" />
      ) : null}

      <div className={`absolute left-[5px] top-2.5 ${isError ? "text-sienna" : "text-verdigris"}`}>
        <MapPinIcon />
      </div>

      <div className="rounded-lg border border-brass/10 bg-surface p-3.5">
        <div className="flex items-center gap-2">
          <span className="font-mono text-[10px] text-warm-gray/40">
            Step {props.stepIndex + 1}
          </span>
          <span
            className={`inline-flex rounded-full px-2 py-0.5 font-mono text-[9px] font-medium uppercase tracking-wide text-white ${pillClass}`}
          >
            {props.segment.outcome.replaceAll("_", " ")}
          </span>
        </div>

        <p className="mt-2 text-sm text-warm-gray">
          On <strong className="text-warm-gray">{props.segment.sourceTitle}</strong>,{" "}
          <span className="text-verdigris">{props.segment.actionPhrase}</span>
        </p>
        <p className="mt-1 text-sm text-warm-gray/70">
          Landed on <strong className="text-warm-gray/90">{props.segment.targetTitle}</strong>
        </p>

        <p className="mt-1.5 font-mono text-[10px] text-warm-gray/30">
          {props.segment.sourcePath} &rarr; {props.segment.targetPath}
        </p>

        {props.showTechnicalIds ? (
          <p className="mt-1 font-mono text-[10px] text-warm-gray/20">
            {props.segment.sourceId} &rarr; {props.segment.targetId}
          </p>
        ) : null}

        {props.segment.expected || props.segment.actual || props.segment.verdictValue ? (
          <div className="mt-2 space-y-1 text-[11px]">
            {props.segment.expected ? (
              <p className="text-warm-gray/50">
                <span className="font-medium text-warm-gray/70">Expected:</span>{" "}
                {props.segment.expected}
              </p>
            ) : null}
            {props.segment.actual ? (
              <p className="text-warm-gray/50">
                <span className="font-medium text-warm-gray/70">Actual:</span>{" "}
                {props.segment.actual}
              </p>
            ) : null}
            {props.segment.verdictValue ? (
              <span
                className={`inline-flex rounded-full px-2 py-0.5 font-mono text-[9px] font-medium uppercase tracking-wide text-white ${verdictColor[props.segment.verdictValue] ?? "bg-warm-gray/30"}`}
              >
                {verdictLabel[props.segment.verdictValue] ?? props.segment.verdictValue}
              </span>
            ) : null}
          </div>
        ) : null}

        {hasDetails ? (
          <div
            className={`mt-3 rounded-lg border px-3 py-2 text-xs ${
              isError
                ? "border-sienna/20 bg-sienna/5 text-sienna/80"
                : "border-brass/10 bg-surface-light text-warm-gray/60"
            }`}
          >
            {props.segment.details}
          </div>
        ) : null}

        {props.segment.screenshotPath ? (
          <div className="mt-3 overflow-hidden rounded-lg border border-brass/10">
            <img
              alt={`Screenshot after ${props.segment.actionPhrase}`}
              className="max-h-52 w-full object-cover"
              src={props.segment.screenshotPath}
            />
          </div>
        ) : null}
      </div>
    </div>
  );
}

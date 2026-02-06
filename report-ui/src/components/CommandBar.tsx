import type { ChangeEvent } from "react";

interface CommandBarProps {
  readonly sourceLabel: string;
  readonly onFileLoad: (event: ChangeEvent<HTMLInputElement>) => void;
  readonly error: string;
  readonly showTechnicalIds: boolean;
  readonly onToggleTechnicalIds: () => void;
  readonly timestamp?: string;
}

function CompassIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="14" cy="14" r="13" stroke="url(#compass-grad)" strokeWidth="1.5" />
      <circle cx="14" cy="14" r="10" stroke="url(#compass-grad)" strokeWidth="0.5" opacity="0.4" />
      <polygon points="14,4 15.5,12.5 14,11 12.5,12.5" fill="#C9A84C" opacity="0.9" />
      <polygon points="14,24 12.5,15.5 14,17 15.5,15.5" fill="#5EADA4" opacity="0.9" />
      <polygon points="4,14 12.5,12.5 11,14 12.5,15.5" fill="#5EADA4" opacity="0.6" />
      <polygon points="24,14 15.5,15.5 17,14 15.5,12.5" fill="#C9A84C" opacity="0.6" />
      <circle cx="14" cy="14" r="1.5" fill="#C9A84C" />
      <defs>
        <linearGradient id="compass-grad" x1="0" y1="0" x2="28" y2="28">
          <stop offset="0%" stopColor="#C9A84C" />
          <stop offset="100%" stopColor="#5EADA4" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export function CommandBar(props: CommandBarProps) {
  return (
    <header className="sticky top-0 z-40 flex h-12 items-center justify-between gap-4 border-b border-brass/15 bg-bg-deep/80 px-5 backdrop-blur-xl">
      <div className="flex items-center gap-3">
        <CompassIcon />
        <span className="font-display text-lg font-bold tracking-tight text-brass">flowscout</span>
      </div>

      <div className="flex items-center gap-3">
        <span className="hidden font-mono text-[11px] text-warm-gray/70 sm:inline">
          {props.sourceLabel}
        </span>

        {props.timestamp ? (
          <span className="hidden rounded-full border border-brass/20 bg-surface px-2.5 py-0.5 font-mono text-[10px] text-warm-gray/60 md:inline">
            {props.timestamp}
          </span>
        ) : null}

        <label className="inline-flex cursor-pointer items-center gap-1.5 rounded-lg border border-brass/20 bg-surface px-3 py-1.5 text-xs font-medium text-warm-gray transition hover:border-brass/40 hover:bg-surface-light">
          <span>Load JSON</span>
          <input
            className="hidden"
            type="file"
            accept=".json,application/json"
            onChange={props.onFileLoad}
          />
        </label>

        <button
          className={`rounded-lg border px-2.5 py-1.5 font-mono text-[10px] font-medium uppercase tracking-wider transition ${
            props.showTechnicalIds
              ? "border-brass bg-brass/15 text-brass"
              : "border-brass/20 bg-surface text-warm-gray/60 hover:border-brass/40"
          }`}
          onClick={props.onToggleTechnicalIds}
          type="button"
        >
          IDs
        </button>
      </div>

      {props.error ? (
        <div className="absolute left-0 top-12 w-full border-b border-sienna/30 bg-sienna/10 px-5 py-2">
          <p className="text-xs text-sienna">{props.error}</p>
        </div>
      ) : null}
    </header>
  );
}

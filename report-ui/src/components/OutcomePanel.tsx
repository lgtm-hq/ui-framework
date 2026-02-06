import { outcomeColor } from "../lib/flow-utils";

interface OutcomePanelProps {
  readonly outcomes: string[];
  readonly activeOutcome: string;
  readonly onOutcomeChange: (outcome: string) => void;
  readonly caseFilter: string;
  readonly onCaseFilterChange: (filter: string) => void;
  readonly searchText: string;
  readonly onSearchChange: (text: string) => void;
  readonly resultCount: number;
  readonly totalCount: number;
  readonly outcomeCounts: Record<string, number>;
  readonly totalEdges: number;
}

export function OutcomePanel(props: OutcomePanelProps) {
  return (
    <section className="space-y-5">
      <h3 className="font-sans text-[10px] font-semibold uppercase tracking-[0.2em] text-warm-gray/50">
        Outcomes
      </h3>

      {/* Distribution bars */}
      <div className="space-y-3">
        {Object.entries(props.outcomeCounts).map(([outcome, count]) => {
          const pct = props.totalEdges === 0 ? 0 : Math.round((count / props.totalEdges) * 100);
          return (
            <div key={outcome} className="space-y-1">
              <div className="flex items-baseline justify-between text-[11px]">
                <span className="font-mono uppercase text-warm-gray/70">
                  {outcome.replaceAll("_", " ")}
                </span>
                <span className="font-mono text-warm-gray/50">{count}</span>
              </div>
              <div className="h-1 overflow-hidden rounded-full bg-surface-light">
                <div
                  className={`h-1 rounded-full ${outcomeColor[outcome] ?? "bg-warm-gray/30"}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
        {Object.keys(props.outcomeCounts).length === 0 ? (
          <p className="text-xs text-warm-gray/40">No transitions loaded.</p>
        ) : null}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-1.5">
        {props.outcomes.map((entry) => (
          <button
            key={entry}
            className={`rounded-full border px-2.5 py-1 text-[10px] font-medium uppercase tracking-wide transition ${
              props.activeOutcome === entry
                ? "border-brass bg-brass/15 text-brass"
                : "border-brass/10 bg-surface text-warm-gray/60 hover:border-brass/30"
            }`}
            onClick={() => {
              props.onOutcomeChange(entry);
            }}
            type="button"
          >
            {entry === "all" ? "all" : entry.replaceAll("_", " ")}
          </button>
        ))}
      </div>

      {/* Case type pills */}
      <div className="flex gap-1.5">
        {["all", "positive", "negative"].map((entry) => (
          <button
            key={entry}
            className={`rounded-full border px-2.5 py-1 text-[10px] font-medium uppercase tracking-wide transition ${
              props.caseFilter === entry
                ? "border-brass bg-brass/15 text-brass"
                : "border-brass/10 bg-surface text-warm-gray/60 hover:border-brass/30"
            }`}
            onClick={() => {
              props.onCaseFilterChange(entry);
            }}
            type="button"
          >
            {entry}
          </button>
        ))}
      </div>

      {/* Search input */}
      <input
        className="w-full rounded-lg border border-brass/15 bg-surface px-3 py-2 font-mono text-xs text-warm-gray outline-none transition placeholder:text-warm-gray/30 focus:border-brass/40 focus:ring-1 focus:ring-brass/20"
        placeholder="Search journeys..."
        value={props.searchText}
        onChange={(event) => {
          props.onSearchChange(event.target.value);
        }}
      />

      <p className="font-mono text-[10px] text-warm-gray/40">
        {props.resultCount} of {props.totalCount} journeys
      </p>
    </section>
  );
}

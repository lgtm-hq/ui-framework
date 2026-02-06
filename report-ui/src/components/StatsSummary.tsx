interface StatsSummaryProps {
  readonly stateCount: number;
  readonly transitionCount: number;
  readonly journeyCount: number;
  readonly actionCount: number;
  readonly passCount?: number;
  readonly failCount?: number;
  readonly warnCount?: number;
}

function StatItem(props: { readonly label: string; readonly value: number; readonly max: number }) {
  const pct = props.max > 0 ? Math.min((props.value / props.max) * 100, 100) : 0;

  return (
    <div className="space-y-1.5">
      <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-warm-gray/60">
        {props.label}
      </p>
      <p className="font-display text-2xl font-bold text-brass">{props.value}</p>
      <div className="h-px overflow-hidden rounded-full bg-surface-light">
        <div
          className="h-px rounded-full bg-gradient-to-r from-brass to-verdigris"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export function StatsSummary(props: StatsSummaryProps) {
  const maxVal = Math.max(
    props.stateCount,
    props.transitionCount,
    props.journeyCount,
    props.actionCount,
    1,
  );

  return (
    <section className="space-y-5">
      <h3 className="font-sans text-[10px] font-semibold uppercase tracking-[0.2em] text-warm-gray/50">
        Telemetry
      </h3>
      <div className="space-y-4">
        <StatItem label="States" value={props.stateCount} max={maxVal} />
        <StatItem label="Transitions" value={props.transitionCount} max={maxVal} />
        <StatItem label="Journeys" value={props.journeyCount} max={maxVal} />
        <StatItem label="Actions" value={props.actionCount} max={maxVal} />
        {(props.passCount ?? 0) > 0 || (props.failCount ?? 0) > 0 ? (
          <>
            <div className="h-px bg-brass/10" />
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-sage" />
                <span className="font-mono text-[10px] text-warm-gray/60">
                  {props.passCount ?? 0} pass
                </span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-sienna" />
                <span className="font-mono text-[10px] text-warm-gray/60">
                  {props.failCount ?? 0} fail
                </span>
              </div>
              {(props.warnCount ?? 0) > 0 ? (
                <div className="flex items-center gap-1.5">
                  <span className="h-2 w-2 rounded-full bg-brass" />
                  <span className="font-mono text-[10px] text-warm-gray/60">
                    {props.warnCount ?? 0} warn
                  </span>
                </div>
              ) : null}
            </div>
          </>
        ) : null}
      </div>
    </section>
  );
}

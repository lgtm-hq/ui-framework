/** Display formatting helpers. */

export function formatDuration(seconds: number): string {
  if (seconds < 1) return `${Math.round(seconds * 1000)}ms`;
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  const mins = Math.floor(seconds / 60);
  const secs = Math.round(seconds % 60);
  return `${mins}m ${secs}s`;
}

export function formatPercent(value: number): string {
  return `${Math.round(value)}%`;
}

export function formatTimestamp(iso: string): string {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

export function pluralize(count: number, singular: string, plural?: string): string {
  return count === 1 ? `${count} ${singular}` : `${count} ${plural ?? singular + "s"}`;
}

export function outcomeIcon(outcome: string): string {
  const map: Record<string, string> = {
    navigation: "\u2192",
    dom_change: "\u0394",
    visual_change: "\u25cf",
    no_change: "\u2014",
    validation_error: "\u26a0",
    network_error: "\u2716",
    console_error: "\u26a0",
    timeout: "\u231b",
    exception: "\u2716",
  };
  return map[outcome] ?? "\u2022";
}

export function verdictColor(verdict: string): string {
  const map: Record<string, string> = {
    pass: "var(--color-pass)",
    fail: "var(--color-fail)",
    warn: "var(--color-warn)",
  };
  return map[verdict] ?? "var(--color-muted)";
}

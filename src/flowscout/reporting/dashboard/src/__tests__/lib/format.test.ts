import { describe, it, expect } from "vitest";
import {
  formatDuration,
  formatPercent,
  formatTimestamp,
  pluralize,
  outcomeIcon,
  verdictColor,
} from "../../lib/format";

describe("formatDuration", () => {
  it("formats sub-second as milliseconds", () => {
    expect(formatDuration(0.25)).toBe("250ms");
  });

  it("formats seconds with one decimal", () => {
    expect(formatDuration(5.123)).toBe("5.1s");
  });

  it("formats minutes and seconds", () => {
    expect(formatDuration(125)).toBe("2m 5s");
  });
});

describe("formatPercent", () => {
  it("rounds to integer percentage", () => {
    expect(formatPercent(85.7)).toBe("86%");
  });

  it("handles zero", () => {
    expect(formatPercent(0)).toBe("0%");
  });
});

describe("formatTimestamp", () => {
  it("returns empty string for empty input", () => {
    expect(formatTimestamp("")).toBe("");
  });

  it("formats valid ISO string", () => {
    const result = formatTimestamp("2026-01-15T10:30:00Z");
    expect(result).toBeTruthy();
    expect(result).not.toBe("2026-01-15T10:30:00Z");
  });
});

describe("pluralize", () => {
  it("uses singular for count of 1", () => {
    expect(pluralize(1, "page")).toBe("1 page");
  });

  it("adds s for plural by default", () => {
    expect(pluralize(5, "page")).toBe("5 pages");
  });

  it("uses custom plural", () => {
    expect(pluralize(0, "index", "indices")).toBe("0 indices");
  });
});

describe("outcomeIcon", () => {
  it("returns arrow for navigation", () => {
    expect(outcomeIcon("navigation")).toBe("\u2192");
  });

  it("returns hourglass for timeout", () => {
    expect(outcomeIcon("timeout")).toBe("\u231b");
  });

  it("returns bullet for unknown outcome", () => {
    expect(outcomeIcon("unknown")).toBe("\u2022");
  });
});

describe("verdictColor", () => {
  it("returns CSS var for pass", () => {
    expect(verdictColor("pass")).toBe("var(--color-pass)");
  });

  it("returns CSS var for fail", () => {
    expect(verdictColor("fail")).toBe("var(--color-fail)");
  });

  it("returns CSS var for warn", () => {
    expect(verdictColor("warn")).toBe("var(--color-warn)");
  });

  it("returns muted for unknown verdict", () => {
    expect(verdictColor("unknown")).toBe("var(--color-muted)");
  });
});

import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import QualityStats from "../../../components/tabs/quality/QualityStats";
import type { QualityReport } from "../../../types";

function makeQuality(overrides: Partial<QualityReport> = {}): QualityReport {
  return {
    locator_health_rows: [],
    flaky_actions: [],
    low_stability_steps: [],
    recommendations: [],
    locator_issue_count: 0,
    flaky_action_count: 0,
    low_stability_count: 0,
    locator_quality_rows: [],
    locator_recommendations: [],
    ...overrides,
  };
}

describe("QualityStats", () => {
  it("renders three stat cards", () => {
    render(() => <QualityStats quality={makeQuality()} />);
    expect(screen.getByText("Locator Issues")).toBeInTheDocument();
    expect(screen.getByText("Flaky Actions")).toBeInTheDocument();
    expect(screen.getByText("Low Stability")).toBeInTheDocument();
  });

  it("renders zero counts", () => {
    render(() => <QualityStats quality={makeQuality()} />);
    const zeros = screen.getAllByText("0");
    expect(zeros.length).toBe(3);
  });

  it("renders non-zero counts", () => {
    render(() => (
      <QualityStats
        quality={makeQuality({
          locator_issue_count: 4,
          flaky_action_count: 2,
          low_stability_count: 7,
        })}
      />
    ));
    expect(screen.getByText("4")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("7")).toBeInTheDocument();
  });
});

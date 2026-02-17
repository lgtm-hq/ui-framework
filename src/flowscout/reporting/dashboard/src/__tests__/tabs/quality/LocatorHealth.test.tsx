import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import LocatorHealth from "../../../components/tabs/quality/LocatorHealth";
import type { LocatorHealthRow } from "../../../types";

function makeRow(overrides: Partial<LocatorHealthRow> = {}): LocatorHealthRow {
  return {
    name: "Home Page",
    anchor_id: "home",
    quality_score: 92,
    instance_count: 5,
    fragile_count: 1,
    recommendation: "Add data-testid",
    ...overrides,
  };
}

describe("LocatorHealth", () => {
  it("renders nothing when rows are empty", () => {
    const { container } = render(() => <LocatorHealth rows={[]} />);
    expect(container.textContent).toBe("");
  });

  it("renders section title when rows exist", () => {
    render(() => <LocatorHealth rows={[makeRow()]} />);
    expect(screen.getByText("Locator Health")).toBeInTheDocument();
  });

  it("renders page name", () => {
    render(() => <LocatorHealth rows={[makeRow()]} />);
    expect(screen.getByText("Home Page")).toBeInTheDocument();
  });

  it("renders quality score as percentage", () => {
    render(() => <LocatorHealth rows={[makeRow()]} />);
    expect(screen.getByText("92%")).toBeInTheDocument();
  });

  it("renders recommendation text", () => {
    render(() => <LocatorHealth rows={[makeRow()]} />);
    expect(screen.getByText("Add data-testid")).toBeInTheDocument();
  });
});

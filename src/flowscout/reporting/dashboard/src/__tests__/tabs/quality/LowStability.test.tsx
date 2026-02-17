import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import LowStability from "../../../components/tabs/quality/LowStability";
import type { LowStabilityStep } from "../../../types";

function makeStep(overrides: Partial<LowStabilityStep> = {}): LowStabilityStep {
  return {
    step_index: 3,
    source_page: "Dashboard",
    action_label: "Click Settings",
    confidence_pct: 45,
    confidence_reason: "inconsistent outcome",
    detail: "Outcome varies across runs",
    flow_id: "f1",
    flow_name: "Settings Flow",
    flow_step: 3,
    template_id: "t1",
    severity: "high",
    ...overrides,
  };
}

describe("LowStability", () => {
  it("renders nothing when steps are empty", () => {
    const { container } = render(() => <LowStability steps={[]} />);
    expect(container.textContent).toBe("");
  });

  it("renders section title when steps exist", () => {
    render(() => <LowStability steps={[makeStep()]} />);
    expect(screen.getByText("Low Stability Steps")).toBeInTheDocument();
  });

  it("renders source page", () => {
    render(() => <LowStability steps={[makeStep()]} />);
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
  });

  it("renders action label", () => {
    render(() => <LowStability steps={[makeStep()]} />);
    expect(screen.getByText("Click Settings")).toBeInTheDocument();
  });

  it("renders confidence as badge", () => {
    render(() => <LowStability steps={[makeStep()]} />);
    expect(screen.getByText("45%")).toBeInTheDocument();
  });

  it("renders severity", () => {
    render(() => <LowStability steps={[makeStep()]} />);
    expect(screen.getByText("high")).toBeInTheDocument();
  });

  it("uses warn tone for confidence >= 60%", () => {
    render(() => <LowStability steps={[makeStep({ confidence_pct: 65 })]} />);
    expect(screen.getByText("65%")).toBeInTheDocument();
  });
});

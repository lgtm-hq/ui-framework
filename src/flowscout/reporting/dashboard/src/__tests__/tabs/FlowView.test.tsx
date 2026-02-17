import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import FlowView from "../../components/tabs/FlowView";
import { makeReportData } from "../fixtures";
import type { FlowTemplateReport } from "../../types";

function makeTemplate(overrides: Partial<FlowTemplateReport> = {}): FlowTemplateReport {
  return {
    template_id: "t1",
    anchor_id: "flow-t1",
    name: "Login Flow",
    occurrence_count: 3,
    stability_score: 0.85,
    stability_pct: 85,
    stability_bucket: "stable",
    template_type: "linear",
    tags: ["auth"],
    stable_count: 2,
    fail_count: 1,
    warn_count: 0,
    representative_rows: [],
    instances: [
      { flow_id: "f1", name: "Login #1", status: "pass", stability_score: 0.9, depth: 2, tags: [] },
      { flow_id: "f2", name: "Login #2", status: "fail", stability_score: 0.5, depth: 2, tags: [] },
    ],
    ...overrides,
  };
}

describe("FlowView", () => {
  it("renders the heading", () => {
    render(() => <FlowView data={makeReportData()} />);
    expect(screen.getByText("Test Flows")).toBeInTheDocument();
  });

  it("shows empty state when no templates", () => {
    render(() => <FlowView data={makeReportData()} />);
    expect(screen.getByText("No flow templates discovered.")).toBeInTheDocument();
  });

  it("renders template name", () => {
    const data = makeReportData({ flow_templates: [makeTemplate()] });
    render(() => <FlowView data={data} />);
    expect(screen.getByText("Login Flow")).toBeInTheDocument();
  });

  it("renders stability badge", () => {
    const data = makeReportData({ flow_templates: [makeTemplate()] });
    render(() => <FlowView data={data} />);
    expect(screen.getByText("85%")).toBeInTheDocument();
  });

  it("renders instance count", () => {
    const data = makeReportData({ flow_templates: [makeTemplate()] });
    render(() => <FlowView data={data} />);
    expect(screen.getByText("3 instances")).toBeInTheDocument();
  });

  it("renders flow instances", () => {
    const data = makeReportData({ flow_templates: [makeTemplate()] });
    render(() => <FlowView data={data} />);
    expect(screen.getByText("Login #1")).toBeInTheDocument();
    expect(screen.getByText("Login #2")).toBeInTheDocument();
  });

  it("renders tags", () => {
    const data = makeReportData({ flow_templates: [makeTemplate()] });
    render(() => <FlowView data={data} />);
    expect(screen.getByText("auth")).toBeInTheDocument();
  });

  it("renders pass/fail/warn counts", () => {
    const data = makeReportData({ flow_templates: [makeTemplate()] });
    render(() => <FlowView data={data} />);
    expect(screen.getByText("2 pass")).toBeInTheDocument();
    expect(screen.getByText("1 fail")).toBeInTheDocument();
    expect(screen.getByText("0 warn")).toBeInTheDocument();
  });
});

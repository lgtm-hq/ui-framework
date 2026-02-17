import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import GraphView from "../../components/tabs/GraphView";
import { makeReportData } from "../fixtures";
import type { GraphNode, GraphEdge } from "../../types";

function makeNode(overrides: Partial<GraphNode> = {}): GraphNode {
  return {
    id: "n1",
    label: "Home Page",
    archetype: "listing",
    instance_count: 3,
    url_pattern: "/",
    quality_score: 90,
    anchor_id: "page-n1",
    ...overrides,
  };
}

function makeEdge(overrides: Partial<GraphEdge> = {}): GraphEdge {
  return {
    source: "Home",
    target: "About",
    action_type: "click",
    action_label: "Click About",
    occurrence_count: 2,
    outcome: "navigation",
    uncovered: false,
    flow_id: "",
    template_id: "",
    ...overrides,
  };
}

describe("GraphView", () => {
  it("renders the heading", () => {
    render(() => <GraphView data={makeReportData()} />);
    expect(screen.getByText("Site Map")).toBeInTheDocument();
  });

  it("shows empty state when no nodes", () => {
    render(() => <GraphView data={makeReportData()} />);
    expect(screen.getByText("No site structure data available.")).toBeInTheDocument();
  });

  it("renders node label", () => {
    const data = makeReportData({ graph: { nodes: [makeNode()], edges: [] } });
    render(() => <GraphView data={data} />);
    expect(screen.getByText("Home Page")).toBeInTheDocument();
  });

  it("renders node archetype badge", () => {
    const data = makeReportData({ graph: { nodes: [makeNode()], edges: [] } });
    render(() => <GraphView data={data} />);
    expect(screen.getByText("listing")).toBeInTheDocument();
  });

  it("renders node instance count", () => {
    const data = makeReportData({ graph: { nodes: [makeNode()], edges: [] } });
    render(() => <GraphView data={data} />);
    expect(screen.getByText("3 instances")).toBeInTheDocument();
  });

  it("renders quality score when present", () => {
    const data = makeReportData({ graph: { nodes: [makeNode()], edges: [] } });
    render(() => <GraphView data={data} />);
    expect(screen.getByText("Quality: 90%")).toBeInTheDocument();
  });

  it("renders edge action label", () => {
    const data = makeReportData({ graph: { nodes: [makeNode()], edges: [makeEdge()] } });
    render(() => <GraphView data={data} />);
    expect(screen.getByText("Click About")).toBeInTheDocument();
  });

  it("renders uncovered badge for uncovered edges", () => {
    const data = makeReportData({
      graph: { nodes: [makeNode()], edges: [makeEdge({ uncovered: true })] },
    });
    render(() => <GraphView data={data} />);
    expect(screen.getByText("Uncovered")).toBeInTheDocument();
  });

  it("shows page type and transition counts", () => {
    const data = makeReportData({
      graph: { nodes: [makeNode()], edges: [makeEdge()] },
    });
    render(() => <GraphView data={data} />);
    expect(screen.getByText("1 page types, 1 transitions")).toBeInTheDocument();
  });
});

import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import QualityTab from "../../components/tabs/quality/QualityTab";
import { makeEmptyReportData } from "../fixtures";

describe("QualityTab", () => {
  it("renders the heading", () => {
    render(() => <QualityTab data={makeEmptyReportData()} />);
    expect(screen.getByText("Quality Signals")).toBeInTheDocument();
  });

  it("renders stat cards at zero with empty data", () => {
    render(() => <QualityTab data={makeEmptyReportData()} />);
    const zeros = screen.getAllByText("0");
    expect(zeros.length).toBeGreaterThanOrEqual(3);
  });

  it("renders stat cards with counts", () => {
    const data = makeEmptyReportData();
    data.quality.locator_issue_count = 2;
    data.quality.flaky_action_count = 1;
    data.quality.low_stability_count = 3;
    render(() => <QualityTab data={data} />);
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("1")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("shows recommendations when present", () => {
    const data = makeEmptyReportData();
    data.quality.recommendations = [
      { priority: "high", title: "Add data-testid", detail: "Fragile selectors detected", link_kind: "", link_value: "" },
    ];
    render(() => <QualityTab data={data} />);
    expect(screen.getByText("Recommendations")).toBeInTheDocument();
    expect(screen.getByText("Add data-testid")).toBeInTheDocument();
  });

  it("hides recommendation section when empty", () => {
    render(() => <QualityTab data={makeEmptyReportData()} />);
    expect(screen.queryByText("Recommendations")).not.toBeInTheDocument();
  });

  it("shows locator health table when rows exist", () => {
    const data = makeEmptyReportData();
    data.quality.locator_health_rows = [
      { name: "Home", anchor_id: "home", quality_score: 85, instance_count: 3, fragile_count: 1, recommendation: "Add IDs" },
    ];
    render(() => <QualityTab data={data} />);
    expect(screen.getByText("Locator Health")).toBeInTheDocument();
    expect(screen.getByText("Home")).toBeInTheDocument();
    expect(screen.getByText("85%")).toBeInTheDocument();
  });

  it("shows flaky actions when present", () => {
    const data = makeEmptyReportData();
    data.quality.flaky_actions = [
      { source_page: "Login", action_label: "Submit", outcomes: ["navigation", "timeout"], occurrences: 5, flow_id: "", template_id: "" },
    ];
    render(() => <QualityTab data={data} />);
    expect(screen.getByRole("heading", { name: "Flaky Actions" })).toBeInTheDocument();
    expect(screen.getByText("Login")).toBeInTheDocument();
  });

  it("shows blocked pages when present", () => {
    const data = makeEmptyReportData();
    data.blocked_pages = [
      { state_id: "s1", state_short: "s1", title: "Admin Panel", url: "/admin", reason: "403", reason_label: "Forbidden", detail: "Access denied", screenshot_link: null },
    ];
    render(() => <QualityTab data={data} />);
    expect(screen.getByText("Blocked Pages")).toBeInTheDocument();
    expect(screen.getByText("Admin Panel")).toBeInTheDocument();
  });

  it("hides all optional sections when data is empty", () => {
    render(() => <QualityTab data={makeEmptyReportData()} />);
    expect(screen.queryByText("Recommendations")).not.toBeInTheDocument();
    expect(screen.queryByText("Locator Health")).not.toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "Flaky Actions" })).not.toBeInTheDocument();
    expect(screen.queryByText("Low Stability Steps")).not.toBeInTheDocument();
    expect(screen.queryByText("Blocked Pages")).not.toBeInTheDocument();
  });
});

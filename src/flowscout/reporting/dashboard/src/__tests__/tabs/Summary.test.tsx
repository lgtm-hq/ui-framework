import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import Summary from "../../components/tabs/Summary";
import { makeReportData } from "../fixtures";

describe("Summary", () => {
  it("renders the start URL", () => {
    render(() => <Summary data={makeReportData()} />);
    expect(screen.getByText("https://example.com")).toBeInTheDocument();
  });

  it("renders stat cards with values", () => {
    render(() => <Summary data={makeReportData()} />);
    expect(screen.getByText("8")).toBeInTheDocument(); // States
    expect(screen.getByText("24")).toBeInTheDocument(); // Actions
    expect(screen.getByText("5")).toBeInTheDocument(); // Flows
    expect(screen.getByText("15")).toBeInTheDocument(); // Test Steps
  });

  it("renders coverage percentages", () => {
    render(() => <Summary data={makeReportData()} />);
    expect(screen.getByText("75%")).toBeInTheDocument();
    expect(screen.getByText("83%")).toBeInTheDocument();
    expect(screen.getByText("60%")).toBeInTheDocument();
  });

  it("renders verdict badges", () => {
    render(() => <Summary data={makeReportData()} />);
    expect(screen.getByText("pass: 3")).toBeInTheDocument();
    expect(screen.getByText("fail: 1")).toBeInTheDocument();
    expect(screen.getByText("warn: 1")).toBeInTheDocument();
  });

  it("renders site structure section", () => {
    render(() => <Summary data={makeReportData()} />);
    expect(screen.getByText("Site Structure")).toBeInTheDocument();
    expect(screen.getByText(/4 page types/)).toBeInTheDocument();
  });

  it("shows top issues when present", () => {
    const data = makeReportData();
    data.summary.top_issues = [
      { priority: "high", title: "Broken login", detail: "Form submit fails", link_kind: "", link_value: "" },
    ];
    render(() => <Summary data={data} />);
    expect(screen.getByText("Top Issues")).toBeInTheDocument();
    expect(screen.getByText("Broken login")).toBeInTheDocument();
  });

  it("hides top issues section when empty", () => {
    render(() => <Summary data={makeReportData()} />);
    expect(screen.queryByText("Top Issues")).not.toBeInTheDocument();
  });
});

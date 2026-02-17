import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import Timeline from "../../components/tabs/Timeline";
import { makeReportData } from "../fixtures";
import type { TimelineEntry } from "../../types";

function makeTimelineEntry(overrides: Partial<TimelineEntry> = {}): TimelineEntry {
  return {
    index: 1,
    source_state_id: "s0",
    target_state_id: "s1",
    source_state_short: "s0",
    target_state_short: "s1",
    source_page: "Home",
    target_page: "About",
    action_id: "a0",
    action_label: "Click About",
    action_type: "click",
    target_selector: "a[href='/about']",
    dom_id: "",
    outcome: "navigation",
    outcome_display: "navigation",
    verdict: "pass",
    confidence_pct: 95,
    duration_ms: 120,
    url_before: "https://example.com",
    url_after: "https://example.com/about",
    message: "",
    error_messages: [],
    console_errors: [],
    transition_kind: "url_change",
    transition_detail: "",
    navigation_status: 200,
    network_errors: [],
    redirect_chain: [],
    screenshot_link: null,
    input_source: "",
    input_profile: "",
    display: {},
    flow_context: {},
    ...overrides,
  };
}

describe("Timeline", () => {
  it("renders the heading", () => {
    render(() => <Timeline data={makeReportData()} />);
    expect(screen.getByText("Crawl Timeline")).toBeInTheDocument();
  });

  it("shows step count", () => {
    const data = makeReportData({ timeline: [makeTimelineEntry(), makeTimelineEntry({ index: 2 })] });
    render(() => <Timeline data={data} />);
    expect(screen.getByText("2 steps executed")).toBeInTheDocument();
  });

  it("renders timeline entries in the table", () => {
    const data = makeReportData({ timeline: [makeTimelineEntry()] });
    render(() => <Timeline data={data} />);
    expect(screen.getByText("Home")).toBeInTheDocument();
    expect(screen.getByText("Click About")).toBeInTheDocument();
    expect(screen.getByText("About")).toBeInTheDocument();
  });

  it("renders outcome badge", () => {
    const data = makeReportData({ timeline: [makeTimelineEntry()] });
    render(() => <Timeline data={data} />);
    expect(screen.getByText("95%")).toBeInTheDocument();
  });

  it("shows empty message when no entries", () => {
    render(() => <Timeline data={makeReportData()} />);
    expect(screen.getByText("No matching timeline entries.")).toBeInTheDocument();
  });

  it("renders filter bars", () => {
    render(() => <Timeline data={makeReportData()} />);
    expect(screen.getByLabelText("Filter by outcome")).toBeInTheDocument();
    expect(screen.getByLabelText("Filter by verdict")).toBeInTheDocument();
  });
});

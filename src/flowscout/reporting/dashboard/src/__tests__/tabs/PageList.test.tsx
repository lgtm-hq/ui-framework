import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import PageList from "../../components/tabs/PageList";
import { makeReportData } from "../fixtures";
import type { PageObjectCard } from "../../types";

function makePageCard(overrides: Partial<PageObjectCard> = {}): PageObjectCard {
  return {
    page_type_id: "pt1",
    anchor_id: "page-pt1",
    name: "Movies Listing",
    class_name: "MoviesListingPage",
    archetype: "listing",
    url_pattern: "/movies",
    instance_count: 5,
    quality_score: 88,
    quality_tone: "good",
    is_changed: false,
    locator_rows: [],
    recommendations: [],
    code_preview: {},
    ...overrides,
  };
}

describe("PageList", () => {
  it("renders the heading", () => {
    render(() => <PageList data={makeReportData()} />);
    expect(screen.getByText("Page Objects")).toBeInTheDocument();
  });

  it("shows empty state when no page objects", () => {
    render(() => <PageList data={makeReportData()} />);
    expect(screen.getByText("No page objects available.")).toBeInTheDocument();
  });

  it("shows page type count", () => {
    const data = makeReportData({ page_objects: [makePageCard()] });
    render(() => <PageList data={data} />);
    expect(screen.getByText("1 page types")).toBeInTheDocument();
  });

  it("renders page name in accordion header", () => {
    const data = makeReportData({ page_objects: [makePageCard()] });
    render(() => <PageList data={data} />);
    expect(screen.getByText("Movies Listing")).toBeInTheDocument();
  });

  it("renders archetype label", () => {
    const data = makeReportData({ page_objects: [makePageCard()] });
    render(() => <PageList data={data} />);
    expect(screen.getByText("listing")).toBeInTheDocument();
  });

  it("renders quality score badge", () => {
    const data = makeReportData({ page_objects: [makePageCard()] });
    render(() => <PageList data={data} />);
    expect(screen.getByText("88%")).toBeInTheDocument();
  });

  it("renders instance count", () => {
    const data = makeReportData({ page_objects: [makePageCard()] });
    render(() => <PageList data={data} />);
    expect(screen.getByText("5 instances")).toBeInTheDocument();
  });

  it("shows changed badge when page is changed", () => {
    const data = makeReportData({ page_objects: [makePageCard({ is_changed: true })] });
    render(() => <PageList data={data} />);
    expect(screen.getByText("Changed")).toBeInTheDocument();
  });

  it("hides changed badge when page is not changed", () => {
    const data = makeReportData({ page_objects: [makePageCard({ is_changed: false })] });
    render(() => <PageList data={data} />);
    expect(screen.queryByText("Changed")).not.toBeInTheDocument();
  });
});

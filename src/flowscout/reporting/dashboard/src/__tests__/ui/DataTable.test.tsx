import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import DataTable from "../../components/ui/DataTable";

interface TestRow {
  name: string;
  score: number;
  [key: string]: unknown;
}

const COLUMNS = [
  { key: "name", header: "Name" },
  { key: "score", header: "Score", align: "right" as const },
];

const SAMPLE_DATA: TestRow[] = [
  { name: "Home Page", score: 95 },
  { name: "Login Page", score: 42 },
];

describe("DataTable", () => {
  it("renders column headers", () => {
    render(() => <DataTable columns={COLUMNS} data={SAMPLE_DATA} />);
    expect(screen.getByText("Name")).toBeInTheDocument();
    expect(screen.getByText("Score")).toBeInTheDocument();
  });

  it("renders row data", () => {
    render(() => <DataTable columns={COLUMNS} data={SAMPLE_DATA} />);
    expect(screen.getByText("Home Page")).toBeInTheDocument();
    expect(screen.getByText("95")).toBeInTheDocument();
    expect(screen.getByText("Login Page")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
  });

  it("shows empty state when data is empty", () => {
    render(() => (
      <DataTable columns={COLUMNS} data={[]} emptyMessage="No pages found." />
    ));
    expect(screen.getByText("No pages found.")).toBeInTheDocument();
  });

  it("shows default empty message", () => {
    render(() => <DataTable columns={COLUMNS} data={[]} />);
    expect(screen.getByText("No data available.")).toBeInTheDocument();
  });

  it("uses custom render function", () => {
    const columns = [
      {
        key: "name",
        header: "Name",
        render: (row: TestRow) => <strong>{row.name}</strong>,
      },
    ];
    render(() => <DataTable columns={columns} data={SAMPLE_DATA} />);
    const strong = screen.getByText("Home Page");
    expect(strong.tagName).toBe("STRONG");
  });

  it("renders sr-only caption when provided", () => {
    const { container } = render(() => (
      <DataTable columns={COLUMNS} data={SAMPLE_DATA} caption="Test results" />
    ));
    const caption = container.querySelector("caption");
    expect(caption).toBeTruthy();
    expect(caption?.textContent).toBe("Test results");
  });
});

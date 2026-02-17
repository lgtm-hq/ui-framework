import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import StatCard from "../../components/ui/StatCard";

describe("StatCard", () => {
  it("renders label and numeric value", () => {
    render(() => <StatCard label="States" value={42} />);
    expect(screen.getByText("42")).toBeInTheDocument();
    expect(screen.getByText("States")).toBeInTheDocument();
  });

  it("renders string value", () => {
    render(() => <StatCard label="Status" value="OK" />);
    expect(screen.getByText("OK")).toBeInTheDocument();
  });

  it("applies default tone border", () => {
    const { container } = render(() => <StatCard label="Test" value={0} />);
    expect(container.firstChild).toHaveClass("border-l-brand");
  });

  it("applies good tone border", () => {
    const { container } = render(() => <StatCard label="Test" value={0} tone="good" />);
    expect(container.firstChild).toHaveClass("border-l-success");
  });

  it("applies warn tone border", () => {
    const { container } = render(() => <StatCard label="Test" value={5} tone="warn" />);
    expect(container.firstChild).toHaveClass("border-l-warning");
  });

  it("applies danger tone border", () => {
    const { container } = render(() => <StatCard label="Test" value={3} tone="danger" />);
    expect(container.firstChild).toHaveClass("border-l-danger");
  });
});

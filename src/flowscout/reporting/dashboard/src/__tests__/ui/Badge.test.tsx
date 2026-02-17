import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import Badge from "../../components/ui/Badge";

describe("Badge", () => {
  it("renders children text", () => {
    render(() => <Badge>pass</Badge>);
    expect(screen.getByText("pass")).toBeInTheDocument();
  });

  it("applies neutral tone by default", () => {
    const { container } = render(() => <Badge>test</Badge>);
    expect(container.firstChild).toHaveClass("text-muted");
  });

  it("applies pass tone classes", () => {
    const { container } = render(() => <Badge tone="pass">ok</Badge>);
    expect(container.firstChild).toHaveClass("text-pass");
  });

  it("applies fail tone classes", () => {
    const { container } = render(() => <Badge tone="fail">err</Badge>);
    expect(container.firstChild).toHaveClass("text-fail");
  });

  it("applies warn tone classes", () => {
    const { container } = render(() => <Badge tone="warn">caution</Badge>);
    expect(container.firstChild).toHaveClass("text-warn");
  });

  it("applies custom class", () => {
    const { container } = render(() => <Badge class="ml-2">tag</Badge>);
    expect(container.firstChild).toHaveClass("ml-2");
  });
});

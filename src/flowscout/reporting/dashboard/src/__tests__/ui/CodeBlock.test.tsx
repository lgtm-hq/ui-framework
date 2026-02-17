import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import CodeBlock from "../../components/ui/CodeBlock";

describe("CodeBlock", () => {
  it("renders code content", () => {
    render(() => <CodeBlock code="const x = 1;" />);
    expect(screen.getByText("const x = 1;")).toBeInTheDocument();
  });

  it("renders label when not collapsible", () => {
    render(() => <CodeBlock code="pass" label="Python" />);
    expect(screen.getByText("Python")).toBeInTheDocument();
  });

  it("renders collapsible with summary", () => {
    render(() => <CodeBlock code="pass" label="Python POM" collapsible />);
    expect(screen.getByText("Python POM")).toBeInTheDocument();
  });

  it("uses language as fallback summary in collapsible mode", () => {
    render(() => <CodeBlock code="pass" language="ts" collapsible />);
    expect(screen.getByText("ts")).toBeInTheDocument();
  });
});

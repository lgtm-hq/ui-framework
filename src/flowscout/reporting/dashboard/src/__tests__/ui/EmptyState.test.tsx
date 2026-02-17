import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import EmptyState from "../../components/ui/EmptyState";

describe("EmptyState", () => {
  it("renders the message", () => {
    render(() => <EmptyState message="No flows found." />);
    expect(screen.getByText("No flows found.")).toBeInTheDocument();
  });

  it("renders an icon when provided", () => {
    render(() => <EmptyState message="Empty" icon="🔍" />);
    expect(screen.getByText("🔍")).toBeInTheDocument();
  });

  it("applies custom class", () => {
    const { container } = render(() => <EmptyState message="Empty" class="mt-8" />);
    expect(container.firstChild).toHaveClass("mt-8");
  });
});

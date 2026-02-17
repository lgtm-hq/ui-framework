import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import Recommendations from "../../../components/tabs/quality/Recommendations";

describe("Recommendations", () => {
  it("renders nothing when empty", () => {
    const { container } = render(() => <Recommendations recommendations={[]} />);
    expect(container.textContent).toBe("");
  });

  it("renders section title when recommendations exist", () => {
    render(() => (
      <Recommendations
        recommendations={[
          { priority: "high", title: "Add data-testid", detail: "Fragile selectors", link_kind: "", link_value: "" },
        ]}
      />
    ));
    expect(screen.getByText("Recommendations")).toBeInTheDocument();
  });

  it("renders recommendation title and detail", () => {
    render(() => (
      <Recommendations
        recommendations={[
          { priority: "medium", title: "Use stable selectors", detail: "Avoid nth-of-type", link_kind: "", link_value: "" },
        ]}
      />
    ));
    expect(screen.getByText("Use stable selectors")).toBeInTheDocument();
    expect(screen.getByText("Avoid nth-of-type")).toBeInTheDocument();
  });

  it("renders priority badge", () => {
    render(() => (
      <Recommendations
        recommendations={[
          { priority: "low", title: "Minor issue", detail: "", link_kind: "", link_value: "" },
        ]}
      />
    ));
    expect(screen.getByText("low")).toBeInTheDocument();
  });

  it("renders multiple recommendations", () => {
    render(() => (
      <Recommendations
        recommendations={[
          { priority: "high", title: "First", detail: "", link_kind: "", link_value: "" },
          { priority: "medium", title: "Second", detail: "", link_kind: "", link_value: "" },
        ]}
      />
    ));
    expect(screen.getByText("First")).toBeInTheDocument();
    expect(screen.getByText("Second")).toBeInTheDocument();
  });
});

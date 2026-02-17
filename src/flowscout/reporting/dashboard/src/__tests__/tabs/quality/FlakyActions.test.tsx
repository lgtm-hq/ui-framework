import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import FlakyActions from "../../../components/tabs/quality/FlakyActions";
import type { FlakyAction } from "../../../types";

function makeAction(overrides: Partial<FlakyAction> = {}): FlakyAction {
  return {
    source_page: "Login",
    action_label: "Submit",
    outcomes: ["navigation", "timeout"],
    occurrences: 5,
    flow_id: "",
    template_id: "",
    ...overrides,
  };
}

describe("FlakyActions", () => {
  it("renders nothing when actions are empty", () => {
    const { container } = render(() => <FlakyActions actions={[]} />);
    expect(container.textContent).toBe("");
  });

  it("renders section title when actions exist", () => {
    render(() => <FlakyActions actions={[makeAction()]} />);
    expect(screen.getByRole("heading", { name: "Flaky Actions" })).toBeInTheDocument();
  });

  it("renders source page", () => {
    render(() => <FlakyActions actions={[makeAction()]} />);
    expect(screen.getByText("Login")).toBeInTheDocument();
  });

  it("renders action label", () => {
    render(() => <FlakyActions actions={[makeAction()]} />);
    expect(screen.getByText("Submit")).toBeInTheDocument();
  });

  it("renders outcomes as comma-separated list", () => {
    render(() => <FlakyActions actions={[makeAction()]} />);
    expect(screen.getByText("navigation, timeout")).toBeInTheDocument();
  });

  it("renders occurrence count", () => {
    render(() => <FlakyActions actions={[makeAction()]} />);
    expect(screen.getByText("5")).toBeInTheDocument();
  });
});

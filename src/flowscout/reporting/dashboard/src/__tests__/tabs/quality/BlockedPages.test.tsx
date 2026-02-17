import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import BlockedPages from "../../../components/tabs/quality/BlockedPages";
import type { BlockedPage } from "../../../types";

function makePage(overrides: Partial<BlockedPage> = {}): BlockedPage {
  return {
    state_id: "s1",
    state_short: "s1",
    title: "Admin Panel",
    url: "/admin",
    reason: "403",
    reason_label: "Forbidden",
    detail: "Access denied",
    screenshot_link: null,
    ...overrides,
  };
}

describe("BlockedPages", () => {
  it("renders nothing when pages are empty", () => {
    const { container } = render(() => <BlockedPages pages={[]} />);
    expect(container.textContent).toBe("");
  });

  it("renders section title when pages exist", () => {
    render(() => <BlockedPages pages={[makePage()]} />);
    expect(screen.getByText("Blocked Pages")).toBeInTheDocument();
  });

  it("renders page title", () => {
    render(() => <BlockedPages pages={[makePage()]} />);
    expect(screen.getByText("Admin Panel")).toBeInTheDocument();
  });

  it("renders reason label", () => {
    render(() => <BlockedPages pages={[makePage()]} />);
    expect(screen.getByText("Forbidden")).toBeInTheDocument();
  });

  it("renders detail text", () => {
    render(() => <BlockedPages pages={[makePage()]} />);
    expect(screen.getByText("Access denied")).toBeInTheDocument();
  });

  it("renders multiple blocked pages", () => {
    render(() => (
      <BlockedPages
        pages={[
          makePage({ title: "Admin Panel" }),
          makePage({ state_id: "s2", title: "Settings", url: "/settings", reason_label: "Auth Required" }),
        ]}
      />
    ));
    expect(screen.getByText("Admin Panel")).toBeInTheDocument();
    expect(screen.getByText("Settings")).toBeInTheDocument();
  });
});

import { render, screen, fireEvent } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import Accordion from "../../components/ui/Accordion";

describe("Accordion", () => {
  it("is collapsed by default", () => {
    render(() => <Accordion header="Header">Hidden content</Accordion>);
    expect(screen.queryByText("Hidden content")).not.toBeInTheDocument();
  });

  it("expands on click", async () => {
    render(() => <Accordion header="Click me">Revealed</Accordion>);
    await fireEvent.click(screen.getByRole("button"));
    expect(screen.getByText("Revealed")).toBeInTheDocument();
  });

  it("collapses on second click", async () => {
    render(() => <Accordion header="Toggle">Content</Accordion>);
    const btn = screen.getByRole("button");
    await fireEvent.click(btn);
    expect(screen.getByText("Content")).toBeInTheDocument();
    await fireEvent.click(btn);
    expect(screen.queryByText("Content")).not.toBeInTheDocument();
  });

  it("starts open with defaultOpen", () => {
    render(() => <Accordion header="Open" defaultOpen>Visible</Accordion>);
    expect(screen.getByText("Visible")).toBeInTheDocument();
  });

  it("sets aria-expanded correctly", async () => {
    render(() => <Accordion header="A11y">Body</Accordion>);
    const btn = screen.getByRole("button");
    expect(btn).toHaveAttribute("aria-expanded", "false");
    await fireEvent.click(btn);
    expect(btn).toHaveAttribute("aria-expanded", "true");
  });

  it("expands on Enter key", async () => {
    render(() => <Accordion header="Key">Keyboard content</Accordion>);
    const btn = screen.getByRole("button");
    await fireEvent.keyDown(btn, { key: "Enter" });
    expect(screen.getByText("Keyboard content")).toBeInTheDocument();
  });

  it("expands on Space key", async () => {
    render(() => <Accordion header="Key">Space content</Accordion>);
    const btn = screen.getByRole("button");
    await fireEvent.keyDown(btn, { key: " " });
    expect(screen.getByText("Space content")).toBeInTheDocument();
  });
});

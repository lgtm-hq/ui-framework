import { render, screen } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import SectionCard from "../../components/ui/SectionCard";

describe("SectionCard", () => {
  it("renders title", () => {
    render(() => <SectionCard title="Locator Health">content</SectionCard>);
    expect(screen.getByText("Locator Health")).toBeInTheDocument();
  });

  it("renders children", () => {
    render(() => <SectionCard title="Test">child content</SectionCard>);
    expect(screen.getByText("child content")).toBeInTheDocument();
  });

  it("renders headerRight element", () => {
    render(() => (
      <SectionCard title="Test" headerRight={<span>3 items</span>}>
        body
      </SectionCard>
    ));
    expect(screen.getByText("3 items")).toBeInTheDocument();
  });

  it("sets id attribute", () => {
    const { container } = render(() => (
      <SectionCard title="Test" id="blocked-pages">
        body
      </SectionCard>
    ));
    expect(container.querySelector("#blocked-pages")).toBeTruthy();
  });
});

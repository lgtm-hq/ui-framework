import { render, screen, fireEvent } from "@solidjs/testing-library";
import { describe, it, expect, vi } from "vitest";
import { createSignal } from "solid-js";
import FilterBar from "../../components/ui/FilterBar";

describe("FilterBar", () => {
  it("renders filter selects", () => {
    const [val, setVal] = createSignal("all");
    render(() => (
      <FilterBar
        filters={[
          {
            name: "outcome",
            label: "Filter by outcome",
            options: [
              { value: "all", label: "All" },
              { value: "pass", label: "Pass" },
            ],
            value: val,
            onChange: setVal,
          },
        ]}
      />
    ));
    expect(screen.getByLabelText("Filter by outcome")).toBeInTheDocument();
  });

  it("renders all options", () => {
    const [val, setVal] = createSignal("all");
    render(() => (
      <FilterBar
        filters={[
          {
            name: "test",
            label: "Test filter",
            options: [
              { value: "a", label: "Alpha" },
              { value: "b", label: "Beta" },
              { value: "c", label: "Gamma" },
            ],
            value: val,
            onChange: setVal,
          },
        ]}
      />
    ));
    expect(screen.getByText("Alpha")).toBeInTheDocument();
    expect(screen.getByText("Beta")).toBeInTheDocument();
    expect(screen.getByText("Gamma")).toBeInTheDocument();
  });

  it("calls onChange on selection", async () => {
    const onChange = vi.fn();
    const [val] = createSignal("all");
    render(() => (
      <FilterBar
        filters={[
          {
            name: "test",
            label: "Test",
            options: [
              { value: "all", label: "All" },
              { value: "pass", label: "Pass" },
            ],
            value: val,
            onChange,
          },
        ]}
      />
    ));
    await fireEvent.change(screen.getByLabelText("Test"), { target: { value: "pass" } });
    expect(onChange).toHaveBeenCalledWith("pass");
  });
});

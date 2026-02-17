import { render, screen, fireEvent } from "@solidjs/testing-library";
import { describe, it, expect } from "vitest";
import ThemeSwitcher from "../../components/ui/ThemeSwitcher";

describe("ThemeSwitcher", () => {
  it("renders theme options", () => {
    render(() => <ThemeSwitcher />);
    expect(screen.getByText("Catppuccin Mocha")).toBeInTheDocument();
    expect(screen.getByText("Tokyo Night Storm")).toBeInTheDocument();
  });

  it("has accessible label", () => {
    render(() => <ThemeSwitcher />);
    expect(screen.getByLabelText("Color theme")).toBeInTheDocument();
  });

  it("sets data-theme on change", async () => {
    render(() => <ThemeSwitcher />);
    const select = screen.getByLabelText("Color theme");
    await fireEvent.change(select, { target: { value: "tokyo-night-storm" } });
    expect(document.documentElement.dataset.theme).toBe("tokyo-night-storm");
  });
});

/** Theme switching via data-theme attribute on <html>. */

import { createSignal } from "solid-js";

const STORAGE_KEY = "flowscout-report-theme";
const DEFAULT_THEME = "catppuccin-mocha";

export const AVAILABLE_THEMES = [
  { id: "catppuccin-mocha", label: "Catppuccin Mocha" },
  { id: "tokyo-night-storm", label: "Tokyo Night Storm" },
] as const;

export function getCurrentTheme(): string {
  try {
    return localStorage.getItem(STORAGE_KEY) ?? DEFAULT_THEME;
  } catch {
    return DEFAULT_THEME;
  }
}

const [currentTheme, setCurrentTheme] = createSignal(getCurrentTheme());

export { currentTheme };

export function setTheme(theme: string): void {
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    // localStorage may be unavailable in file:// context
  }
  document.documentElement.dataset.theme = theme;
  setCurrentTheme(theme);
}

// Apply saved theme on load
document.documentElement.dataset.theme = getCurrentTheme();

/** Theme switching — reads turbo-themes CSS via relative asset paths. */

const STORAGE_KEY = "flowscout-report-theme";
const DEFAULT_THEME = "catppuccin-mocha";

export function getCurrentTheme(): string {
  try {
    return localStorage.getItem(STORAGE_KEY) ?? DEFAULT_THEME;
  } catch {
    return DEFAULT_THEME;
  }
}

export function setTheme(theme: string): void {
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    // localStorage may be unavailable in file:// context
  }

  const link = document.getElementById("theme-css") as HTMLLinkElement | null;
  if (link) {
    const base = link.getAttribute("data-theme-base") ?? "assets/themes/";
    link.href = `${base}${theme}.css`;
  }
}

export const AVAILABLE_THEMES = [
  { id: "catppuccin-mocha", label: "Catppuccin Mocha" },
  { id: "tokyo-night-storm", label: "Tokyo Night Storm" },
] as const;

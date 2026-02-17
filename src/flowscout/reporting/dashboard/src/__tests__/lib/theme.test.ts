// @vitest-environment jsdom
import { describe, it, expect, beforeEach, afterEach } from "vitest";

const STORAGE_KEY = "flowscout-report-theme";

/** Map-backed Storage mock — Node 22+ exposes a broken native localStorage that shadows jsdom's. */
function createStorage(): Storage {
  const store = new Map<string, string>();
  return {
    getItem: (key: string) => store.get(key) ?? null,
    setItem: (key: string, value: string) => {
      store.set(key, value);
    },
    removeItem: (key: string) => {
      store.delete(key);
    },
    clear: () => {
      store.clear();
    },
    get length() {
      return store.size;
    },
    key: (index: number) => [...store.keys()][index] ?? null,
  } as Storage;
}

// Install mock before theme.ts module-level code runs
Object.defineProperty(globalThis, "localStorage", {
  value: createStorage(),
  writable: true,
  configurable: true,
});

// Import after localStorage mock is in place
const { getCurrentTheme, setTheme, currentTheme, AVAILABLE_THEMES } = await import("../../lib/theme");

describe("getCurrentTheme", () => {
  beforeEach(() => {
    Object.defineProperty(globalThis, "localStorage", {
      value: createStorage(),
      writable: true,
      configurable: true,
    });
    document.documentElement.dataset.theme = "";
  });

  it("returns default theme when nothing stored", () => {
    expect(getCurrentTheme()).toBe("catppuccin-mocha");
  });

  it("returns stored theme from localStorage", () => {
    localStorage.setItem(STORAGE_KEY, "tokyo-night-storm");
    expect(getCurrentTheme()).toBe("tokyo-night-storm");
  });
});

describe("setTheme", () => {
  beforeEach(() => {
    Object.defineProperty(globalThis, "localStorage", {
      value: createStorage(),
      writable: true,
      configurable: true,
    });
    document.documentElement.dataset.theme = "";
  });

  it("sets data-theme attribute on document element", () => {
    setTheme("tokyo-night-storm");
    expect(document.documentElement.dataset.theme).toBe("tokyo-night-storm");
  });

  it("persists to localStorage", () => {
    setTheme("tokyo-night-storm");
    expect(localStorage.getItem(STORAGE_KEY)).toBe("tokyo-night-storm");
  });

  it("updates the reactive signal", () => {
    setTheme("tokyo-night-storm");
    expect(currentTheme()).toBe("tokyo-night-storm");
  });
});

describe("AVAILABLE_THEMES", () => {
  it("has at least 2 themes", () => {
    expect(AVAILABLE_THEMES.length).toBeGreaterThanOrEqual(2);
  });

  it("each theme has id and label", () => {
    for (const theme of AVAILABLE_THEMES) {
      expect(theme.id).toBeTruthy();
      expect(theme.label).toBeTruthy();
    }
  });

  it("includes catppuccin-mocha as default", () => {
    expect(AVAILABLE_THEMES.some((t) => t.id === "catppuccin-mocha")).toBe(true);
  });
});

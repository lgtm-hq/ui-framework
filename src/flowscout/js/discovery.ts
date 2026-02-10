() => {
  const results: Record<string, unknown>[] = [];
  const seen = new Set<string>();

  function getSelector(el: Element): string {
    // 1. ID-based (most stable)
    if (el.id) return "#" + CSS.escape(el.id);

    // 2. Test IDs and data attributes
    if (el.getAttribute("data-testid")) return `[data-testid="${el.getAttribute("data-testid")}"]`;
    if (el.getAttribute("data-tab")) return `[data-tab="${el.getAttribute("data-tab")}"]`;
    if (el.getAttribute("data-theme")) return `[data-theme="${el.getAttribute("data-theme")}"]`;

    const tag = el.tagName.toLowerCase();

    // 3. Links: use href (very stable across pages)
    if (tag === "a" && el.getAttribute("href")) {
      const href = el.getAttribute("href")!;
      // For relative/absolute paths, use href selector
      if (href && !href.startsWith("javascript:") && !href.startsWith("#")) {
        const escaped = CSS.escape(href);
        // Verify uniqueness
        if (document.querySelectorAll(`a[href="${escaped}"]`).length === 1) {
          return `a[href="${escaped}"]`;
        }
      }
    }

    // 4. Aria-label (stable across pages for nav/buttons)
    const ariaLabel = el.getAttribute("aria-label");
    if (ariaLabel) {
      const sel = `${tag}[aria-label="${CSS.escape(ariaLabel)}"]`;
      if (document.querySelectorAll(sel).length === 1) return sel;
    }

    // 5. Role + accessible name
    const role = el.getAttribute("role");
    if (role) {
      const name = el.getAttribute("aria-label") || el.textContent!.trim().substring(0, 40);
      if (name) {
        const sel = `[role="${role}"]`;
        // If role alone is unique, use it; otherwise combine with text
        if (document.querySelectorAll(sel).length === 1) return sel;
      }
    }

    // 6. Name attribute (for form elements)
    if ((el as HTMLInputElement).name) {
      const sel = `${tag}[name="${CSS.escape((el as HTMLInputElement).name)}"]`;
      if (document.querySelectorAll(sel).length === 1) return sel;
    }

    // 7. Type attribute for inputs
    if (tag === "input" && (el as HTMLInputElement).type) {
      const sel = `input[type="${(el as HTMLInputElement).type}"]`;
      if (document.querySelectorAll(sel).length === 1) return sel;
    }

    // 8. Fallback: positional selector
    const parent = el.parentElement;
    if (!parent) return tag;

    const siblings = Array.from(parent.children).filter((c) => c.tagName === el.tagName);
    if (siblings.length === 1) {
      const parentSel = getSelector(parent);
      return parentSel + " > " + tag;
    }
    const idx = siblings.indexOf(el) + 1;
    const parentSel = getSelector(parent);
    return parentSel + " > " + tag + ":nth-of-type(" + idx + ")";
  }

  function sanitizeLabel(raw: string): string {
    // Strip CSS block patterns: .class-name:pseudo { ... }
    let text = raw.replace(/\.[a-zA-Z0-9_-]+(?::[\w-]+)?\s*\{[^}]*\}/g, "");
    // Strip any remaining { ... } fragments
    text = text.replace(/\{[^}]*\}/g, "");
    // Collapse whitespace
    text = text.trim().replace(/\s+/g, " ");
    if (text.length <= 80) return text;
    return text.substring(0, 77) + "...";
  }

  function getLabel(el: Element): string {
    // Check aria-label first
    const ariaLabel = el.getAttribute("aria-label");
    if (ariaLabel) return ariaLabel.trim();

    // Input buttons expose their user-facing caption via value.
    if (el instanceof HTMLInputElement) {
      const type = (el.type || "").toLowerCase();
      if (["submit", "button", "reset", "image"].includes(type)) {
        const valueLabel = (el.value || "").trim();
        if (valueLabel) return valueLabel;
      }
    }

    // Check associated label
    if (el.id) {
      const label = document.querySelector(`label[for="${el.id}"]`);
      if (label) {
        const labelText = (label as HTMLElement).innerText || label.textContent || "";
        return sanitizeLabel(labelText);
      }
    }

    // Input placeholders and names are better than empty text nodes.
    if (el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement) {
      const placeholder = (el.getAttribute("placeholder") || "").trim();
      if (placeholder) return placeholder;
      const name = (el.getAttribute("name") || "").trim();
      if (name) return name;
    }

    // Use innerText (respects visibility, ignores CSS pseudo-elements)
    // Fall back to textContent for non-HTMLElement nodes
    const text = (el as HTMLElement).innerText || el.textContent || "";
    return sanitizeLabel(text);
  }

  function isVisible(el: Element): boolean {
    const node = el as HTMLElement;

    // Modern visibility API catches many CSS-hidden cases.
    const checkVisibilityFn = (node as any).checkVisibility;
    if (typeof checkVisibilityFn === "function") {
      try {
        if (!checkVisibilityFn.call(node, { checkOpacity: true, checkVisibilityCSS: true })) {
          return false;
        }
      } catch {
        // Fallback to manual checks below.
      }
    }

    const style = getComputedStyle(node);
    if (style.display === "none" || style.visibility === "hidden" || style.visibility === "collapse")
      return false;
    if (Number.parseFloat(style.opacity || "1") === 0) return false;
    if (node.hasAttribute("hidden") || node.getAttribute("aria-hidden") === "true") return false;
    if (node.closest("[hidden], [aria-hidden='true']")) return false;

    const rect = node.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return false;

    const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    if (rect.bottom < 0 || rect.right < 0 || rect.top > viewportHeight || rect.left > viewportWidth) {
      return false;
    }

    // Ensure the element is actually hit-test visible in the viewport.
    const centerX = Math.min(Math.max(rect.left + rect.width / 2, 0), Math.max(viewportWidth - 1, 0));
    const centerY = Math.min(Math.max(rect.top + rect.height / 2, 0), Math.max(viewportHeight - 1, 0));
    const topElement = document.elementFromPoint(centerX, centerY);
    if (!topElement) return false;
    return topElement === node || node.contains(topElement) || topElement.contains(node);
  }

  function getDataAttrs(el: Element): Record<string, string> {
    const data: Record<string, string> = {};
    for (const attr of Array.from(el.attributes)) {
      if (attr.name.startsWith("data-")) {
        data[attr.name] = attr.value;
      }
    }
    return data;
  }

  function getBBox(el: Element): { x: number; y: number; width: number; height: number } {
    const r = el.getBoundingClientRect();
    return { x: r.x, y: r.y, width: r.width, height: r.height };
  }

  const selectors = [
    "a[href]",
    "button",
    '[role="button"]',
    '[role="tab"]',
    '[role="link"]',
    '[role="menuitem"]',
    '[role="option"]',
    '[role="search"]',
    'input:not([type="hidden"])',
    "select",
    "textarea",
    "[aria-expanded]",
    "[aria-haspopup]",
    "[data-tab]",
    "details > summary",
  ];

  const elements = document.querySelectorAll(selectors.join(", "));

  for (const el of Array.from(elements)) {
    const selector = getSelector(el);
    if (seen.has(selector)) continue;
    seen.add(selector);

    const tag = el.tagName.toLowerCase();
    const visible = isVisible(el);

    // Collect select options
    let options: string[] = [];
    if (tag === "select") {
      options = Array.from((el as HTMLSelectElement).options).map(
        (o) => o.value || o.textContent!.trim(),
      );
    }

    // Find parent form
    let parentForm: string | null = null;
    const form = el.closest("form");
    if (form) parentForm = getSelector(form);

    results.push({
      selector: selector,
      dom_id: el.id || null,
      tag: tag,
      input_type: el.getAttribute("type") || null,
      role: el.getAttribute("role") || null,
      aria_label: el.getAttribute("aria-label") || null,
      aria_expanded: el.getAttribute("aria-expanded"),
      href: el.getAttribute("href") || null,
      name: el.getAttribute("name") || null,
      placeholder: el.getAttribute("placeholder") || null,
      value: (el as HTMLInputElement).value || null,
      required: (el as HTMLInputElement).required || el.getAttribute("aria-required") === "true",
      disabled: (el as HTMLInputElement).disabled || el.getAttribute("aria-disabled") === "true",
      visible: visible,
      label: getLabel(el),
      options: options,
      parent_form: parentForm,
      bbox: visible ? getBBox(el) : null,
      data_attrs: getDataAttrs(el),
    });
  }

  return results;
};

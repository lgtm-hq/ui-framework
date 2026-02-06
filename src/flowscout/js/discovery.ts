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

  function getLabel(el: Element): string {
    // Check aria-label first
    const ariaLabel = el.getAttribute("aria-label");
    if (ariaLabel) return ariaLabel.trim();

    // Check associated label
    if (el.id) {
      const label = document.querySelector(`label[for="${el.id}"]`);
      if (label) return label.textContent!.trim();
    }

    // Check innerText (truncated)
    const text = el.textContent || "";
    const trimmed = text.trim().replace(/\s+/g, " ");
    if (trimmed.length <= 80) return trimmed;
    return trimmed.substring(0, 77) + "...";
  }

  function isVisible(el: Element): boolean {
    if ((el as HTMLElement).offsetParent === null && getComputedStyle(el).position !== "fixed")
      return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
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

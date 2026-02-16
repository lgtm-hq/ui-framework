/**
 * Browser-side DOM structural analysis for smart flow framework.
 *
 * Runs in-page and returns:
 * - repeated_groups: structurally similar sibling groups
 * - content_metrics: text/heading/image/link/form/interactive counts
 * - zone_hints: booleans for nav, search, pagination, filters, hero, single heading
 * - structural_skeleton: content-blind DOM skeleton for archetype matching
 * - extracted_entities: text from repeated structures + h2s
 * - element_catalog: all interactive + content elements with zone classification
 */
(() => {
  // --- Repeated Groups ---
  function findRepeatedGroups(): Array<{
    parent_selector: string;
    count: number;
    tag_signature: string;
    item_texts: string[];
    item_selectors: string[];
  }> {
    const groups: Array<{
      parent_selector: string;
      count: number;
      tag_signature: string;
      item_texts: string[];
      item_selectors: string[];
    }> = [];

    const containers = document.querySelectorAll(
      "main, [role='main'], .content, #content, article, section, .container, .wrapper, body",
    );

    const visited = new Set<Element>();

    containers.forEach((container) => {
      // Group direct children by tag skeleton
      const childMap = new Map<string, Element[]>();

      Array.from(container.children).forEach((child) => {
        if (visited.has(child)) return;
        const skeleton = getTagSkeleton(child, 3);
        if (!skeleton) return;
        const list = childMap.get(skeleton) || [];
        list.push(child);
        childMap.set(skeleton, list);
      });

      childMap.forEach((items, signature) => {
        if (items.length < 3) return;
        items.forEach((el) => visited.add(el));

        const parentSel = buildSelector(container);
        const itemTexts = items.slice(0, 10).map((el) => {
          const h = el.querySelector("h1, h2, h3, h4, h5, h6, a");
          return (h ? (h.textContent ?? "") : (el.textContent ?? "")).trim().slice(0, 100);
        });
        const itemSelectors = items.slice(0, 3).map((el) => buildSelector(el));

        groups.push({
          parent_selector: parentSel,
          count: items.length,
          tag_signature: signature,
          item_texts: itemTexts.filter((t) => t.length > 0),
          item_selectors: itemSelectors,
        });
      });
    });

    return groups;
  }

  function getTagSkeleton(el: Element, depth: number): string {
    if (depth <= 0 || !el.tagName) return "";
    const tag = el.tagName.toLowerCase();
    if (depth === 1) return tag;

    const childSigs = Array.from(el.children)
      .slice(0, 6)
      .map((child) => getTagSkeleton(child, depth - 1))
      .filter((s) => s.length > 0);

    return childSigs.length > 0 ? `${tag}>${childSigs.join("+")}` : tag;
  }

  // --- Content Metrics ---
  function getContentMetrics(): {
    total_text_length: number;
    heading_count: number;
    h1_texts: string[];
    h2_texts: string[];
    image_count: number;
    link_count: number;
    form_input_count: number;
    interactive_count: number;
  } {
    const body = document.body;
    const textLen = (body.innerText || "").length;
    const headings = body.querySelectorAll("h1, h2, h3, h4, h5, h6");
    const h1s = Array.from(body.querySelectorAll("h1")).map((h) => (h.textContent || "").trim());
    const h2s = Array.from(body.querySelectorAll("h2")).map((h) => (h.textContent || "").trim());
    const images = body.querySelectorAll("img, picture, svg[role='img']");
    const links = body.querySelectorAll("a[href]");
    const inputs = body.querySelectorAll("input, textarea, select");
    const interactives = body.querySelectorAll(
      "a, button, input, textarea, select, [role='button'], [role='link'], [role='tab'], [onclick]",
    );

    return {
      total_text_length: textLen,
      heading_count: headings.length,
      h1_texts: h1s.slice(0, 5),
      h2_texts: h2s.slice(0, 10),
      image_count: images.length,
      link_count: links.length,
      form_input_count: inputs.length,
      interactive_count: interactives.length,
    };
  }

  // --- Zone Hints ---
  function getZoneHints(): {
    has_nav: boolean;
    has_search_input: boolean;
    has_pagination: boolean;
    has_filters: boolean;
    has_hero: boolean;
    has_single_heading_focus: boolean;
  } {
    const body = document.body;
    const hasNav = body.querySelector("nav, [role='navigation']") !== null;
    const hasSearch =
      body.querySelector(
        "input[type='search'], [role='search'], input[placeholder*='earch'], input[aria-label*='earch']",
      ) !== null;
    const hasPagination =
      body.querySelector(
        "[aria-label*='agination'], .pagination, .pager, nav[aria-label*='age'], [role='navigation'][aria-label*='age']",
      ) !== null;
    const hasFilters =
      body.querySelector(
        "[aria-label*='ilter'], .filter, .filters, select[name*='filter'], select[name*='sort']",
      ) !== null;
    const hasHero =
      body.querySelector(".hero, [class*='hero'], .banner, [class*='banner'], .jumbotron") !== null;

    const h1s = body.querySelectorAll("h1");
    const h2s = body.querySelectorAll("h2");
    const hasSingleHeadingFocus = h1s.length === 1 && h2s.length <= 2;

    return {
      has_nav: hasNav,
      has_search_input: hasSearch,
      has_pagination: hasPagination,
      has_filters: hasFilters,
      has_hero: hasHero,
      has_single_heading_focus: hasSingleHeadingFocus,
    };
  }

  // --- Structural Skeleton ---
  function getStructuralSkeleton(): string {
    const main = document.querySelector("main, [role='main']") || document.body;
    return buildSkeleton(main, 4);
  }

  function buildSkeleton(el: Element, depth: number): string {
    if (depth <= 0) return "";
    const tag = el.tagName.toLowerCase();
    if (depth === 1) return tag;
    const children = Array.from(el.children)
      .slice(0, 20)
      .map((c) => buildSkeleton(c, depth - 1))
      .filter((s) => s.length > 0);
    return children.length > 0 ? `${tag}(${children.join(",")})` : tag;
  }

  // --- Extracted Entities ---
  function extractEntities(groups: Array<{ item_texts: string[] }>, h2Texts: string[]): string[] {
    const entities: string[] = [];
    const seen = new Set<string>();

    // Entities from repeated group items
    for (const group of groups) {
      for (const text of group.item_texts) {
        const clean = text.trim();
        if (clean && !seen.has(clean.toLowerCase()) && clean.length <= 100) {
          seen.add(clean.toLowerCase());
          entities.push(clean);
        }
      }
    }

    // h2 headings
    for (const text of h2Texts) {
      const clean = text.trim();
      if (clean && !seen.has(clean.toLowerCase()) && clean.length <= 100) {
        seen.add(clean.toLowerCase());
        entities.push(clean);
      }
    }

    return entities.slice(0, 30);
  }

  function isElementVisible(el: Element): boolean {
    const node = el as HTMLElement;
    const style = window.getComputedStyle(node);
    if (
      style.display === "none" ||
      style.visibility === "hidden" ||
      style.visibility === "collapse"
    ) {
      return false;
    }
    if (Number.parseFloat(style.opacity || "1") === 0) {
      return false;
    }
    if (node.hasAttribute("hidden") || node.getAttribute("aria-hidden") === "true") {
      return false;
    }
    if (node.closest("[hidden], [aria-hidden='true']")) {
      return false;
    }

    const rect = node.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  }

  // --- Interactive element check ---
  const INTERACTIVE_TAGS = new Set(["a", "button", "input", "textarea", "select"]);
  const INTERACTIVE_ROLES = new Set([
    "button",
    "link",
    "tab",
    "menuitem",
    "option",
    "switch",
    "checkbox",
    "radio",
    "slider",
    "spinbutton",
    "combobox",
    "searchbox",
    "textbox",
  ]);

  function isInteractiveElement(el: Element): boolean {
    const tag = el.tagName.toLowerCase();
    if (INTERACTIVE_TAGS.has(tag)) return true;
    const role = el.getAttribute("role") || "";
    if (INTERACTIVE_ROLES.has(role)) return true;
    if (el.hasAttribute("onclick") || el.hasAttribute("tabindex")) return true;
    return false;
  }

  // --- Data attributes ---
  function getDataAttributes(el: Element): Record<string, string> {
    const attrs: Record<string, string> = {};
    const dataset = (el as HTMLElement).dataset;
    if (!dataset) return attrs;
    for (const key of Object.keys(dataset)) {
      const val = dataset[key];
      if (val !== undefined) {
        attrs[key] = val.slice(0, 100);
      }
    }
    return attrs;
  }

  // --- Parent info ---
  function getParentInfo(el: Element): { selector: string; tag: string } | null {
    const parent = el.parentElement;
    if (!parent || parent === document.body || parent === document.documentElement) {
      return null;
    }
    return { selector: buildSelector(parent), tag: parent.tagName.toLowerCase() };
  }

  // --- Element Catalog ---
  interface CatalogItem {
    selector: string;
    xpath: string;
    dom_id: string;
    tag: string;
    label: string;
    visible_text: string;
    zone: string;
    element_type: string;
    aria_role: string;
    aria_label: string;
    input_type: string;
    is_visible: boolean;
    is_interactive: boolean;
    href: string;
    src: string;
    name: string;
    parent_selector: string;
    parent_tag: string;
    bounding_box: { x: number; y: number; width: number; height: number } | null;
    data_attributes: Record<string, string>;
  }

  function buildElementCatalog(): CatalogItem[] {
    const catalog: CatalogItem[] = [];

    // Query ALL semantic, interactive, and content elements
    const allElements = document.querySelectorAll(
      "a, button, input, textarea, select, label, " +
        "h1, h2, h3, h4, h5, h6, p, img, picture, video, audio, " +
        "table, ul, ol, li, dl, dt, dd, " +
        "nav, header, footer, main, aside, section, article, " +
        "form, fieldset, legend, " +
        "[role='button'], [role='link'], [role='tab'], " +
        "[role='menuitem'], [role='option'], [role='search'], " +
        "[role='navigation'], [role='banner'], [role='contentinfo'], " +
        "[role='complementary'], [role='main'], " +
        "[onclick], [tabindex]",
    );

    const seen = new Set<string>();

    allElements.forEach((el) => {
      const selector = buildSelector(el);
      if (seen.has(selector)) return;
      seen.add(selector);

      const tag = el.tagName.toLowerCase();
      const isVisible = isElementVisible(el);

      // Get visible text (trimmed, max 200 chars)
      const rawText = (el.textContent || "").trim();
      const visibleText = rawText.length > 200 ? rawText.slice(0, 200) : rawText;

      const parentInfo = getParentInfo(el);

      const rect = el.getBoundingClientRect();
      const bbox = isVisible
        ? { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
        : null;

      catalog.push({
        selector,
        xpath: buildXPath(el),
        dom_id: el.id || "",
        tag,
        label: getElementLabel(el),
        visible_text: visibleText,
        zone: classifyZone(el),
        element_type: classifyElementType(el),
        aria_role: el.getAttribute("role") || "",
        aria_label: el.getAttribute("aria-label") || "",
        input_type: (el as HTMLInputElement).type || "",
        is_visible: isVisible,
        is_interactive: isInteractiveElement(el),
        href: (el as HTMLAnchorElement).href || el.getAttribute("href") || "",
        src: (el as HTMLImageElement).src || el.getAttribute("src") || "",
        name: (el as HTMLInputElement).name || el.getAttribute("name") || "",
        parent_selector: parentInfo?.selector || "",
        parent_tag: parentInfo?.tag || "",
        bounding_box: bbox,
        data_attributes: getDataAttributes(el),
      });
    });

    return catalog;
  }

  // --- Form Structures ---
  interface FormFieldItem {
    selector: string;
    name: string;
    input_type: string;
    label: string;
    is_required: boolean;
    placeholder: string;
    options: string[];
    validation_pattern: string;
  }

  interface FormStructureItem {
    form_selector: string;
    action: string;
    method: string;
    fields: FormFieldItem[];
    submit_selector: string;
  }

  function buildFormStructures(): FormStructureItem[] {
    const forms = document.querySelectorAll("form");
    const structures: FormStructureItem[] = [];

    forms.forEach((form) => {
      const formSelector = buildSelector(form);
      const fields: FormFieldItem[] = [];
      let submitSelector = "";

      const inputs = form.querySelectorAll("input, textarea, select");
      inputs.forEach((input) => {
        const inputEl = input as HTMLInputElement;
        const inputType = inputEl.type || "text";

        // Skip hidden and submit inputs from field list
        if (inputType === "hidden" || inputType === "submit") {
          if (inputType === "submit" && !submitSelector) {
            submitSelector = buildSelector(input);
          }
          return;
        }

        // Find associated label
        let fieldLabel = "";
        if (inputEl.id) {
          const labelEl = form.querySelector(`label[for="${CSS.escape(inputEl.id)}"]`);
          if (labelEl) {
            fieldLabel = (labelEl.textContent || "").trim().slice(0, 100);
          }
        }
        if (!fieldLabel) {
          const parentLabel = input.closest("label");
          if (parentLabel) {
            fieldLabel = (parentLabel.textContent || "").trim().slice(0, 100);
          }
        }
        if (!fieldLabel) {
          fieldLabel = inputEl.getAttribute("aria-label") || "";
        }

        // Collect options for selects
        const options: string[] = [];
        if (input.tagName.toLowerCase() === "select") {
          const selectEl = input as HTMLSelectElement;
          Array.from(selectEl.options).forEach((opt) => {
            if (opt.value) {
              options.push(opt.value);
            }
          });
        }

        fields.push({
          selector: buildSelector(input),
          name: inputEl.name || "",
          input_type: inputType,
          label: fieldLabel,
          is_required: inputEl.required || inputEl.getAttribute("aria-required") === "true",
          placeholder: inputEl.placeholder || "",
          options,
          validation_pattern: inputEl.pattern || "",
        });
      });

      // Find submit button if not found yet
      if (!submitSelector) {
        const submitBtn = form.querySelector(
          "button[type='submit'], input[type='submit'], button:not([type])",
        );
        if (submitBtn) {
          submitSelector = buildSelector(submitBtn);
        }
      }

      structures.push({
        form_selector: formSelector,
        action: form.action || "",
        method: (form.method || "GET").toUpperCase(),
        fields,
        submit_selector: submitSelector,
      });
    });

    return structures;
  }

  function classifyZone(el: Element): string {
    let current: Element | null = el;
    while (current) {
      const tag = current.tagName.toLowerCase();
      const role = current.getAttribute("role") || "";

      if (tag === "nav" || role === "navigation") return "navigation";
      if (tag === "header" || role === "banner") return "header";
      if (tag === "footer" || role === "contentinfo") return "footer";
      if (role === "search") return "search";

      const cls = current.className || "";
      if (typeof cls === "string") {
        const clsLower = cls.toLowerCase();
        if (clsLower.includes("search")) return "search";
        if (clsLower.includes("filter")) return "filter";
        if (clsLower.includes("pagination") || clsLower.includes("pager")) return "pagination";
        if (clsLower.includes("sidebar")) return "sidebar";
        if (clsLower.includes("nav")) return "navigation";
      }

      const ariaLabel = (current.getAttribute("aria-label") || "").toLowerCase();
      if (ariaLabel.includes("pagination") || ariaLabel.includes("page")) return "pagination";
      if (ariaLabel.includes("filter")) return "filter";
      if (ariaLabel.includes("search")) return "search";

      current = current.parentElement;
    }

    return "main_content";
  }

  function classifyElementType(el: Element): string {
    const tag = el.tagName.toLowerCase();
    const role = el.getAttribute("role") || "";

    if (tag === "a") return "link";
    if (tag === "button" || role === "button") return "button";
    if (tag === "input") {
      const type = (el as HTMLInputElement).type || "text";
      return `input_${type}`;
    }
    if (tag === "select") return "select";
    if (tag === "textarea") return "textarea";
    if (tag === "label") return "label";
    if (tag === "form") return "form";
    if (tag === "fieldset") return "fieldset";
    if (tag === "legend") return "legend";
    if (role === "tab") return "tab";
    if (role === "menuitem") return "menuitem";
    if (role === "option") return "option";
    if (role === "search") return "search";
    if (tag.match(/^h[1-6]$/)) return "heading";
    if (tag === "img" || tag === "picture") return "image";
    if (tag === "video") return "video";
    if (tag === "audio") return "audio";
    if (tag === "p") return "paragraph";
    if (tag === "table") return "table";
    if (tag === "ul" || tag === "ol") return "list";
    if (tag === "li") return "list_item";
    if (tag === "dl") return "definition_list";
    if (tag === "dt") return "definition_term";
    if (tag === "dd") return "definition_detail";
    if (tag === "nav" || role === "navigation") return "navigation";
    if (tag === "header" || role === "banner") return "header";
    if (tag === "footer" || role === "contentinfo") return "footer";
    if (tag === "main" || role === "main") return "main";
    if (tag === "aside" || role === "complementary") return "aside";
    if (tag === "section") return "section";
    if (tag === "article") return "article";
    return "other";
  }

  function getElementLabel(el: Element): string {
    const ariaLabel = el.getAttribute("aria-label");
    if (ariaLabel) return ariaLabel.trim().slice(0, 100);

    const text = (el.textContent || "").trim();
    if (text && text.length <= 100) return text;
    if (text) return text.slice(0, 100);

    const alt = el.getAttribute("alt");
    if (alt) return alt.trim().slice(0, 100);

    const title = el.getAttribute("title");
    if (title) return title.trim().slice(0, 100);

    const placeholder = (el as HTMLInputElement).placeholder;
    if (placeholder) return placeholder.trim().slice(0, 100);

    return "";
  }

  // --- Selector Builder ---
  function buildSelector(el: Element): string {
    // Prefer ID
    if (el.id) return `#${CSS.escape(el.id)}`;

    // data-testid
    const testId = el.getAttribute("data-testid");
    if (testId) return `[data-testid="${CSS.escape(testId)}"]`;

    // aria-label
    const ariaLabel = el.getAttribute("aria-label");
    if (ariaLabel) {
      const tag = el.tagName.toLowerCase();
      return `${tag}[aria-label="${CSS.escape(ariaLabel)}"]`;
    }

    // href for links
    const tag = el.tagName.toLowerCase();
    if (tag === "a") {
      const href = el.getAttribute("href");
      if (href && href !== "#" && href.length < 100) {
        return `a[href="${CSS.escape(href)}"]`;
      }
    }

    // role
    const role = el.getAttribute("role");
    if (role) {
      const name = ariaLabel || (el.textContent || "").trim().slice(0, 30);
      if (name) {
        return `[role="${role}"]`;
      }
    }

    // nth-of-type fallback
    if (el.parentElement) {
      const parent = buildSelector(el.parentElement);
      const siblings = Array.from(el.parentElement.children).filter(
        (c) => c.tagName === el.tagName,
      );
      if (siblings.length === 1) {
        return `${parent} > ${tag}`;
      }
      const index = siblings.indexOf(el) + 1;
      return `${parent} > ${tag}:nth-of-type(${index})`;
    }

    return tag;
  }

  function buildXPath(el: Element): string {
    if (el.id) {
      return `//*[@id=${JSON.stringify(el.id)}]`;
    }

    const segments: string[] = [];
    let current: Element | null = el;
    while (current !== null) {
      const node: Element = current;
      const tag = node.tagName.toLowerCase();
      const parentEl: Element | null = node.parentElement;
      if (!parentEl) {
        segments.unshift(tag);
        break;
      }

      const siblings = Array.from(parentEl.children).filter(
        (child): child is Element => child.tagName === node.tagName,
      );
      const index = siblings.indexOf(node) + 1;
      segments.unshift(`${tag}[${index}]`);
      current = parentEl;
    }

    return `/${segments.join("/")}`;
  }

  // --- Main ---
  const repeatedGroups = findRepeatedGroups();
  const metrics = getContentMetrics();
  const zoneHints = getZoneHints();
  const skeleton = getStructuralSkeleton();
  const entities = extractEntities(repeatedGroups, metrics.h2_texts);
  const catalog = buildElementCatalog();
  const formStructures = buildFormStructures();

  return {
    repeated_groups: repeatedGroups,
    content_metrics: metrics,
    zone_hints: zoneHints,
    structural_skeleton: skeleton,
    extracted_entities: entities,
    element_catalog: catalog,
    form_structures: formStructures,
  };
})();

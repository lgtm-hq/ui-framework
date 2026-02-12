() => {
  const parts: string[] = [];
  // Select values
  document.querySelectorAll("select").forEach((el) => {
    const sel = el as HTMLSelectElement;
    parts.push(sel.name + "=" + sel.value);
  });
  // Checked checkboxes and radios
  document
    .querySelectorAll('input[type="checkbox"]:checked, input[type="radio"]:checked')
    .forEach((el) => {
      const inp = el as HTMLInputElement;
      parts.push((inp.name || inp.id) + "=checked");
    });
  // Non-empty text inputs
  document
    .querySelectorAll('input[type="text"], input[type="email"], input[type="search"], textarea')
    .forEach((el) => {
      const inp = el as HTMLInputElement;
      if (inp.value) parts.push((inp.name || inp.id) + "=" + inp.value.substring(0, 50));
    });
  // Expanded dropdowns
  document.querySelectorAll('[aria-expanded="true"]').forEach((el) => {
    parts.push("expanded:" + (el.id || el.getAttribute("aria-label") || "unknown"));
  });
  // Active theme or similar data attributes
  const themeEl = document.querySelector("[data-theme]");
  if (themeEl) parts.push("theme=" + themeEl.getAttribute("data-theme"));
  return parts.join("|");
};

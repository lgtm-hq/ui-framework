() => {
  const parts: string[] = [];
  // Headings
  document.querySelectorAll("h1, h2, h3").forEach((el) => {
    if ((el as HTMLElement).offsetParent !== null) parts.push(el.textContent!.trim());
  });
  // Active navigation items
  document.querySelectorAll("[aria-current], .active, .is-active, [data-active]").forEach((el) => {
    parts.push(el.textContent!.trim().substring(0, 100));
  });
  // Selected tabs
  document
    .querySelectorAll('[role="tab"][aria-selected="true"], [data-tab].active, [data-tab].is-active')
    .forEach((el) => {
      parts.push(el.textContent!.trim());
    });
  // Page title
  parts.push(document.title);
  return parts.filter((p) => p).join("|");
};

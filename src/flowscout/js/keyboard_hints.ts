() => {
  const hints: string[] = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  const pattern = /(ctrl|cmd|alt|shift|meta)\s*[+]\s*[a-z0-9]/gi;
  while (walker.nextNode()) {
    const text = walker.currentNode.textContent!;
    const matches = text.match(pattern);
    if (matches) {
      for (const m of matches) hints.push(m.trim());
    }
  }
  // Also check title and aria-label attributes
  document.querySelectorAll("[title], [aria-label], [aria-keyshortcuts]").forEach((el) => {
    const title = el.getAttribute("title") || "";
    const label = el.getAttribute("aria-label") || "";
    const shortcut = el.getAttribute("aria-keyshortcuts") || "";
    for (const text of [title, label, shortcut]) {
      const matches = text.match(pattern);
      if (matches) {
        for (const m of matches) hints.push(m.trim());
      }
    }
  });
  return [...new Set(hints)];
};

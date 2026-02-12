() => {
  function walk(node: Element): string {
    if (!node || node.nodeType !== 1) return "";
    const tag = node.tagName.toLowerCase();
    if (["script", "style", "noscript"].includes(tag)) return "";
    const role = node.getAttribute("role") || "";
    const type = tag === "input" ? (node as HTMLInputElement).getAttribute("type") || "text" : "";
    const childStrs: string[] = [];
    for (const child of Array.from(node.children)) {
      if (!child) continue;
      const s = walk(child);
      if (s) childStrs.push(s);
    }
    const children = childStrs.join("");
    return (
      "<" +
      tag +
      (role ? ":" + role : "") +
      (type ? "." + type : "") +
      ">" +
      children +
      "</" +
      tag +
      ">"
    );
  }
  if (!document.body) return "";
  return walk(document.body);
};

function getText() {
  const bad = new Set(["SCRIPT", "STYLE", "NOSCRIPT"]);
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);

  let out = [];
  let node;
  while ((node = walker.nextNode())) {
    const parent = node.parentElement;
    if (!parent || bad.has(parent.tagName)) continue;
    const t = (node.textContent || "").replace(/\s+/g, " ").trim();
    if (!t) continue;
    out.push(t);
    if (out.join(" ").length > 14000) break;
  }
  return out.join(" ");
}

chrome.runtime.onMessage.addListener((msg, _, sendResponse) => {
  if (msg?.type === "GET_PAGE") {
    sendResponse({
      ok: true,
      title: document.title || "",
      url: location.href,
      text: getText()
    });
  }
});

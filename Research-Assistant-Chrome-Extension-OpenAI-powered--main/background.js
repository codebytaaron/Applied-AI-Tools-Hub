async function activeTabId() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) throw new Error("No active tab");
  return tab.id;
}

async function ensureContentScript(tabId) {
  // MV3: inject when needed
  await chrome.scripting.executeScript({
    target: { tabId },
    files: ["content.js"]
  });
}

async function getPage() {
  const tabId = await activeTabId();
  await ensureContentScript(tabId);

  const page = await new Promise((resolve) => {
    chrome.tabs.sendMessage(tabId, { type: "GET_PAGE" }, (resp) => resolve(resp));
  });

  if (!page?.ok) throw new Error("Could not read page");
  return page;
}

function rootDomain(hostname) {
  const parts = (hostname || "").split(".").filter(Boolean);
  if (parts.length <= 2) return hostname;
  return parts.slice(-2).join(".");
}

async function openaiCall({ apiKey, prompt }) {
  // Uses OpenAI Responses API style payload (simple + robust)
  const res = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4.1-mini",
      input: prompt
    })
  });

  if (!res.ok) {
    const t = await res.text().catch(() => "");
    throw new Error(`OpenAI error (${res.status}): ${t.slice(0, 200)}`);
  }

  const data = await res.json();
  // Pull text output safely
  const text =
    data.output_text ||
    (data.output?.map(o => o.content?.map(c => c.text).join("")).join("\n") ?? "");
  return text.trim();
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  (async () => {
    if (msg?.type === "RUN") {
      const { mode } = msg;
      const { apiKey } = await chrome.storage.local.get(["apiKey"]);
      if (!apiKey) return sendResponse({ ok: false, error: "Missing API key" });

      const page = await getPage();
      const host = new URL(page.url).hostname;
      const domain = rootDomain(host);

      const system =
        "You are a helpful research assistant. Be concise. Use bullet points. Do not invent facts. If missing, say 'Not found on this page'.";

      const modePrompts = {
        summarize: "Summarize this page in 6 to 10 bullets.",
        requirements: "Extract any requirements, eligibility, or needed materials. If none, say so.",
        dates: "Extract any dates, deadlines, timelines, or time-related info. If none, say so.",
        nextclicks: "Suggest 5 to 8 next links or sections a person should look for next based on this page (example: cost, requirements, deadlines, contact).",
        checklist: "Create a checklist of action items a person should do after reading this page."
      };

      const task = modePrompts[mode] || modePrompts.summarize;

      const prompt = `${system}

TASK: ${task}

PAGE TITLE: ${page.title}
PAGE URL: ${page.url}

PAGE TEXT (may be truncated):
${page.text}`;

      const output = await openaiCall({ apiKey, prompt });

      // Save per domain history
      const key = `history:${domain}`;
      const existing = await chrome.storage.local.get([key]);
      const history = Array.isArray(existing[key]) ? existing[key] : [];
      history.unshift({
        ts: Date.now(),
        mode,
        title: page.title,
        url: page.url,
        output
      });
      if (history.length > 50) history.length = 50;
      await chrome.storage.local.set({ [key]: history });

      sendResponse({ ok: true, domain, result: output, title: page.title, url: page.url });
      return;
    }

    if (msg?.type === "SAVE_KEY") {
      const { apiKey } = msg;
      await chrome.storage.local.set({ apiKey });
      sendResponse({ ok: true });
      return;
    }

    if (msg?.type === "GET_HISTORY") {
      const { domain } = msg;
      const key = `history:${domain}`;
      const existing = await chrome.storage.local.get([key]);
      sendResponse({ ok: true, history: existing[key] || [] });
      return;
    }

    sendResponse({ ok: false, error: "Unknown message" });
  })().catch((err) => sendResponse({ ok: false, error: err.message }));
  return true;
});

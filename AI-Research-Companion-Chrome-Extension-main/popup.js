const $ = (id) => document.getElementById(id);

function setStatus(t) { $("status").textContent = t || ""; }
function setOutput(t) { $("out").textContent = t || ""; }

async function saveKey() {
  const apiKey = $("key").value.trim();
  if (!apiKey) return setStatus("Paste your API key first.");
  const resp = await chrome.runtime.sendMessage({ type: "SAVE_KEY", apiKey });
  setStatus(resp.ok ? "Saved." : resp.error || "Error saving.");
}

async function run(mode) {
  setStatus("Working...");
  setOutput("");

  const resp = await chrome.runtime.sendMessage({ type: "RUN", mode });
  if (!resp.ok) {
    setStatus(resp.error || "Failed.");
    return;
  }

  $("meta").textContent = `${resp.domain} • ${resp.title}`;
  setOutput(resp.result);
  setStatus("Done.");

  await loadHistory(resp.domain);
}

async function loadHistory(domain) {
  const resp = await chrome.runtime.sendMessage({ type: "GET_HISTORY", domain });
  if (!resp.ok) return;

  const hist = resp.history || [];
  if (!hist.length) {
    $("hist").textContent = "(none yet)";
    return;
  }

  $("hist").innerHTML = "";
  for (const item of hist.slice(0, 5)) {
    const div = document.createElement("div");
    div.className = "hist-item";

    const a = document.createElement("a");
    a.href = item.url;
    a.textContent = `${item.mode} • ${item.title || item.url}`;
    a.target = "_blank";

    const small = document.createElement("div");
    small.className = "small";
    const d = new Date(item.ts);
    small.textContent = d.toLocaleString();

    div.appendChild(a);
    div.appendChild(small);
    $("hist").appendChild(div);
  }
}

document.addEventListener("click", (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;

  if (btn.id === "save") saveKey();
  const mode = btn.dataset.mode;
  if (mode) run(mode);
});

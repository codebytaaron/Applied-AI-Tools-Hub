const $ = (id) => document.getElementById(id);

function setStatus(msg) {
  $("status").textContent = msg || "";
}

function setOutput(tags) {
  const text = tags && tags.length ? tags.join(" ") : "";
  $("out").textContent = text || "No hashtags returned.";
  $("copyBtn").disabled = !text;
}

$("genBtn").addEventListener("click", async () => {
  const payload = {
    platform: $("platform").value,
    caption: $("caption").value.trim(),
    context: $("context").value.trim(),
    niche: $("niche").value.trim(),
    hashtag_count: parseInt($("count").value || "18", 10),
    include_branded: $("includeBrand").checked,
    brand_tag: $("brand").value.trim()
  };

  if (!payload.caption) {
    setStatus("Add a caption first.");
    return;
  }

  setStatus("Generating...");
  $("genBtn").disabled = true;
  setOutput([]);

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Request failed");
    const data = await res.json();

    $("source").textContent = `source: ${data.source || "-"}`;
    setOutput(data.hashtags || []);
    setStatus("");
  } catch (e) {
    setStatus("Something broke. Check the server console.");
  } finally {
    $("genBtn").disabled = false;
  }
});

$("copyBtn").addEventListener("click", async () => {
  const text = $("out").textContent;
  if (!text) return;
  await navigator.clipboard.writeText(text);
  setStatus("Copied.");
  setTimeout(() => setStatus(""), 1200);
});

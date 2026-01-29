"use client";

import { useMemo, useState } from "react";

const AUDIENCES = [
  { id: "middle_school", label: "Middle school" },
  { id: "high_school", label: "High school" },
  { id: "general", label: "General public" },
  { id: "professional", label: "Professional" }
];

export default function Page() {
  const [text, setText] = useState("");
  const [audience, setAudience] = useState("high_school");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const [report, setReport] = useState(null);

  const canSubmit = useMemo(() => text.trim().length >= 10 && !loading, [text, loading]);

  async function analyze() {
    setErr("");
    setReport(null);
    setLoading(true);

    try {
      const res = await fetch("/api/clarity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, audience })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data?.error || "Analysis failed");

      setReport(data);
    } catch (e) {
      setErr(e?.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  function copySummary() {
    if (!report) return;
    const lines = [];
    lines.push(`Clarity score: ${report.clarity_score}/100`);
    lines.push(`Reading level: ${report.reading_level_guess}`);
    lines.push("");
    lines.push("Top issues:");
    (report.top_issues || []).forEach((i, idx) => {
      lines.push(`${idx + 1}. ${i.issue} (severity: ${i.severity})`);
      if (i.fix) lines.push(`   Fix: ${i.fix}`);
    });
    navigator.clipboard.writeText(lines.join("\n"));
  }

  return (
    <main style={styles.main}>
      <div style={styles.card}>
        <div style={styles.headerRow}>
          <h1 style={styles.h1}>ClarityCheck AI</h1>
          <span style={styles.badge}>Clarity analyzer</span>
        </div>

        <p style={styles.sub}>
          Paste text and get a clarity score plus specific, actionable feedback (no full rewrites).
        </p>

        <label style={styles.label}>Text</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste your paragraph, email, essay section, etc."
          style={styles.textarea}
        />

        <div style={styles.controls}>
          <div>
            <label style={styles.label}>Audience</label>
            <select value={audience} onChange={(e) => setAudience(e.target.value)} style={styles.select}>
              {AUDIENCES.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.label}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={analyze}
            disabled={!canSubmit}
            style={{ ...styles.button, opacity: canSubmit ? 1 : 0.6 }}
          >
            {loading ? "Analyzing..." : "Analyze clarity"}
          </button>
        </div>

        {err ? <p style={styles.error}>{err}</p> : null}

        <div style={{ marginTop: 16 }}>
          <label style={styles.label}>Report</label>
          <div style={styles.reportBox}>
            {!report ? (
              <p style={styles.placeholder}>Your report will appear here.</p>
            ) : (
              <div style={{ display: "grid", gap: 14 }}>
                <div style={styles.metricsRow}>
                  <div style={styles.metric}>
                    <div style={styles.metricLabel}>Clarity score</div>
                    <div style={styles.metricValue}>{report.clarity_score}/100</div>
                  </div>
                  <div style={styles.metric}>
                    <div style={styles.metricLabel}>Reading level</div>
                    <div style={styles.metricValue}>{report.reading_level_guess}</div>
                  </div>
                  <div style={styles.metric}>
                    <div style={styles.metricLabel}>Confidence</div>
                    <div style={styles.metricValue}>{report.confidence}</div>
                  </div>
                </div>

                <div>
                  <div style={styles.sectionTitle}>Summary</div>
                  <p style={styles.text}>{report.summary}</p>
                </div>

                <div>
                  <div style={styles.sectionTitle}>Top issues</div>
                  <div style={{ display: "grid", gap: 10 }}>
                    {(report.top_issues || []).map((item, idx) => (
                      <div key={idx} style={styles.issueCard}>
                        <div style={styles.issueHeader}>
                          <div style={styles.issueTitle}>
                            {idx + 1}. {item.issue}
                          </div>
                          <span style={styles.severityPill}>severity: {item.severity}</span>
                        </div>
                        {item.evidence ? (
                          <div style={styles.evidence}>
                            <div style={styles.smallLabel}>Evidence</div>
                            <div style={styles.mono}>{item.evidence}</div>
                          </div>
                        ) : null}
                        {item.fix ? (
                          <div style={styles.fix}>
                            <div style={styles.smallLabel}>Fix</div>
                            <div style={styles.text}>{item.fix}</div>
                          </div>
                        ) : null}
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <div style={styles.sectionTitle}>Sentence notes</div>
                  <div style={{ display: "grid", gap: 10 }}>
                    {(report.sentence_notes || []).map((s, idx) => (
                      <div key={idx} style={styles.sentenceCard}>
                        <div style={styles.sentenceTop}>
                          <div style={styles.sentenceIndex}>Sentence {s.sentence_index}</div>
                          <span style={styles.flagPill}>{s.flag}</span>
                        </div>
                        <div style={styles.mono}>{s.sentence}</div>
                        {s.suggestion ? <div style={styles.text}>Suggestion: {s.suggestion}</div> : null}
                      </div>
                    ))}
                  </div>
                </div>

                <div style={styles.bottomRow}>
                  <button
                    onClick={copySummary}
                    style={{ ...styles.secondaryButton, opacity: report ? 1 : 0.6 }}
                    disabled={!report}
                  >
                    Copy report summary
                  </button>
                  <p style={styles.note}>Built for writing improvement and learning.</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}

const styles = {
  main: {
    minHeight: "100vh",
    display: "grid",
    placeItems: "center",
    padding: 24,
    background: "#0b0f19"
  },
  card: {
    width: "min(980px, 100%)",
    background: "rgba(255,255,255,0.06)",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: 18,
    padding: 22,
    color: "white",
    boxShadow: "0 20px 60px rgba(0,0,0,0.35)"
  },
  headerRow: { display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 },
  h1: { margin: 0, fontSize: 26, letterSpacing: 0.2 },
  badge: {
    fontSize: 12,
    padding: "6px 10px",
    borderRadius: 999,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "rgba(255,255,255,0.08)"
  },
  sub: { marginTop: 10, marginBottom: 0, opacity: 0.8, lineHeight: 1.4 },
  label: { display: "block", fontSize: 13, opacity: 0.9, marginTop: 14, marginBottom: 8 },
  textarea: {
    width: "100%",
    minHeight: 170,
    padding: 12,
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.18)",
    outline: "none",
    resize: "vertical",
    background: "rgba(0,0,0,0.25)",
    color: "white",
    lineHeight: 1.45
  },
  controls: { display: "grid", gridTemplateColumns: "1fr 220px", gap: 12, marginTop: 10, alignItems: "end" },
  select: {
    width: "100%",
    padding: 10,
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "rgba(0,0,0,0.25)",
    color: "white",
    outline: "none"
  },
  button: {
    width: "100%",
    padding: 12,
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "white",
    color: "black",
    fontWeight: 800,
    cursor: "pointer"
  },
  error: { marginTop: 12, color: "#ffb4b4" },
  reportBox: {
    padding: 12,
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "rgba(0,0,0,0.25)"
  },
  placeholder: { margin: 0, opacity: 0.65 },
  metricsRow: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 },
  metric: {
    border: "1px solid rgba(255,255,255,0.14)",
    borderRadius: 14,
    padding: 12,
    background: "rgba(255,255,255,0.06)"
  },
  metricLabel: { fontSize: 12, opacity: 0.75 },
  metricValue: { fontSize: 18, fontWeight: 800, marginTop: 6 },
  sectionTitle: { fontSize: 14, fontWeight: 800, marginBottom: 8 },
  text: { margin: 0, lineHeight: 1.45, opacity: 0.95 },
  issueCard: {
    border: "1px solid rgba(255,255,255,0.14)",
    borderRadius: 14,
    padding: 12,
    background: "rgba(255,255,255,0.04)"
  },
  issueHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", gap: 10 },
  issueTitle: { fontWeight: 800 },
  severityPill: {
    fontSize: 12,
    padding: "4px 8px",
    borderRadius: 999,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "rgba(255,255,255,0.08)",
    whiteSpace: "nowrap"
  },
  evidence: { marginTop: 10 },
  fix: { marginTop: 10 },
  smallLabel: { fontSize: 12, opacity: 0.75, marginBottom: 4 },
  mono: {
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
    fontSize: 13,
    lineHeight: 1.45,
    opacity: 0.95,
    whiteSpace: "pre-wrap"
  },
  sentenceCard: {
    border: "1px solid rgba(255,255,255,0.14)",
    borderRadius: 14,
    padding: 12,
    background: "rgba(255,255,255,0.03)"
  },
  sentenceTop: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  sentenceIndex: { fontWeight: 800, opacity: 0.9 },
  flagPill: {
    fontSize: 12,
    padding: "4px 8px",
    borderRadius: 999,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "rgba(255,255,255,0.08)",
    whiteSpace: "nowrap"
  },
  bottomRow: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginTop: 6 },
  secondaryButton: {
    padding: "10px 12px",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "rgba(255,255,255,0.08)",
    color: "white",
    cursor: "pointer",
    whiteSpace: "nowrap"
  },
  note: { margin: 0, opacity: 0.75, fontSize: 12 }
};

"use client";

import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [form, setForm] = useState({
    carbs_g: 0,
    fiber_g: 0,
    protein_g: 0,
    fat_g: 0
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function predict() {
    setLoading(true);
    setResult(null);

    const res = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  }

  return (
    <main style={{ padding: 32, maxWidth: 900, margin: "0 auto" }}>
      <h1>Glucose Impact Analyzer AI</h1>
      <p>Educational glucose impact prediction based on meal macros.</p>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
        {Object.entries(form).map(([key, value]) => (
          <input
            key={key}
            type="number"
            placeholder={key.replace("_g", " (g)")}
            value={value}
            onChange={(e) => setForm({ ...form, [key]: Number(e.target.value) })}
            style={{
              padding: 10,
              borderRadius: 8,
              border: "1px solid #ccc"
            }}
          />
        ))}
      </section>

      <button
        onClick={predict}
        disabled={loading}
        style={{
          marginTop: 20,
          padding: "12px 20px",
          borderRadius: 10,
          border: "none",
          background: "black",
          color: "white",
          fontSize: 16
        }}
      >
        {loading ? "Analyzing..." : "Analyze Glucose Impact"}
      </button>

      {result && (
        <>
          <section style={{ marginTop: 40 }}>
            <h2>Impact Score</h2>
            <div style={{ fontSize: 48, fontWeight: 600 }}>
              {Math.round(result.impact_score)}/100
            </div>
            <p>Estimated peak glucose rise: +{Math.round(result.peak_mgdl_delta)} mg/dL</p>
          </section>

          <section style={{ height: 300, marginTop: 40 }}>
            <h2>Predicted Glucose Curve (2h)</h2>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={result.curve_minutes.map((m: number, i: number) => ({
                  minute: m,
                  delta: result.curve_mgdl_delta[i]
                }))}
              >
                <XAxis dataKey="minute" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="delta" stroke="#000" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </section>

          <section style={{ marginTop: 30 }}>
            <h3>Explanation</h3>
            <pre style={{ background: "#f5f5f5", padding: 16, borderRadius: 10 }}>
              {JSON.stringify(result.explanation, null, 2)}
            </pre>
          </section>
        </>
      )}
    </main>
  );
}

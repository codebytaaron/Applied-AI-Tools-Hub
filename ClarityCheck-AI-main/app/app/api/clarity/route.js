export const runtime = "nodejs";

function audienceInstruction(audience) {
  switch (audience) {
    case "middle_school":
      return "Assume the reader is in middle school. Favor simple wording and obvious context.";
    case "high_school":
      return "Assume the reader is a high school student. Keep feedback practical and clear.";
    case "professional":
      return "Assume the reader is a professional audience. Focus on clarity, structure, and precision.";
    case "general":
    default:
      return "Assume the reader is the general public. Avoid jargon and ambiguity.";
  }
}

function safeJsonParse(s) {
  try {
    return JSON.parse(s);
  } catch {
    return null;
  }
}

export async function POST(req) {
  try {
    const { text, audience = "high_school" } = await req.json();

    if (!text || typeof text !== "string" || text.trim().length < 10) {
      return Response.json({ error: "Please provide at least 10 characters of text." }, { status: 400 });
    }

    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      return Response.json({ error: "Missing OPENAI_API_KEY in .env.local" }, { status: 500 });
    }

    const model = process.env.OPENAI_MODEL || "gpt-4o-mini";

    const system =
      "You are ClarityCheck AI, a writing clarity analyzer. " +
      "You must produce STRICT JSON ONLY, with no extra text. " +
      "Do not rewrite the full text. Provide feedback and suggestions only. " +
      "Do not add new facts about the user's content. " +
      "If you reference examples, quote short snippets from the input as evidence.";

    const schemaHint = {
      clarity_score: "number 0-100",
      reading_level_guess: "one of: 'middle school', 'high school', 'college', 'professional'",
      confidence: "one of: 'low', 'medium', 'high'",
      summary: "1-2 sentences explaining overall clarity and biggest improvement area",
      top_issues: [
        {
          issue: "short name of the problem",
          severity: "low|medium|high",
          evidence: "short quote/snippet from text (optional but preferred)",
          fix: "specific actionable fix"
        }
      ],
      sentence_notes: [
        {
          sentence_index: "number starting at 1",
          sentence: "the sentence (as in the text, or close)",
          flag: "OK|Too long|Vague|Jargon|Missing context|Unclear reference|Grammar|Run-on",
          suggestion: "one helpful suggestion (optional)"
        }
      ]
    };

    const user =
      `${audienceInstruction(audience)}\n\n` +
      "Analyze the following text for clarity and readability.\n" +
      "Return STRICT JSON in the exact structure described.\n\n" +
      "JSON structure example (types and allowed values matter):\n" +
      JSON.stringify(schemaHint, null, 2) +
      "\n\nText:\n" +
      text;

    const resp = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content: user }
        ],
        temperature: 0.2
      })
    });

    const data = await resp.json();
    if (!resp.ok) {
      const msg = data?.error?.message || "OpenAI request failed";
      return Response.json({ error: msg }, { status: 500 });
    }

    const content = data?.choices?.[0]?.message?.content?.trim() || "";
    const parsed = safeJsonParse(content);

    if (!parsed) {
      return Response.json(
        {
          error: "Model returned non-JSON output. Try again.",
          raw: content.slice(0, 2000)
        },
        { status: 500 }
      );
    }

    // Minimal validation and normalization
    const score = Number(parsed.clarity_score);
    parsed.clarity_score = Number.isFinite(score) ? Math.max(0, Math.min(100, score)) : 0;

    if (!Array.isArray(parsed.top_issues)) parsed.top_issues = [];
    if (!Array.isArray(parsed.sentence_notes)) parsed.sentence_notes = [];

    return Response.json(parsed);
  } catch (e) {
    return Response.json({ error: e?.message || "Server error" }, { status: 500 });
  }
}

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import httpx

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


@dataclass
class GradeRequest:
    assignment_type: str
    grade_level: str
    rubric: str
    student_work: str
    strictness: str = "medium"  # easy | medium | hard


def _strictness_instructions(level: str) -> str:
    level = (level or "medium").lower().strip()
    if level == "easy":
        return (
            "Be supportive but still honest. Assume minor mistakes are common. "
            "Do not over-penalize small grammar issues unless they hurt clarity."
        )
    if level == "hard":
        return (
            "Be strict and direct. Penalize weak evidence, vague claims, sloppy structure, "
            "and unclear writing. Point out missing requirements explicitly."
        )
    return (
        "Be balanced and honest. Reward clarity and strong evidence. "
        "Penalize confusion, missing rubric items, and weak reasoning."
    )


def _system_prompt() -> str:
    return (
        "You are Honest Grader AI, a fair but direct schoolwork grader. "
        "You follow the rubric exactly, give scores with reasons, and provide actionable fixes. "
        "You never invent sources or claim you verified facts online. "
        "If the rubric is unclear, you make reasonable assumptions and state them."
    )


def _user_prompt(req: GradeRequest) -> str:
    return f"""
ASSIGNMENT TYPE: {req.assignment_type}
GRADE LEVEL: {req.grade_level}
STRICTNESS MODE: {req.strictness}

RUBRIC (authoritative):
{req.rubric}

STUDENT WORK TO GRADE:
{req.student_work}

Return your output as VALID JSON only (no extra text), matching this schema:

{{
  "assumptions": ["..."],
  "rubric_breakdown": [
    {{
      "criterion": "string",
      "score": number,
      "max_score": number,
      "why": "string",
      "how_to_improve": ["string", "string"]
    }}
  ],
  "overall_score": number,
  "overall_max": number,
  "letter_grade": "string",
  "strengths": ["string", "string"],
  "top_fixes": ["string", "string", "string"],
  "rewrite_suggestions": [
    {{
      "original_excerpt": "string",
      "improved_version": "string",
      "reason": "string"
    }}
  ],
  "final_comment": "string"
}}

Rules:
- If rubric does not list max scores, assume each criterion is out of 10.
- Use short, specific “why” explanations tied to the student work.
- If something is missing, say exactly what is missing.
- Rewrite suggestions must use excerpts from the student work.
""".strip()


def _default_letter_grade(pct: float) -> str:
    if pct >= 97:
        return "A+"
    if pct >= 93:
        return "A"
    if pct >= 90:
        return "A-"
    if pct >= 87:
        return "B+"
    if pct >= 83:
        return "B"
    if pct >= 80:
        return "B-"
    if pct >= 77:
        return "C+"
    if pct >= 73:
        return "C"
    if pct >= 70:
        return "C-"
    if pct >= 67:
        return "D+"
    if pct >= 63:
        return "D"
    if pct >= 60:
        return "D-"
    return "F"


async def _call_ollama(system: str, user: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,
        },
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{OLLAMA_HOST}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"]


def _safe_json_parse(text: str) -> Dict[str, Any]:
    """
    Attempts to parse JSON even if the model wrapped it in code fences.
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        # try to remove leading language tag
        lines = cleaned.splitlines()
        if lines and lines[0].lower().strip() in {"json", "javascript"}:
            cleaned = "\n".join(lines[1:])
    cleaned = cleaned.strip()
    return json.loads(cleaned)


def _postprocess(result: Dict[str, Any]) -> Dict[str, Any]:
    # Ensure numbers exist and compute letter grade if missing
    overall = result.get("overall_score", None)
    overall_max = result.get("overall_max", None)

    if overall is None or overall_max is None:
        # try to compute from rubric_breakdown
        total = 0.0
        total_max = 0.0
        for item in result.get("rubric_breakdown", []):
            try:
                total += float(item.get("score", 0))
                total_max += float(item.get("max_score", 10))
            except Exception:
                pass
        overall = overall if overall is not None else total
        overall_max = overall_max if overall_max is not None else total_max
        result["overall_score"] = overall
        result["overall_max"] = overall_max

    try:
        pct = (float(overall) / float(overall_max)) * 100 if float(overall_max) > 0 else 0.0
    except Exception:
        pct = 0.0

    if not result.get("letter_grade"):
        result["letter_grade"] = _default_letter_grade(pct)

    result["percent"] = round(pct, 1)
    return result


async def grade_work(req: GradeRequest) -> Dict[str, Any]:
    system = _system_prompt() + " " + _strictness_instructions(req.strictness)
    user = _user_prompt(req)

    raw = await _call_ollama(system=system, user=user)

    try:
        parsed = _safe_json_parse(raw)
    except Exception:
        # fallback: return something helpful instead of crashing
        parsed = {
            "assumptions": [
                "The model response was not valid JSON.",
                "Grading could not be parsed, so only the raw output is shown.",
            ],
            "rubric_breakdown": [],
            "overall_score": 0,
            "overall_max": 0,
            "letter_grade": "N/A",
            "strengths": [],
            "top_fixes": [],
            "rewrite_suggestions": [],
            "final_comment": raw.strip(),
        }

    return _postprocess(parsed)

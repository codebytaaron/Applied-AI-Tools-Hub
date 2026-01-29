import os
import json
import requests
from typing import List

from .utils import normalize_hashtag, dedupe_keep_order, extract_existing_hashtags

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

def _ollama_generate(prompt: str) -> str:
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.4},
        },
        timeout=45,
    )
    r.raise_for_status()
    return r.json().get("response", "")

def generate_hashtags_ai(
    platform: str,
    caption: str,
    context: str,
    niche: str,
    hashtag_count: int,
    include_branded: bool,
    brand_tag: str,
) -> List[str]:
    existing = extract_existing_hashtags(caption)
    brand_norm = normalize_hashtag(brand_tag) if brand_tag else ""

    system_rules = (
        "You are a social media hashtag generator.\n"
        "Return ONLY valid JSON with this schema:\n"
        '{ "hashtags": ["#tag1","#tag2", "..."] }\n'
        "Rules:\n"
        "- hashtags must start with #\n"
        "- lowercase only\n"
        "- no spaces, no punctuation\n"
        "- mix: broad + niche + intent-based\n"
        "- avoid banned/unsafe content\n"
        "- do not include duplicates\n"
    )

    platform_hint = {
        "instagram": "Instagram: include a mix of broad and niche discovery tags.",
        "tiktok": "TikTok: include trend-style tags plus niche tags. Keep it punchy.",
        "youtube": "YouTube: include searchable topic tags and creator niche tags.",
        "x": "X: use fewer, sharper tags, focus on topic and community tags.",
        "linkedin": "LinkedIn: professional tags, industry keywords, avoid spammy tags.",
    }.get(platform, "General: balanced tags.")

    prompt = f"""
{system_rules}

Platform: {platform}
Platform guidance: {platform_hint}

Caption:
{caption}

Extra context (optional):
{context}

Niche (optional):
{niche}

Already used hashtags (optional):
{existing}

Target hashtag count: {hashtag_count}

If include_branded is true and brand_tag is provided, include it once.
"""

    raw = _ollama_generate(prompt).strip()

    # Parse JSON safely
    try:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("No JSON object found.")
        obj = json.loads(raw[start : end + 1])
        tags = obj.get("hashtags", [])
        if not isinstance(tags, list):
            raise ValueError("hashtags is not a list")
    except Exception as e:
        raise RuntimeError(f"Model output not valid JSON: {e}")

    cleaned = [normalize_hashtag(t) for t in tags]
    cleaned = [t for t in cleaned if t]

    if include_branded and brand_norm:
        cleaned = [brand_norm] + cleaned

    # Keep existing tags if they are good, but do not exceed count
    merged = dedupe_keep_order(existing + cleaned)

    # Trim to requested count
    return merged[:hashtag_count]

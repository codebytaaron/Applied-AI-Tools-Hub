import re
from typing import List
from .utils import normalize_hashtag, dedupe_keep_order, extract_existing_hashtags

PLATFORM_BASE = {
    "instagram": ["#instagood", "#photooftheday", "#explorepage", "#contentcreator", "#reels"],
    "tiktok": ["#fyp", "#foryou", "#viral", "#tiktokcreator", "#trend"],
    "youtube": ["#shorts", "#youtube", "#content", "#creator", "#subscribe"],
    "x": ["#news", "#update", "#discussion"],
    "linkedin": ["#leadership", "#business", "#career", "#growth", "#branding"],
}

TOPIC_MAP = {
    "fitness": ["#fitness", "#workout", "#gym", "#training", "#health"],
    "sports": ["#sports", "#athlete", "#training", "#highlights", "#game"],
    "tech": ["#tech", "#ai", "#software", "#startup", "#buildinpublic"],
    "finance": ["#finance", "#investing", "#money", "#business", "#wealth"],
    "travel": ["#travel", "#wanderlust", "#adventure", "#explore", "#trip"],
    "food": ["#food", "#foodie", "#cooking", "#recipe", "#yum"],
    "music": ["#music", "#artist", "#newmusic", "#producer", "#playlist"],
}

def _keywords(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    words = [w for w in text.split() if len(w) >= 4]
    # light stop words
    stop = {"this","that","with","have","just","like","from","your","what","when","then","than","into","they","them","there"}
    words = [w for w in words if w not in stop]
    return words[:25]

def generate_hashtags_rules(
    platform: str,
    caption: str,
    context: str,
    niche: str,
    hashtag_count: int,
    include_branded: bool,
    brand_tag: str,
) -> List[str]:
    existing = extract_existing_hashtags(caption)
    base = PLATFORM_BASE.get(platform, ["#content", "#creator", "#post"])

    pool = []
    pool.extend(base)

    # infer topic from niche/context keywords
    joined = f"{caption} {context} {niche}".lower()
    for topic, tags in TOPIC_MAP.items():
        if topic in joined:
            pool.extend(tags)

    # build custom tags from keywords
    words = _keywords(joined)
    for w in words:
        if w.isdigit():
            continue
        # make short keyword tags
        if len(w) <= 14:
            pool.append("#" + w)

    # optional brand
    if include_branded and brand_tag:
        pool.insert(0, normalize_hashtag(brand_tag))

    merged = dedupe_keep_order(existing + [normalize_hashtag(t) for t in pool])
    merged = [t for t in merged if t]

    return merged[:hashtag_count]

import re
from typing import List

def normalize_hashtag(tag: str) -> str:
    tag = tag.strip()
    tag = re.sub(r"^#+", "", tag)          # remove leading ###
    tag = re.sub(r"[^\w]+", "", tag)       # keep letters/numbers/underscore
    if not tag:
        return ""
    return "#" + tag.lower()

def dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def extract_existing_hashtags(text: str) -> List[str]:
    return [normalize_hashtag(t) for t in re.findall(r"#\w+", text)]

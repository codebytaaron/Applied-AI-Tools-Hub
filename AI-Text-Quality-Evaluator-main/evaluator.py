import re

def evaluate_text(text: str):
    words = re.findall(r"\w+", text)
    sentences = re.split(r"[.!?]+", text)

    word_count = len(words)
    sentence_count = max(1, len([s for s in sentences if s.strip()]))

    avg_sentence_length = round(word_count / sentence_count, 1)

    clarity = "High" if avg_sentence_length < 20 else "Medium" if avg_sentence_length < 30 else "Low"

    tone = "Neutral"
    if any(w in text.lower() for w in ["great", "excellent", "amazing"]):
        tone = "Positive"
    elif any(w in text.lower() for w in ["bad", "terrible", "awful"]):
        tone = "Negative"

    score = min(100, max(40, 100 - (avg_sentence_length * 2)))

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_sentence_length": avg_sentence_length,
        "clarity": clarity,
        "tone": tone,
        "overall_score": score,
        "feedback": [
            "Shorten long sentences for better clarity." if clarity != "High" else "Sentence length is well balanced.",
            "Tone is clear and consistent."
        ]
    }

from typing import Dict, Any

__all__ = ["analyze_input"]

import re

# Simple keyword maps for reflection
INTENT_KEYWORDS = {
    "reflect": ["feel", "been thinking", "wonder", "keep", "always", "never", "don’t know"],
    "vent": ["tired", "sick of", "can’t take", "frustrated", "annoyed", "angry"],
    "ask": ["how do", "what should", "can you", "do you know"],
    "celebrate": ["proud", "happy", "excited", "finally", "accomplished"]
}

EMOTION_TAGS = {
    "self-doubt": ["not enough", "never finish", "doubt", "useless", "insecure"],
    "frustration": ["can’t", "tired", "stuck", "again", "fail"],
    "loneliness": ["alone", "isolated", "no one", "distant", "ignored"],
    "hope": ["better", "improve", "hope", "starting to", "maybe"],
    "longing": ["miss", "used to", "want to", "wish", "could have"]
}

def analyze_input(text: str) -> Dict[str, Any]:
    lowered = text.lower()

    # Detect intent
    intent_scores = {intent: 0 for intent in INTENT_KEYWORDS}
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in lowered:
                intent_scores[intent] += 1

    # Choose highest scoring intent
    best_intent = max(intent_scores, key=intent_scores.get)
    intent_confidence = intent_scores[best_intent] / (len(INTENT_KEYWORDS[best_intent]) or 1)

    # Detect emotion
    emotion_scores = {tag: 0 for tag in EMOTION_TAGS}
    for tag, keywords in EMOTION_TAGS.items():
        for kw in keywords:
            if kw in lowered:
                emotion_scores[tag] += 1

    best_emotion = max(emotion_scores, key=emotion_scores.get)
    if emotion_scores[best_emotion] == 0:
        best_emotion = "unclassified"

    return {
        "text": text.strip(),
        "intent": best_intent,
        "confidence": round(intent_confidence, 2),
        "emotion_tag": best_emotion
    }

# Example usage:
if __name__ == "__main__":
    result = analyze_input("I feel like I never finish anything I start.")
    print(result)

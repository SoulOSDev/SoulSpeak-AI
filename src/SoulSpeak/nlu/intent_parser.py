import re

INTENT_KEYWORDS = {
    "new_entry": ["write", "journal", "remember", "log entry", "record"],
    "view_memories": ["view", "entries", "see", "past memories", "recent memories", "show memories", "show me my memories"],
    "check_trend": ["trend", "pattern", "patterns", "emotion", "emotional", "feeling", "feelings", "update"],
    "summarize_archive": ["summarize", "summary of past logs", "summary", "archive summary", "summary of archive", "summarize logs", "summarize my archive"],
    "archive": ["archive memories", "store older", "compress", "move older", "store everything", "store", "archive"],
    "exit": ["exit", "quit", "leave", "goodbye", "bye"]
}

def get_intent(text: str) -> str:
    text = text.lower()

    # Check for full phrases first
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return intent

    # Fallback to word boundary matching
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', text):
                return intent

    return "unknown"
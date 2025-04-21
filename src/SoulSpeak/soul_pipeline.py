import os
import sys

# Add the parent folder of 'memory_journal' to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from memory_journal.check_emotional_themes import (
    load_memories,
    summarize_recent_emotions,
    generate_theme_summary,
    compare_emotional_trends,
    should_generate_trend_summary,
    update_last_trend_check
)

from memory_journal.memory_store import build_memory, save_memory
from memory_journal.preprocess import preprocess
from memory_journal.emotion_classifier import classify_emotions_mistral, classify_sentiment_mistral
from memory_journal.soul_reflect import generate_reflection
from memory_journal.memory_store import is_duplicate_memory

def soul_speak_pipeline(user_input: str) -> dict:
    """
    Complete SoulSpeak emotional pipeline:
    - Cleans input
    - Tags emotions
    - Scores sentiment
    - Builds memory
    - Returns reflection and memory
    """
    # Step 1: Preprocess
    cleaned = preprocess(user_input)

    # Step 2: Classify Emotions
    emotion_tags = classify_emotions_mistral(cleaned)

    # Step 3: Sentiment Score
    sentiment_score = classify_sentiment_mistral(cleaned)

    # Step 4: Build Memory
    memory = build_memory(user_input, emotion_tags, sentiment_score)

    # Step 5: Reflect
    reflection = generate_reflection(memory)
    trend_reflection = ""

    if should_generate_trend_summary(days=3):
        memories = load_memories(include_archive=True) # Change to =False to toggle archive
        tag_summary = summarize_recent_emotions(memories, limit=10)
        trend_reflection = compare_emotional_trends(memories)
        update_last_trend_check()

    # Step 6: Save Memory
    if not is_duplicate_memory(user_input):
        save_memory(memory)
    else:
        print("Duplicate entry detected. Memory not saved.")

    full_reflection = reflection
    if trend_reflection:
        full_reflection += "\n\n" + trend_reflection
    
    return {
        "reflection": full_reflection,
        "memory": memory
    }

# 🧪 Optional test
if __name__ == "__main__":
    test_input = "Lately, I've been feeling more like myself again."
    result = soul_speak_pipeline(test_input)

    print("\nSoulSpeak says:\n", result["reflection"])
    print("\nMemory stored:\n", result["memory"])
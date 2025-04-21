import os
import time
from SoulSpeak.memory_journal.soul_reflect import generate_reflection
from SoulSpeak.memory_journal.memory_store import (
    build_memory,
    save_memory,
    load_memories,
    is_duplicate_memory,
    archive_old_memories
)
from SoulSpeak.memory_journal.check_emotional_themes import (
    summarize_recent_emotions,
    generate_theme_summary,
    compare_emotional_trends,
    should_generate_trend_summary,
    update_last_trend_check
)
from SoulSpeak.memory_journal.summarize_archive import generate_archive_summary
from SoulSpeak.memory_journal.preprocess import preprocess
from SoulSpeak.memory_journal.emotion_classifier import (
    classify_emotions_mistral,
    classify_sentiment_mistral
)

def pause():
    input("\nPress Enter to continue...")

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def journal_entry():
    clear()
    print("New Journal Entry\n")
    user_input = input("What’s on your mind today?\n\n> ").strip()
    if not user_input:
        print("Entry was empty. Returning to menu.")
        return

    if is_duplicate_memory(user_input):
        print("This seems identical to your last entry. Not saved.")
        return

    cleaned = preprocess(user_input)
    tags = classify_emotions_mistral(cleaned)
    sentiment = classify_sentiment_mistral(cleaned)
    memory = build_memory(user_input, tags, sentiment)
    reflection = generate_reflection(memory)

    if should_generate_trend_summary(days=3):
        trend = compare_emotional_trends(load_memories(include_archive=True))
        reflection += "\n\n" + trend
        update_last_trend_check()

    save_memory(memory)
    print("\nSoulSpeak says:\n")
    print(reflection)
    pause()

def view_recent_memories():
    clear()
    print("Recent Memories\n")
    memories = load_memories()
    for mem in memories[-5:]:
        print(f"{mem['timestamp']} - {', '.join(mem['tags'])}")
        print(f"{mem['text']}\n")
    pause()

def check_trends():
    clear()
    print("Emotional Trend Check\n")
    memories = load_memories(include_archive=True)
    tags = summarize_recent_emotions(memories)
    summary = generate_theme_summary(tags)
    trend = compare_emotional_trends(memories)

    print("Theme Summary:\n", summary)
    print("\nTrend Reflection:\n", trend)
    pause()

def summarize_old_memories():
    clear()
    print("Summarize Old Memories\n")
    choice = input("Summarize from (archive / active / all)? ").strip().lower()
    prompt = generate_archive_summary(source=choice)
    if "nothing" in prompt.lower():
        print(prompt)
    else:
        print("\nSoulSpeak Reflects:\n")
        import requests
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        print(response.json()["response"].strip())
    pause()

def archive_old():
    clear()
    print("Archiving old memories (30+ days)...\n")
    archive_old_memories()
    pause()

def main():
    clear()
    print("\nSoulSpeak is listening...")
    print("(Type your thoughts below. Use /memories, /trend, /archive, or /exit.)\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Commands
        if user_input.lower() == "/exit":
            print("\nSoulSpeak: Until next time.\n")
            break

        if user_input.lower() == "/memories":
            view_recent_memories()
            continue

        if user_input.lower() == "/trend":
            check_trends()
            continue

        if user_input.lower() == "/archive":
            archive_old()
            continue

        # Process reflection
        if is_duplicate_memory(user_input):
            print("SoulSpeak: You've already shared something very similar.")
            continue

        cleaned = preprocess(user_input)
        tags = classify_emotions_mistral(cleaned)
        sentiment = classify_sentiment_mistral(cleaned)
        memory = build_memory(user_input, tags, sentiment)
        save_memory(memory)

        reflection = generate_reflection(memory)

        if should_generate_trend_summary(days=3):
            trend = compare_emotional_trends(load_memories(include_archive=True))
            reflection += "\n\n" + trend
            update_last_trend_check()

        print(f"\nSoulSpeak: {reflection}\n")
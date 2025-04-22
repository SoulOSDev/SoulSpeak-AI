import os
from src.SoulSpeak.nlu.intent_parser import get_intent
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

def main():
    print("Welcome to SoulSpeak CLI")
    print("You can speak naturally. To exit, just say something like 'exit' or 'bye'.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        intent = get_intent(user_input)

        if intent == "new_entry":
            raw_text = input("\nWhat would you like to reflect on?\n> ")
            preprocessed = preprocess(raw_text)
            emotions = classify_emotions_mistral(preprocessed)
            sentiment = classify_sentiment_mistral(preprocessed)
            memory = build_memory(preprocessed, emotions, sentiment)
            if is_duplicate_memory(memory):
                print("This memory has already been saved.")
            else:
                save_memory(memory)
                print("Memory saved successfully.")

        elif intent == "view_memories":
            memories = load_memories()
            for m in memories[-5:]:
                print(f"- {m['text']}")

        elif intent == "check_trend":
            if should_generate_trend_summary():
                trend_summary = generate_theme_summary()
                update_last_trend_check()
                print("\nRecent Emotional Trends:\n", trend_summary)
            else:
                print("Not enough new entries to generate a trend summary.")

        elif intent == "summarize_archive":
            print("\nArchive Summary:")
            print(generate_archive_summary())

        elif intent == "archive":
            archive_old_memories()
            print("Older memories have been archived.")

        elif intent == "exit":
            print("Goodbye. Your memories are safe.")
            break

        else:
            print("I didn't understand that. Try rephrasing your request.")

        pause()

if __name__ == "__main__":
    main()


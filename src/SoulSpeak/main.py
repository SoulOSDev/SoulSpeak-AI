# pyright: reportUndefinedVariable=false

from brain import Brain
import random

OPENING_MESSAGES = [
    "I'm here. What's on your mind?",
    "You're not alone. Just say something and I'll listen",
    "I'm ready when you are.",
    "Hey... Talk to me",
    "Another day, another chance to understand. I'm Listening.",
    "Take your time. I'm with you.",
    "Whenever you're ready, go ahead and say something."
]

def main():
    print(f"\nWelcome back, {USERNAME}. I’ll keep things {TONE} today.\n")

    while True:
        user_input = input(f"{USERNAME}: ").strip()
        if not user_input:
            continue

        if user_input.lower() in {"exit", "bye", "quit"}:
            print("Goodbye. Your memories are safe.")
            break

        preprocessed = preprocess(user_input)
        emotions = classify_emotions_mistral(preprocessed)
        sentiment = classify_sentiment_mistral(preprocessed)
        memory = build_memory(preprocessed, emotions, sentiment)

        if is_duplicate_memory(memory):
            print("SoulSpeak: I remember you saying something like this before.")
        else:
            save_memory(memory)

        response = generate_reflection(memory)
        print(f"SoulSpeak: {response}")

if __name__ == "__main__":
    main()
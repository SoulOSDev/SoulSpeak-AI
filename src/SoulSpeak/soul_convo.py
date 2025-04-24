import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import time

from SoulSpeak.memory_journal.soul_reflect import generate_reflection
from SoulSpeak.memory_journal.memory_store import (
    build_memory,
    save_memory,
    is_duplicate_memory
)

from SoulSpeak.memory_journal.preprocess import preprocess
from SoulSpeak.memory_journal.emotion_classifier import (
    classify_emotions_mistral,
    classify_sentiment_mistral
)

CONFIG_PATH = "SoulSpeak/data/user_config.json"

def get_or_create_user_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    else:
        print("\n Let's get to know each other.")
        name = input("What should I call you?")
        tone = input("Which tone fits me best for you? (warm / stoic / etc.)")
        config = {"username": name, "tone_profile": tone}

        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)

        print(f"\nNice to meet you, {name}. I'll remember that.")
        return config
    
user_config = get_or_create_user_config()
USERNAME = user_config["username"]
TONE = user_config["tone_profile"]

def pause():
    input("\nPress Enter to continue...")

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


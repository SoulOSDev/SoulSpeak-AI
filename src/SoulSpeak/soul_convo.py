import sys
import os
import time
import requests
sys.path.append(os.path.abspath("src"))

CONVO_LOG_PATH = "src/SoulSpeak/conversation_log.txt"

def log_conversation(speaker, message):
    with open(CONVO_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{speaker}: {message}\n")

# Memory paths for SoulSpeak A
MEMORY_A_PATH = "src/SoulSpeak/memory_journal/memory_a/memory_log.json"
ARCHIVE_A_PATH = "src/SoulSpeak/memory_journal/memory_a/archive_log.json"

# Memory paths for SoulSpeak B
MEMORY_B_PATH = "src/SoulSpeak/memory_journal/memory_b/memory_log.json"
ARCHIVE_B_PATH = "src/SoulSpeak/memory_journal/memory_b/archive_log.json"

import time
from SoulSpeak.memory_journal.preprocess import preprocess
from SoulSpeak.memory_journal.memory_store import (
    build_memory,
    save_memory,
    load_memories,
    is_duplicate_memory
)
from SoulSpeak.memory_journal.emotion_classifier import (
    classify_emotions_mistral,
    classify_sentiment_mistral
)
from SoulSpeak.memory_journal.soul_reflect import generate_reflection

def soul_speak_instance(input_text, memory_path):
    cleaned = preprocess(input_text)
    tags = classify_emotions_mistral(cleaned)
    sentiment = classify_sentiment_mistral(cleaned)

    if is_duplicate_memory(input_text, memory_path):
        print("[Duplicate] Message already exists in memory.")
        return None

    memory = build_memory(input_text, tags, sentiment)
    save_memory(memory, memory_path)

    reflection = generate_reflection(memory)
    return reflection


# New: Generate random thought to begin conversation
def generate_initial_thought():
    prompt = """
Create a natural, introspective statement someone might say at the start of a quiet, personal conversation. Keep it short and emotionally sincere. Do not ask questions. Limit to 1-2 sentences.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()


# Conversation starts here
if __name__ == "__main__":
    print("SoulSpeak A and B are beginning their conversation...\n")

    message = generate_initial_thought()
    print(f"SoulSpeak A: {message}")
    log_conversation("SoulSpeak A", message)

    speaker = "B"
    for _ in range(10):
        if speaker == "B":
            response = soul_speak_instance(message, MEMORY_B_PATH)
            if response:
                print(f"SoulSpeak B: {response}")
                log_conversation("SoulSpeak B", response)
                message = response
                speaker = "A"
        else:
            response = soul_speak_instance(message, MEMORY_A_PATH)
            if response:
                print(f"SoulSpeak A: {response}")
                log_conversation("SoulSpeak A", response)
                message = response
                speaker = "B"


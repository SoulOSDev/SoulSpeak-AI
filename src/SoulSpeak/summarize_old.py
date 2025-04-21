from memory_journal.summarize_archive import generate_archive_summary
import requests

# 🔄 Choose: "archive", "active", or "all"
SOURCE_MODE = "all"

prompt = generate_archive_summary(source=SOURCE_MODE)

if "nothing" in prompt.lower():
    print(prompt)
else:
    print(f"\n🧠 SoulSpeak summary based on: {SOURCE_MODE.upper()}")
    print(prompt)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    print("\n💬 SoulSpeak reflects:")
    print(response.json()["response"].strip())
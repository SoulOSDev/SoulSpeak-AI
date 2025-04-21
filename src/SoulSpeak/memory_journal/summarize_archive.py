import json
from SoulSpeak.memory_journal.check_emotional_themes import load_memories, summarize_recent_emotions
from SoulSpeak.memory_journal.soul_reflect import generate_reflection_prompt
from datetime import datetime

def generate_archive_summary(source="archive", limit=25) -> str:
    """
    Generate a reflective summary from stored memories.
    - source: "archive", "active", or "all"
    """
    if source == "archive":
        memories = load_memories(file_path="data/archive_log.json")
    elif source == "active":
        memories = load_memories(file_path="data/memory_log.json")
    elif source == "all":
        archive = load_memories(file_path="data/archive_log.json")
        active = load_memories(file_path="data/memory_log.json")
        memories = archive + active
    else:
        return "Invalid source provided."

    if not memories:
        return "There’s nothing in the selected memory source to reflect on."

    recent = memories[-limit:]
    combined_text = "\n".join([f"- {m['text']}" for m in recent])
    tags = [tag for m in recent for tag in m.get("tags", [])]

    pseudo_memory = {
        "text": f"In reviewing these past moments:\n{combined_text}",
        "tags": tags,
        "sentiment": round(sum(m.get("sentiment", 0) for m in recent) / len(recent), 2)
    }

    return generate_reflection_prompt(pseudo_memory)
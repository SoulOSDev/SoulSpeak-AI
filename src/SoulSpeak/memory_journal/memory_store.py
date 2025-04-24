from datetime import datetime
from typing import List
from SoulSpeak.memory_journal.check_emotional_themes import load_memories
from datetime import datetime, timedelta

def archive_old_memories(days_old=30,
                          active_path="data/memory_log.json",
                          archive_path="data/archive_log.json"):

    active = load_memories(active_path)
    if not active:
        return

    cutoff = datetime.now() - timedelta(days=days_old)
    keep = []
    archive = []

    for mem in active:
        try:
            timestamp = datetime.fromisoformat(mem["timestamp"])
            if timestamp < cutoff:
                archive.append(mem)
            else:
                keep.append(mem)
        except Exception:
            keep.append(mem)  # Keep malformed entries

    if archive:
        # Append to archive log
        existing_archive = load_memories(archive_path)
        combined = existing_archive + archive
        with open(archive_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2)

        # Rewrite memory log with kept entries
        with open(active_path, "w", encoding="utf-8") as f:
            json.dump(keep, f, indent=2)

        print(f"Archived {len(archive)} old memories.")
    else:
        print("No memories needed archiving.")

# Optional: You might want to adjust weight differently later
def calculate_weight(score, tags):
    """
    Calculates memory importance weight.
    Emotional intensity + tag-based importance.
    """
    emotional_intensity = abs(score)
    base_weight = 1.0
    special_tags = ["fragmented", "fulfilled", "grieving", "whole"]
    for tag in tags:
        if tag in special_tags:
            base_weight = 1.5
            break
    return round(emotional_intensity * base_weight, 2)

from datetime import datetime, timezone

def build_memory(text, tags, sentiment):
    """
    Creates a memory object ready for storage or reflection.
    """
    return {
        "text": text,
        "tags": tags,
        "sentiment": sentiment,
        "weight": calculate_weight(sentiment, tags),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

import json
import os

def save_memory(memory, file_path="data/memory_log.json"):
    """
    Appends a memory entry to a JSON file.
    Creates the file if it doesn't exist.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        # Load existing memories
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        # Append new memory
        data.append(memory)

        # Save back to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"[Memory Save Error] {e}")

from datetime import datetime
import re

def search_memories(tags=None, keywords=None, since=None, file_path="data/memory_log.json") -> List[dict]:
    memories = load_memories(file_path)
    results = []

    for mem in memories:
        # Check tag match
        if tags and not any(tag in mem.get("tags", []) for tag in tags):
            continue

        # Check keyword match
        if keywords:
            text = mem.get("text", "").lower()
            if not any(re.search(rf"\b{kw.lower()}\b", text) for kw in keywords):
                continue

        # Check timestamp filter
        if since:
            try:
                mem_time = datetime.fromisoformat(mem.get("timestamp"))
                if mem_time < since:
                    continue
            except Exception:
                continue

        results.append(mem)

    return results

def is_duplicate_memory(new_memory: dict, file_path="data/memory_log.json") -> bool:
    memories = load_memories(file_path)
    if not memories:
        return False

    last = memories[-1]
    return last.get("text", "").strip() == new_memory.get("text", "").strip()
from datetime import datetime
from typing import List
from .check_emotional_themes import load_memories
from datetime import datetime, timedelta

from .memory_utils import calculate_priority
from datetime import datetime, timezone, timedelta

def archive_old_memories(days_old=30,
                          priority_threshold=0.3,
                          active_path="data/memory_log.json",
                          archive_path="data/archive_log.json"):

    active = load_memories(active_path)
    if not active:
        return

    cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)
    keep = []
    archive = []

    for mem in active:
        try:
            timestamp = datetime.fromisoformat(mem["timestamp"])
        except Exception:
            timestamp = datetime.now(timezone.utc)

        priority = calculate_priority(mem)
        age_trigger = timestamp < cutoff
        priority_trigger = priority < priority_threshold

        if age_trigger or priority_trigger:
            archive.append(mem)
        else:
            keep.append(mem)

    # Save updated memory log and archive
    with open(active_path, "w", encoding="utf-8") as f:
        json.dump(keep, f, indent=4)

    with open(archive_path, "r+", encoding="utf-8") as f:
        try:
            existing_archive = json.load(f)
        except Exception:
            existing_archive = []

        existing_archive.extend(archive)
        f.seek(0)
        json.dump(existing_archive, f, indent=4)
        f.truncate()

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

def build_memory(text, tags, sentiment, memory_type="journal"):
    """
    Creates a memory object ready for storage or reflection.
    """
    return {
        "text": text,
        "tags": tags,
        "sentiment": sentiment,
        "weight": calculate_weight(sentiment, tags),
        "type": memory_type,
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

from datetime import datetime
from .check_emotional_themes import load_memories

def calculate_priority(memory):
    """
    Returns a priority score (0.0 to 1.0) based on emotional intensity and recency.
    """
    intensity = memory.get("emotional_intensity", 0.0)
    timestamp_str = memory.get("timestamp")

    if not timestamp_str:
        return intensity  # fallback: use intensity alone

    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        days_ago = (datetime.now() - timestamp).days
        recency_weight = max(0.0, 1.0 - (days_ago / 30.0))  # score drops over 30 days
    except Exception:
        recency_weight = 0.5  # fallback

    priority_score = (0.7 * intensity) + (0.3 * recency_weight)
    return round(priority_score, 3)

def is_duplicate_memory(new_text: str, file_path="data/memory_log.json") -> bool:
    memories = load_memories(file_path)
    if not memories:
        return False

    last = memories[-1]
    return last.get("text", "").strip() == new_text.strip()
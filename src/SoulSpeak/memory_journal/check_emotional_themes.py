import json
from collections import Counter
from typing import List
from datetime import datetime, timedelta
import os

def should_generate_trend_summary(days=3, tracker_path="data/last_trend_check.json") -> bool:
    try:
        if not os.path.exists(tracker_path) :
            return True
        
        with open(tracker_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        last_checked = datetime.fromisoformat(data["last_checked"])
        return datetime.now() - last_checked >= timedelta(days=days)
    
    except Exception as e:
        print(f"[Trend Check Error] {e}")
        return True # Fail-safe: allow trend check

def update_last_trend_check(tracker_path="data/last_trend_check.json"):
    os.makedirs(os.path.dirname(tracker_path), exist_ok=True)
    with open(tracker_path, "w", encoding="utf-8") as f:
        json.dump({"last_checked": datetime.now().isoformat()}, f)

def load_memories(file_path="data/memory_log.json", include_archive=False) -> List[dict]:
    def read_json(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"[Load Error] {e}")
            return []

    memories = read_json(file_path)

    if include_archive:
        archive = read_json("data/archive_log.json")
        return memories + archive

    return memories

def summarize_recent_emotions(memories: List[dict], limit=10):
    """
    Returns a frequency summary of emotional tags from the last N memories.
    """
    recent = memories[-limit:] if len(memories) >= limit else memories
    tag_counter = Counter()

    for mem in recent:
        tags = mem.get("tags", [])
        tag_counter.update(tags)

    return tag_counter.most_common()

def generate_theme_summary(tag_counts: List[tuple]) -> str:
    """
    Converts tag frequency data into a natural language summary.
    """
    if not tag_counts:
        return "You haven’t really shared much lately. I'm looking forward to hearing more when you're ready."

    top = tag_counts[:3]  # Get top 3 emotions

    if len(top) == 1:
        emotion, count = top[0]
        return f"Lately, you’ve been mostly feeling {emotion}. It’s been a steady vibe."

    elif len(top) == 2:
        e1, e2 = top[0][0], top[1][0]
        return f"Seems like you've been swinging between feeling {e1} and {e2} lately. Totally valid."

    else:
        e1, e2, e3 = top[0][0], top[1][0], top[2][0]
        return f"From what I’ve picked up, you’ve been feeling a mix of {e1}, {e2}, and {e3}. That’s a pretty rich combo."

def compare_emotional_trends(memories: List[dict], window_size=5) -> str:
    if len(memories) < window_size * 2:
        return "You're still early in your journey — let's collect more before drawing conclusions."

    # Split into two halves
    recent = memories[-window_size:]
    previous = memories[-(window_size * 2):-window_size]

    # Count tags and sentiment
    def count_tags(mem_slice):
        tag_counter = Counter()
        total_sentiment = 0.0
        for mem in mem_slice:
            tags = mem.get("tags", [])
            sentiment = mem.get("sentiment", 0)
            tag_counter.update(tags)
            total_sentiment += sentiment
        avg_sentiment = round(total_sentiment / len(mem_slice), 2)
        return tag_counter, avg_sentiment

    recent_tags, recent_sent = count_tags(recent)
    prev_tags, prev_sent = count_tags(previous)

    # Detect emotional shift
    sentiment_change = recent_sent - prev_sent
    sentiment_trend = ""
    if sentiment_change > 0.15:
        sentiment_trend = "Your emotional tone has been lifting recently."
    elif sentiment_change < -0.15:
        sentiment_trend = "Things have felt a bit heavier than before."
    else:
        sentiment_trend = "Your emotional tone has been fairly steady."

    # Detect rising emotions
    rising = []
    for tag, count in recent_tags.items():
        if count > prev_tags.get(tag, 0):
            rising.append(tag)

    if rising:
        top_rising = rising[:3]  # limit to 3 emotional highlights
        if len(top_rising) == 1:
            rising_statement = f"You’ve been feeling more {top_rising[0]} lately."
        elif len(top_rising) == 2:
            rising_statement = f"You’ve been moving between {top_rising[0]} and {top_rising[1]} a lot lately."
        else:
            rising_statement = f"Lately, I’ve felt more {top_rising[0]}, {top_rising[1]}, and {top_rising[2]} coming through in your energy."
    else:
        rising_statement = "Your energy's been pretty steady lately."
        
    return f"{sentiment_trend} {rising_statement}"

# Test with natural reflection
if __name__ == "__main__":
        memories = load_memories()
        tag_summary = summarize_recent_emotions(memories, limit=10)
        theme_summary = generate_theme_summary(tag_summary)
        trend_summary = compare_emotional_trends(memories)

        print("\nRecent Emotional Themes:")
        for emotion, count in tag_summary:
            print(f"{emotion}: {count}x")

        print("\nSoulSpeak says:\n", theme_summary)
        print("\nSoulSpeak trend check:\n", trend_summary)
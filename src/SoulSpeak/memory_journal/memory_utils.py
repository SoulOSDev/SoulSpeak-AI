from datetime import datetime

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
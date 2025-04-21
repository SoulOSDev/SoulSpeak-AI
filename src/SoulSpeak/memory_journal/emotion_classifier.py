import requests

# Emotion tag list
emotion_tags = [
    "joyful", "grateful", "inspired", "hopeful", "radiant", "proud", "playful", "loving", "compassionate",
    "devoted", "tender", "at peace", "whole", "centered", "secure", "welcoming", "fulfilled", "excited",
    "eager", "rejuvenated", "confident", "serene", "satisfied", "empowered", "curious", "contemplative",
    "reflective", "present", "steady", "focused", "attuned", "observant", "accepting", "grounded", "aware",
    "calm", "still", "numb", "disconnected", "fragmented", "wistful", "longing", "nostalgic", "sad", "lonely",
    "ashamed", "guilty", "angry", "frustrated", "anxious", "afraid", "overwhelmed", "envious", "embarrassed",
    "jealous", "bitter", "resentful", "hollow", "insecure", "vulnerable", "lost", "powerless", "grieving"
]

# Prompt builder
def generate_emotion_prompt(text):
    return f"""
You are an emotionally intelligent AI. A user just shared this message:

\"{text}\"

From the list of emotions below, return the 1 to 3 most accurate emotional tags that describe how they feel. Use only the emotion words from this list:

{', '.join(emotion_tags)}

Respond with a comma-separated list of the selected emotion tags only.
"""

# Send to Mistral
def classify_emotions_mistral(text):
    prompt = generate_emotion_prompt(text)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"].strip()
    return [tag.strip() for tag in result.split(',') if tag.strip() in emotion_tags]

# Test (optional)
if __name__ == "__main__":
    from SoulSpeak.memory_journal.preprocess import preprocess
    test_input = "I finally feel like things are getting better."
    clean_text = preprocess(test_input)
    tags = classify_emotions_mistral(clean_text)
    print("Emotion tags:", tags)

   # Build a prompt to rate sentiment
def generate_sentiment_prompt(text):
    return f"""
Rate the overall emotional sentiment of the following message on a scale from -1.0 to +1.0:

-1.0 = very negative (pain, fear, grief)
 0.0 = neutral or unclear
+1.0 = very positive (joy, hope, love)

Message:
\"{text}\"

Respond with a single number only.
"""

# Send sentiment request to Mistral
def classify_sentiment_mistral(text):
    prompt = generate_sentiment_prompt(text)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    score_str = response.json()["response"].strip()

    try:
        return float(score_str)
    except ValueError:
        return 0.0  # fallback if something goes wrong 
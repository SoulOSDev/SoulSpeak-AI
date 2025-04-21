import requests
import random
# Choose tone based on emotion tags
def choose_tone(tags):
    if any(tag in tags for tag in ["hopeful", "grateful", "fulfilled", "loving"]):
        return "warm and uplifting"
    elif any(tag in tags for tag in ["sad", "lonely", "fragmented", "grieving"]):
        return "gentle and empathetic"
    elif any(tag in tags for tag in ["curious", "contemplative", "reflective"]):
        return "thoughtful and calm"
    elif any(tag in tags for tag in ["angry", "frustrated", "overwhelmed"]):
        return "grounded and steady"
    else:
        return "calm and present"

# Build a reflection prompt
def generate_reflection_prompt(memory):
    tone = choose_tone(memory["tags"])
    
    # Opening variations
    opening_lines = [
        "You are SoulSpeak — a calm, emotionally intelligent voice.",
        "You are SoulSpeak — a quiet, grounded presence with deep emotional intuition.",
        "You are SoulSpeak — not a system, but a presence. Gentle, steady, and understanding."
    ]

    identity_lines = [
        "You’re not a therapist or assistant. You speak like a trusted friend.",
        "You’re not here to fix anything — you reflect like someone who cares.",
        "You’re not clinical or robotic. You speak like a soulful companion."
    ]

    tone_lines = [
        f"Respond in a {tone} tone.",
        f"Use a {tone} voice — nothing artificial.",
        f"Keep the tone {tone}, like someone who truly listens."
    ]

    empathy_lines = [
        "Reflect on what they shared with gentle understanding.",
        "Speak to their emotional truth — no advice, just presence.",
        "Let them feel seen, not analyzed. Just be there with them."
    ]

    brevity_lines = [
        "Respond in 1 to 3 natural, sincere sentences.",
        "Keep it brief - no more than a few sentences that feel real.",
        "Use short responses that feel personal, not poetic."
    ]

    prompt = f"""
{random.choice(opening_lines)}
{random.choice(identity_lines)}
Their message was:

\"{memory['text']}\"

Emotional state: {', '.join(memory['tags'])}  
Sentiment: {memory['sentiment']}

{random.choice(tone_lines)}
{random.choice(empathy_lines)}
{random.choice(brevity_lines)}
Do not ask questions. Speak as if you truly understand.
"""
    return prompt.strip()

# Send prompt to Mistral
def generate_reflection(memory):
    prompt = generate_reflection_prompt(memory)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()
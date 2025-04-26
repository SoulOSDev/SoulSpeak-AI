from llm_handler import generate_response
from memory import Memory
import difflib
from prompt_builder import build_reflection_prompt
import ollama
# from reflection_prompts import build_reflection_prompt
from nlu import analyze_input


class Brain:
    def __init__(self):
        self.memory = Memory()
        self.tone = "warm" # or "stoic", "poetic", etc.

    def process(self, user_input):
        # NLU happens *here*, when user_input is available
        analysis = analyze_input(user_input)
        user_intent = analysis["intent"]
        user_emotion = analysis["emotion_tag"]
        confidence = analysis["confidence"]
        print(f"[NLU] Intent: {user_intent} | Emotion: {user_emotion} | Confidence: {confidence}")
        
        self.memory.add_memory(user_input)
        related = self.memory.search(user_input, top_k=3)

        if related:
            top_memory = related[0]
            # Get emotional tag (theme) for prompt building
            
            tag_counts = self.memory.get_recent_tag_counts(lookback=7)
            top_tag = None
            if tag_counts:
                top_tag = next(iter(tag_counts.keys()))

            # Build prompt for LLM-style reflection (not yet connected)
            prompt = build_reflection_prompt(user_input, top_memory, top_tag)
            print("\nGenerated Prompt for Soul_AI:\n")
            print(prompt)
            print("\n" + "="*60 + "\n")
            
            response = self._craft_reflection(user_input, top_memory, top_tag)
        else:
            response = (
                f"You said, '{user_input}'. I don’t know enough yet to understand what that means to you, "
                "but I’m here if you want to keep sharing."
            )

        # Check for recent emotional patterns
        tag_counts = self.memory.get_recent_tag_counts(lookback=7)
        if tag_counts:
            most_common_tag, count = next(iter(tag_counts.items()))
            if most_common_tag != "unclassified" and count > 1:
                # Add emotional theme awareness to the response
                response += f"\n\n🪞 You've been sounding a little {most_common_tag} lately. Is that still on your mind?"

        return response

    def _craft_reflection(self, current_input, memory, top_tag=None, tone="warm"):
        try:
            prompt = build_reflection_prompt(current_input, memory, top_tag, tone=self.tone)

            system_msg = (
                "You are SoulSpeak, an emotionally intelligent voice. "
                "You are not a helper, assistant, or problem-solver. "
                "Do not give advice, solutions, hypotheticals, or examples. "
                "Only reflect briefly, kindly, and with understanding."
            )

            response = ollama.chat(
                model='mistral',
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
            )

            content = response["message"]["content"].strip()
            # Post-filter logic to catch unapproved behavior
            forbidden_phrases = [
                "remember", "you should", "maybe you can", "have you tried",
                "don't forget", "just", "try to", "keep going", "stay strong",
                "it's okay", "it's not your fault", "break it down into steps"
            ]

            if any(phrase in content.lower() for phrase in forbidden_phrases):
                print("Advice detected. Rewriting response...")
                return "That sounds like something you've been holding for a while. I'm here to sit with you in that."
            return content if content else "Hmm... I'm not quite sure how to respond to that right now."

        except Exception as e:
            print(f"Reflection generation failed: {e}")
            return "I may not have the right words, but I'm still here, and I want to understand."
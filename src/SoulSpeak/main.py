from brain import Brain
import random

OPENING_MESSAGES = [
    "I'm here. What's on your mind?",
    "You're not alone. Just say something and I'll listen",
    "I'm ready when you are.",
    "Hey... Talk to me",
    "Another day, another chance to understand. I'm Listening.",
    "Take your time. I'm with you.",
    "Whenever you're ready, go ahead and say something."
]

def main():
    brain = Brain()

    print(random.choice(OPENING_MESSAGES))
    print("(Type 'exit' to end the conversation.)")

    while True:
        try:
            user_input = input("🗣️ You: ")

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("🕯️ Soul_AI: Goodbye. I'll remember this.")
                break

            response = brain.process(user_input)
            print(f"Soul_AI: {response}\n")

        except KeyboardInterrupt:
            print("\nSoul_AI: Conversation interrupted. Until next time.")
            break

if __name__ == "__main__":
    main()
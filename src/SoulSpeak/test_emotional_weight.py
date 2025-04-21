from memory import Memory

def main():
    mem = Memory()

    test_inputs = [
        "I feel like I always mess things up.",
        "I’ve been really hopeful lately.",
        "Everything feels numb and empty.",
        "I'm proud of what I did today.",
        "Why do I always push people away?"
    ]

    for text in test_inputs:
        mem.add_memory(text)

    print("\n🧠 Recent Memories with Weights:")
    for i, memory in enumerate(mem.memory[-5:], start=1):
        print(f"{i}. 📝 {memory['text']}")
        print(f"   🏋️ Weight: {memory.get('weight', 'N/A')}")
        print("")

if __name__ == "__main__":
    main()
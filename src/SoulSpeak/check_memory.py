import pickle

def load_memories(file_path='data/memory_store.pkl'):
    try:
        with open(file_path, 'rb') as f:
            memory_data = pickle.load(f)
            return memory_data
    except FileNotFoundError:
        print("❌ No memory file found.")
        return []
    except Exception as e:
        print(f"❌ Failed to load memories: {e}")
        return []

def print_memories(memories):
    if not memories:
        print("⚠️ No memories to display.")
        return

    print(f"\n🧠 Soul_AI currently remembers {len(memories)} entries:\n")

    for i, memory in enumerate(memories, 1):
        if isinstance(memory, dict):
            print(f"{i}. 📝 {memory.get('text', '[No text found]')}")
            print(f"   🕰️  Timestamp: {memory.get('timestamp', 'unknown')}")
            print(f"   🔖 Tags: {', '.join(memory.get('tags', []))}\n")
        else:
            print(f"{i}. (legacy memory)")
            print(f"   📝 {memory}\n")

if __name__ == "__main__":
    memories = load_memories()
    print_memories(memories)
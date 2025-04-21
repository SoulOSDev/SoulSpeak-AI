from memory_journal.memory_store import search_memories

print("\nShowing all stored memories...")

matches = search_memories()

if not matches:
    print("No memories stored yet.")
else:
    for mem in matches:
        print(f"{mem['timestamp']} - {mem['tags']}")
        print(f"{mem['text']}")
        print("-" * 50)
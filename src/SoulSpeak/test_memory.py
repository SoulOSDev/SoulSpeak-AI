print("🧠 Running memory test...")

# Step 1: Import the memory module
try:
    from memory import Memory
    print("✅ memory.py imported successfully.")
except Exception as e:
    print("❌ Failed to import memory.py:", e)

# Step 2: Try creating a Memory instance
try:
    print("🧠 Instantiating Memory...")
    mem = Memory()
    print("✅ Memory system initialized.")
except Exception as e:
    print("❌ Failed during Memory initialization:", e)

# Step 3: Add test memories
try:
    print("💾 Adding test memories...")
    mem.add_memory("I love stargazing on clear nights.")
    mem.add_memory("Artificial intelligence fascinates me.")
    mem.add_memory("Pizza is my favorite comfort food.")
    mem.add_memory("I once visited Tokyo and it was incredible.")
    print("✅ Memories added.")
except Exception as e:
    print("❌ Error while adding memories:", e)

# Step 4: Search memory
try:
    print("🔍 Searching memory for related thoughts...")
    results = mem.search("What do I enjoy eating?")
    print("🧠 Top memories related to the question:")
    for r in results:
        print("-", r)
except Exception as e:
    print("❌ Error during memory search:", e)
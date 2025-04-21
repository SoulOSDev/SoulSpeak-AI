import pickle
from datetime import datetime
import os

STORE_PATH = "data/memory_store.pkl"

def is_structured(memory):
    return isinstance(memory, dict) and "text" in memory and "tags" in memory and "weight" in memory

def upgrade_memory(memory_list):
    upgraded = []
    for item in memory_list:
        if is_structured(item):
            upgraded.append(item)
        elif isinstance(item, str):
            upgraded.append({
                "text": item,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tags": ["unclassified"],
                "weight": 1.0
            })
        else:
            print(f"Skipped unknown memory format: {item}")
    return upgraded

def load_memory_store():
    if not os.path.exists(STORE_PATH):
        print("No memory store found to upgrade.")
        return []
    with open(STORE_PATH, "rb") as f:
        return pickle.load(f)

def save_memory_store(data):
    with open(STORE_PATH, "wb") as f:
        pickle.dump(data, f)
    print(f"Memory store upgraded and saved. Total entries: {len(data)}")

if __name__ == "__main__":
    print("Upgrading legacy memory format...")
    original = load_memory_store()
    upgraded = upgrade_memory(original)
    save_memory_store(upgraded)
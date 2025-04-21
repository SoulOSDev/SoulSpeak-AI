from memory import Memory

def main():
    mem = Memory()
    tag_counts = mem.get_recent_tag_counts(lookback=7)

    if not tag_counts:
        print("🫥 No emotional tags found in recent memories.")
        return

    print("\n🧠 Soul_AI has detected the following emotional themes in your recent conversations:\n")

    for tag, count in tag_counts.items():
        print(f"🔖 {tag.capitalize()}: {count} mention{'s' if count > 1 else ''}")

if __name__ == "__main__":
    main()
# SoulSpeak v1.0 — Personal Edition

SoulSpeak is a fully local, emotionally intelligent journaling companion.  
It remembers how you’ve been feeling, gently reflects back, and grows with you over time.  
No cloud. No tracking. Just presence.

---

## Features

- Daily journal entries with emotional tagging
- Personalized reflections powered by Mistral (via Ollama)
- Emotional trend awareness and streak sensitivity
- Hybrid memory system (emotional + vector search via FAISS)
- Memory archiving and summarization
- CLI interface for a quiet, focused experience
- macOS `.app` packaging for personal use

---

## Requirements

- Python 3.10–3.13
- Ollama running with the `mistral` model:
  
  ollama run mistral

- Virtual environment with:
  - `requests`
  - `sentence-transformers`
  - `faiss-cpu` (or `faiss` for GPU)
  - `py2app` (for packaging)
  - Any others from `requirements.txt`

---

## Launch Instructions

To run SoulSpeak:

    python3 cli_soul.py

To build the macOS `.app` (if needed):

    python3 setup.py py2app

---

## Data Storage

All data is saved locally in the `/data` folder:

- `memory_log.json` — active emotional memories
- `archive_log.json` — auto-archived memories (30+ days)
- `memory_store.pkl` + `memory_index.faiss` — for semantic recall
- `last_trend_check.json` — timestamp for when trend summaries were last run

---

## Privacy

This app is fully offline and does not communicate with any server.  
Your thoughts remain yours — always.

---

## Future Upgrades (Pinned)

- Tone profile switching
- GUI and voice interface
- Exportable memory summaries
- Real-time “Reflect Back” command

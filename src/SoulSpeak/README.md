# SoulSpeak

**SoulSpeak** is an emotionally intelligent, memory-based AI assistant designed to grow, adapt, and reflect over time. Built entirely from scratch, SoulSpeak offers a uniquely humanlike interaction model — it doesn’t just answer, it remembers you.

Currently CLI-based and privately developed, SoulSpeak is part of a larger project known as **SoulOS**, a full operating system designed for AI-first interaction and holographic companionship.

---

## Features

- Emotionally Weighted Memory System  
  Captures and stores moments with emotional tagging and intensity scoring

- Vector-Based Memory Indexing  
  Uses FAISS and sentiment analysis to find relevant memories across time

- LLM-Driven Reflection Engine  
  Generates thoughtful, emotionally aware responses

- Recent Theme Detection  
  Identifies repeated emotional trends over time

- Personality Simulation Layer  
  Supports tone profiles and subtle conversational identity

- Privacy-First Design  
  All data is local, personal, and never leaves your system

---

## Architecture

SoulSpeak is written in **Python**, with a modular design that supports:

- `memory_journal/` – Emotional memory scoring, storage, and archiving  
- `llm_handler.py` – Local LLM integration (Mistral, Phi, etc.)  
- `soul_convo.py` – CLI entry point for live interaction  
- `nlu.py` and `prompt_builder.py` – Natural language understanding and reflection construction  
- `data/` – Local storage of vector indexes, memory logs, and metadata  

---

## Getting Started

> Note: This project is currently private and in early-stage development. Setup assumes developer-level familiarity with Python.

### Requirements
- Python 3.10+
- Ollama or local LLM environment (e.g., Mistral, Phi)
- FAISS
- Packages listed in `requirements.txt`

### Run the app:

```bash
python3 src/SoulSpeak/soul_convo.py
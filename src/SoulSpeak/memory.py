from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle
from datetime import datetime

def build_emotional_weight_prompt(text):
    return (
        f"On a scale from 0.0 (emotionally neutral) to 1.0 (deeply emotional), "
        f"how emotionally intense is the following statement?\n\n"
        f'"{text}"\n\n'
        f"Respond with only a number between 0.0 and 1.0."
    )

import re
import ollama  # Make sure this is installed and already imported near the top

def get_emotional_weight(text):
    prompt = build_emotional_weight_prompt(text)
    
    response = ollama.chat(
        model='phi',
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract the first float from the model's response
    match = re.search(r"\d*\.\d+|\d+", response['message']['content'])
    if match:
        score = float(match.group())
        return max(0.0, min(score, 1.0))  # Clamp to range [0.0, 1.0]
    else:
        return 0.5  # Fallback in case something goes wrong

class Memory:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='data/memory_index.faiss', store_path='data/memory_store.pkl'):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.store_path = store_path
        self.memory = []
        self.index = None
        self.dim = 384
        self._load()

    def _load(self):
        if os.path.exists(self.index_path) and os.path.exists(self.store_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.store_path, 'rb') as f:
                self.memory = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)

    def _tag_memory(self, text):
        tags = []
        lowered = text.lower()

        if any(phrase in lowered for phrase in ["never good enough", "not capable", "fail", "i'm a failure"]):
            tags.append("self-doubt")
        if any(phrase in lowered for phrase in ["stuck", "can't finish", "go in circles", "always blocked"]):
            tags.append("frustration")
        if any(phrase in lowered for phrase in ["i miss", "i want something more", "i wish", "longing"]):
            tags.append("longing")
        if any(phrase in lowered for phrase in ["alone", "lonely", "no one", "empty", "unseen"]):
            tags.append("loneliness")
        if any(phrase in lowered for phrase in ["things will get better", "i’m changing", "starting over", "hope"]):
            tags.append("hope")

        if not tags:
            tags.append("unclassified")

        return tags

    def _calculate_weight(self, text):
        # Extract emotion tags
        tags = self._tag_memory(text)

        if not tags:
            return 1.0  # fallback for neutral or untagged memories

        # Emotion-to-weight mapping
        emotional_weights = {
            "self-doubt": 2.2,
            "frustration": 1.8,
            "loneliness": 2.5,
            "longing": 2.1,
            "hope": 1.4,
            "gratitude": 1.3,
            "joy": 1.6,
            "anger": 2.0,
            "fear": 2.3,
            "peace": 1.1,
            "unclassified": 1.0
        }

        # Get weights for each tag
        weights = [emotional_weights.get(tag, 1.0) for tag in tags]

        # Return the strongest signal — we’ll assume the most intense tag dominates
        return max(weights)

        tag_score = sum(emotional_weights.get(tag, 1.0) for tag in tags) / max(len(tags), 1)

        # LLM-based scoring
        llm_score = get_emotional_weight(text)

        # Combine and clamp
        combined_score = (tag_score + llm_score) / 2
        return max(0.0, min(combined_score, 1.0))

        total_weight = sum(emotional_weights.get(tag, 1.0) for tag in tags)
        average = total_weight / len(tags) if tags else base_weight
        return round(average, 2)

    def add_memory(self, text):
        embedding = self.model.encode([text])
        self.index.add(embedding)

        tags = self._tag_memory(text)
        weight = self._calculate_weight(text)

        memory_obj = {
            "text": text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tags": tags,
            "weight": weight
        }

        self.memory.append(memory_obj)
        self._save()

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.store_path, 'wb') as f:
            pickle.dump(self.memory, f)

    def search(self, query, top_k=5):
        embedding = self.model.encode([query])
        scores, indices = self.index.search(embedding, len(self.memory))

        weighted_results = []

        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(self.memory):
                memory = self.memory[idx]
                score = scores[0][i]

                # Lower scores = closer match. We'll use inverse so higher = better
                similarity_score = 1 / (score + 1e-5)  # Avoid division by zero

                # Combine semantic similarity with emotional weight
                priority_score = similarity_score * memory.get("weight", 1.0)

                weighted_results.append((priority_score, memory))

        # Sort by combined score descending
        weighted_results.sort(reverse=True, key=lambda x: x[0])

        # Return only the memory objects (not the scores)
        return [memory for _, memory in weighted_results[:top_k]]
    
    def get_recent_tag_counts(self, lookback=7):
            tag_counter = {}

            # Look only at the most recent N memories
            recent_memories = self.memory[-lookback:]

            for mem in recent_memories:
                if isinstance(mem, dict) and "tags" in mem:
                    for tag in mem["tags"]:
                        if tag not in tag_counter:
                            tag_counter[tag] = 0
                        tag_counter[tag] += 1

            # Sort from most to least common
            sorted_tags = dict(sorted(tag_counter.items(), key=lambda x: x[1], reverse=True))

            return sorted_tags
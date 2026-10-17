
import json
import os
import re
from dataclasses import asdict, is_dataclass


class MemoryManager:

    STOP_WORDS = {
        "a", "an", "the", "is", "am", "are", "was", "were",
        "be", "been", "being", "i", "me", "my", "mine", "you",
        "your", "we", "our", "they", "their", "it", "this",
        "that", "what", "which", "who", "whom", "when", "where",
        "why", "how", "do", "does", "did", "have", "has", "had",
        "can", "could", "would", "should", "will", "shall",
        "to", "of", "in", "on", "at", "for", "from", "with",
        "about", "and", "or", "but", "if", "then", "as", "by",
        "working", "work", "tell", "me", "please", "remember"
    }

    def __init__(self, file_path="data/memory/memories.json"):
        self.file_path = file_path
        self.memories = []
        self.load_memories()

    def load_memories(self):
        if not os.path.exists(self.file_path):
            directory = os.path.dirname(self.file_path)

            if directory:
                os.makedirs(directory, exist_ok=True)

            self.save_memories()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.memories = data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            self.memories = []

    def save_memories(self):
        directory = os.path.dirname(self.file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        data = []

        for memory in self.memories:
            if is_dataclass(memory):
                data.append(asdict(memory))
            else:
                data.append(memory)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_memory(self, memory):
        if isinstance(memory, dict):
            new_content = str(memory.get("content", "")).strip()

            if not new_content:
                return False

            for existing in self.memories:
                if isinstance(existing, dict):
                    old_content = str(
                        existing.get("content", "")
                    ).strip()

                    if old_content.casefold() == new_content.casefold():
                        return False

        self.memories.append(memory)
        self.save_memories()
        return True

    def get_memories(self):
        return self.memories

    def get_memory_contents(self):
        contents = []

        for memory in self.memories:
            if isinstance(memory, str):
                contents.append(memory)

            elif isinstance(memory, dict):
                contents.append(memory.get("content", ""))

            elif hasattr(memory, "content"):
                contents.append(memory.content)

        return contents

    
    def _get_keywords(self, text):
        words = re.findall(
            r"[a-zA-Z0-9]+(?:[-_][a-zA-Z0-9]+)*",
            text.casefold()
        )

        return {
            word for word in words
            if word not in self.STOP_WORDS and len(word) > 1
        }


    def search_memories(self, query, limit=5):
        query_words = self._get_keywords(query)

        if not query_words or limit <= 0:
            return []

        matches = []

        for memory in self.memories:
            if isinstance(memory, dict):
                content = str(memory.get("content", ""))
                category = str(memory.get("category", "general"))
                importance = memory.get("importance", 0.5)
            else:
                content = str(memory)
                category = "general"
                importance = 0.5

            memory_words = self._get_keywords(content)

            if not memory_words:
                continue

            matched_words = query_words & memory_words

            if not matched_words:
                if (
                    category == "project"
                    and any(
                        word in query.casefold()
                        for word in ["project", "building", "developing"]
                    )
                ):
                    matches.append((0.1 + 0.15 * importance, memory))
                continue

            relevance = len(matched_words) / len(query_words)

            try:
                importance = float(importance)
            except (TypeError, ValueError):
                importance = 0.5

            importance = max(0.0, min(1.0, importance))

            score = relevance + (0.15 * importance)

            matches.append((score, memory))

        matches.sort(key=lambda item: item[0], reverse=True)

        return [
            memory for _, memory in matches[:limit]
        ]

    def delete_memory(self, index):
        if index < 0 or index >= len(self.memories):
            return False

        del self.memories[index]
        self.save_memories()
        return True

    def clear_memories(self):
        self.memories = []
        self.save_memories()

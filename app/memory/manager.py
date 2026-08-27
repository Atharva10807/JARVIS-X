import json
import os
import re
from dataclasses import asdict, is_dataclass


class MemoryManager:

    def __init__(self, file_path="data/memory/memories.json"):
        self.file_path = file_path
        self.memories = []
        self.load_memories()

    def load_memories(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self.save_memories()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.memories = json.load(file)
        except (json.JSONDecodeError, OSError):
            self.memories = []

    def save_memories(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        data = []

        for memory in self.memories:
            if is_dataclass(memory):
                data.append(asdict(memory))
            else:
                data.append(memory)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_memory(self, memory):
        self.memories.append(memory)
        self.save_memories()

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

    def search_memories(self, query):
        """
        Return memories that are relevant to the supplied query.
        Uses simple keyword matching for the current development version.
        """

        query_words = set(
            re.findall(r"\b[a-zA-Z0-9_-]+\b", query.lower())
        )

        if not query_words:
            return []

        matches = []

        for memory in self.memories:
            if isinstance(memory, dict):
                content = memory.get("content", "")
                category = memory.get("category", "general")
            else:
                content = str(memory)
                category = "general"

            memory_words = set(
                re.findall(r"\b[a-zA-Z0-9_-]+\b", content.lower())
            )

            score = len(query_words & memory_words)

            if score > 0:
                matches.append((score, memory))

        matches.sort(key=lambda item: item[0], reverse=True)

        return [memory for _, memory in matches]
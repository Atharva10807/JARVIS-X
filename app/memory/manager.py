import json
import os
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
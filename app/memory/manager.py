import json
import os


class MemoryManager:
    def __init__(self, file_path="data/memory/memories.json"):
        self.file_path = file_path
        self.memories = self.load_memories()

    def load_memories(self):
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def save_memories(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.memories, file, indent=4)

    def add_memory(self, memory):
        if memory not in self.memories:
            self.memories.append(memory)
            self.save_memories()

    def get_memories(self):
        return self.memories
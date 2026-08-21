from app.memory.models import Memory


class MemoryExtractor:
    def extract(self, user_input):
        text = user_input.strip()

        if not text:
            return None

        lower_text = text.lower()

        if lower_text.startswith("my name is "):
            return Memory(
                content=text,
                category="personal",
                importance=0.9
            )

        if lower_text.startswith("i am building "):
            return Memory(
                content=text,
                category="project",
                importance=0.9
            )

        if lower_text.startswith("my project is "):
            return Memory(
                content=text,
                category="project",
                importance=0.95
            )

        if lower_text.startswith("i prefer "):
            return Memory(
                content=text,
                category="preference",
                importance=0.8
            )

        if lower_text.startswith("my goal is "):
            return Memory(
                content=text,
                category="goal",
                importance=0.9
            )

        return None
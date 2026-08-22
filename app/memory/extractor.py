import json
import os

import ollama

from app.memory.models import Memory


class MemoryExtractor:

    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "qwen3:4b")

    def extract(self, user_input):
        if not user_input.strip():
            return None

        prompt = f"""
You are the memory extraction system for JARVIS-X.

Analyze the user's message and decide whether it contains information
that should be remembered for future conversations.

Remember:
- Personal information
- User preferences
- Important goals
- Projects
- Skills
- Important plans
- Long-term facts about the user

Do NOT remember:
- Normal questions
- General knowledge
- Temporary conversation
- Casual statements with no future value

Return ONLY JSON.

The JSON must contain:
- should_remember: boolean
- content: concise normalized memory
- category: personal, preference, project, goal, skill, plan, or other
- importance: number from 0.0 to 1.0

If the message should not be remembered, return:

{{
    "should_remember": false,
    "content": "",
    "category": "other",
    "importance": 0.0
}}

User message:
{user_input}
"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                format={
                    "type": "object",
                    "properties": {
                        "should_remember": {
                            "type": "boolean"
                        },
                        "content": {
                            "type": "string"
                        },
                        "category": {
                            "type": "string",
                            "enum": [
                                "personal",
                                "preference",
                                "project",
                                "goal",
                                "skill",
                                "plan",
                                "other"
                            ]
                        },
                        "importance": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "should_remember",
                        "content",
                        "category",
                        "importance"
                    ]
                },
                options={
                    "temperature": 0
                }
            )

            content = response["message"]["content"]
            data = json.loads(content)

            if not data.get("should_remember"):
                return None

            memory_content = data.get("content", "").strip()
            category = data.get("category", "other")
            importance = float(data.get("importance", 0.0))

            if not memory_content:
                return None

            importance = max(0.0, min(1.0, importance))

            return Memory(
                content=memory_content,
                category=category,
                importance=importance
            )

        except Exception as e:
            print(f"Memory extraction error: {e}")
            return None
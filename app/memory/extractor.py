import json
import os

import requests

from app.memory.models import Memory


class MemoryExtractor:

    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model = os.getenv("OLLAMA_MODEL", "qwen3")

    def extract(self, user_input):
        if not user_input.strip():
            return None

        prompt = f"""
You are the memory extraction system for JARVIS-X.

Analyze the user's message and decide whether it contains information
that should be remembered for future conversations.

Remember information such as:
- Personal information
- User preferences
- Important goals
- Projects
- Skills
- Important plans
- Long-term facts about the user

Do NOT remember:
- Normal questions
- Temporary conversation
- General knowledge
- Requests that do not reveal lasting user information
- Casual statements with no future value

Return ONLY valid JSON in this exact format:

{{
    "should_remember": true,
    "content": "short normalized memory",
    "category": "personal",
    "importance": 0.0
}}

Rules:
- should_remember must be true or false.
- content must be concise.
- category must be one of:
  personal, preference, project, goal, skill, plan, other
- importance must be between 0.0 and 1.0.
- If the information is not worth remembering:
  should_remember must be false,
  content must be "",
  category must be "other",
  importance must be 0.0.

User message:
{user_input}
"""

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "format": {
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
            "options": {
                "temperature": 0
            }
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=60
            )

            response.raise_for_status()

            result = response.json()
            content = result["message"]["content"]
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

        except Exception:
            return None
from app.llm.client import LLMClient
from app.memory.manager import MemoryManager


class Jarvis:
    def __init__(self):
        self.llm = LLMClient()
        self.memory = MemoryManager()

        self.system_prompt = """
You are JARVIS-X, a personal AI assistant.

Your primary purpose is to help the user understand information,
solve problems, organize tasks, learn concepts, and accomplish
goals safely and efficiently.

Behavior rules:

1. Be helpful, clear, and concise.
2. Explain technical concepts according to the user's level.
3. Break complex tasks into logical steps.
4. Do not invent facts.
5. Clearly state uncertainty when you are not sure.
6. Never claim to have performed an action that you did not perform.
7. Protect user privacy and sensitive information.
8. Ask for confirmation before sensitive actions.
9. Maintain context throughout the current conversation.
10. Use available long-term memory when it is relevant.

You are currently operating in the text-only development version
of JARVIS-X.

You do not currently have access to:
- Files
- Web browsers
- Camera
- Microphone
- Computer control
- IoT devices
- External applications

Only claim to have access to a capability when that capability
has actually been implemented and provided to you by the application.
"""

        self.conversation = []

    def respond(self, user_input):
        if not user_input.strip():
            return "Please provide something for me to work with."

        if user_input.lower().startswith("remember "):
            memory = user_input[9:].strip()

            if memory:
                self.memory.add_memory(memory)
                return "I will remember that."

        memories = self.memory.get_memories()

        memory_text = ""

        if memories:
            memory_text = "\nKnown user information:\n"

            for memory in memories:
                memory_text += f"- {memory}\n"

        messages = [
            {
                "role": "system",
                "content": self.system_prompt + memory_text
            }
        ]

        messages.extend(self.conversation)

        messages.append({
            "role": "user",
            "content": user_input
        })

        response = self.llm.generate_response(messages)

        self.conversation.append({
            "role": "user",
            "content": user_input
        })

        self.conversation.append({
            "role": "assistant",
            "content": response
        })

        return response

import re

from app.llm.client import LLMClient
from app.memory.manager import MemoryManager


class Jarvis:

    def __init__(self):
        self.llm = LLMClient()
        self.memory = MemoryManager()
        self.pending_memory_clear = False

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
10. Use relevant long-term memory when it helps answer the user's request.
11. Do not mention memories unless they are relevant to the response.
12. Do not claim knowledge that is not present in the conversation or memory.

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

    def _save_memory(self, content, category, importance):
        memories = self.memory.get_memories()

        for memory in memories:
            if isinstance(memory, dict):
                existing_content = memory.get("content", "")

                if existing_content.casefold() == content.casefold():
                    return False

        return self.memory.add_memory({
            "content": content,
            "category": category,
            "importance": importance
        })

    def _extract_memory(self, user_input):
        text = user_input.strip()

        project_match = re.search(
            r"\bmy project is(?: called)?\s+(.+?)[.!?]?$",
            text,
            re.IGNORECASE
        )

        if project_match:
            project_name = project_match.group(1).strip()

            content = f"My project is {project_name}."

            self._save_memory(content, "project", 0.95)
            return content

        preference_match = re.search(
            r"\bi prefer\s+(.+?)[.!?]?$",
            text,
            re.IGNORECASE
        )

        if preference_match:
            preference = preference_match.group(1).strip()

            content = f"I prefer {preference}."

            self._save_memory(content, "preference", 0.85)
            return content

        return None

    def _handle_remember_command(self, user_input):
        memory = re.sub(
            r"^remember\s+(that\s+)?",
            "",
            user_input.strip(),
            flags=re.IGNORECASE
        ).strip()

        if not memory:
            return None

        memory = memory.rstrip(".!?")

        category = "general"
        importance = 0.80

        if re.search(
            r"\b(project|working on|building|developing)\b",
            memory,
            re.IGNORECASE
        ):
            category = "project"
            importance = 0.95

        content = memory[0].upper() + memory[1:] + "."
        self._save_memory(content, category, importance)

        return content

    def _handle_memory_command(self, user_input):
        command = user_input.strip().casefold()
        memories = self.memory.get_memories()

        if command == "memory list":
            if not memories:
                return "No saved memories found."

            lines = ["Saved memories:"]

            for index, memory in enumerate(memories, start=1):
                if isinstance(memory, dict):
                    content = memory.get("content", "")
                    category = memory.get("category", "general")
                else:
                    content = str(memory)
                    category = "general"

                lines.append(
                    f"{index}. {content} [{category}]"
                )

            return "\n".join(lines)

        if command.startswith("memory delete "):
            number_text = command[len("memory delete "):].strip()

            if not number_text.isdigit():
                return "Use: memory delete <number>"

            index = int(number_text) - 1

            if not self.memory.delete_memory(index):
                return "Invalid memory number. Use 'memory list' to see valid numbers."

            self.pending_memory_clear = False
            return f"Memory {index + 1} deleted successfully."

        if command == "memory clear":
            if not memories:
                return "There are no memories to clear."

            self.pending_memory_clear = True
            return (
                f"This will permanently delete all {len(memories)} saved memories. "
                "Type 'confirm clear' to proceed or 'cancel clear' to cancel."
            )

        return None

    def _get_relevant_memories(self, user_input):
        return self.memory.search_memories(user_input)

    def respond(self, user_input):
        if not user_input.strip():
            return "Please provide something for me to work with."

        user_input = user_input.strip()
        command = user_input.casefold()

        if command == "exit":
            return "Shutting down. Goodbye."

        if self.pending_memory_clear:
            if command == "confirm clear":
                self.memory.clear_memories()
                self.pending_memory_clear = False
                return "All saved memories have been deleted."

            if command == "cancel clear":
                self.pending_memory_clear = False
                return "Memory clearing cancelled."

            self.pending_memory_clear = False

        if command.startswith("memory "):
            result = self._handle_memory_command(user_input)

            if result is not None:
                return result

        if command.startswith("remember "):
            self._handle_remember_command(user_input)
        else:
            self._extract_memory(user_input)

        relevant_memories = self._get_relevant_memories(user_input)

        memory_text = ""

        if relevant_memories:
            memory_text = "\nRelevant long-term memory:\n"

            for memory in relevant_memories:
                if isinstance(memory, dict):
                    content = memory.get("content", "")
                    category = memory.get("category", "general")
                    memory_text += f"- {content} [{category}]\n"
                else:
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

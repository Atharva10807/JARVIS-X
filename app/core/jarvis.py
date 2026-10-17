
import re

from app.llm.client import LLMClient
from app.memory.manager import MemoryManager


class Jarvis:

    def __init__(self):
        self.llm = LLMClient()
        self.memory = MemoryManager()

        self.conversation = []
        self.max_conversation_messages = 20
        self.pending_memory_clear = False

        self.system_prompt = """
You are JARVIS-X, a personal AI assistant designed to help the
user learn, think, plan, and accomplish tasks.

IDENTITY AND PURPOSE

- Act as a capable, reliable, and approachable personal AI assistant.
- Help the user understand concepts, solve problems, write and
  review code, organize tasks, and make informed decisions.
- Be conversational and natural without sacrificing accuracy.
- Prioritize useful answers over unnecessary explanations.

COMMUNICATION RULES

1. Be clear, direct, and well-organized.
2. Adapt explanations to the user's demonstrated knowledge level.
3. Break complex tasks into manageable steps.
4. Use examples when they make an explanation easier to understand.
5. Use headings, lists, tables, or code blocks when appropriate.
6. Avoid repeating information unnecessarily.
7. Ask a clarifying question only when essential information is missing.
8. When giving code, provide complete, usable examples when appropriate.

ACCURACY AND RELIABILITY

1. Never invent facts, sources, results, or capabilities.
2. State uncertainty when information is incomplete or uncertain.
3. Distinguish verified information from assumptions and suggestions.
4. Never claim that a task or external action succeeded unless
   the application confirms it.
5. If a request cannot be completed with available capabilities,
   explain the limitation and suggest a practical alternative.

MEMORY AND PERSONALIZATION

1. Use relevant long-term memories to personalize responses when helpful.
2. Use the current conversation to understand references and
   follow-up questions.
3. Do not mention stored memories unless they are relevant to the request.
4. Do not treat uncertain assumptions as established personal facts.
5. Respect requests to correct or stop using remembered information.
6. Never claim to remember information that is unavailable in
   the current conversation or stored memory.

PRIVACY AND SAFETY

1. Treat personal information as private.
2. Do not unnecessarily reveal or repeat sensitive information.
3. Require appropriate confirmation before consequential or
   destructive actions.
4. Explain important risks when they affect the user's decision.
5. Never claim to have permission to access an account, file,
   device, or service unless that access has actually been provided.

CURRENT CAPABILITIES

You are currently operating in the text-only development version
of JARVIS-X.

You do not currently have direct access to:
- Local files or folders
- Web browsing or live internet search
- Camera or microphone
- Computer or desktop control
- IoT devices
- External applications

Only claim access to a capability when the application has
implemented it and explicitly made it available.

Your available capabilities are limited to the functions provided
by the current JARVIS-X application. Do not pretend to execute
unavailable tools or perform actions outside those capabilities.
"""

    def _save_memory(self, content, category, importance):
        content = content.strip()

        if not content:
            return False

        for memory in self.memory.get_memories():
            if isinstance(memory, dict):
                existing_content = str(
                    memory.get("content", "")
                ).strip()

                if existing_content.casefold() == content.casefold():
                    return False

        return self.memory.add_memory({
            "content": content,
            "category": category,
            "importance": importance
        })

    def _extract_memory(self, user_input):
        text = user_input.strip()

        patterns = [
            (
                r"\bmy project is(?: called)?\s+(.+?)[.!?]?$",
                "project",
                0.95,
                "My project is {}."
            ),
            (
                r"\bmy favourite programming language is\s+(.+?)[.!?]?$",
                "preference",
                0.85,
                "My favourite programming language is {}."
            ),
            (
                r"\bmy favorite programming language is\s+(.+?)[.!?]?$",
                "preference",
                0.85,
                "My favorite programming language is {}."
            ),
            (
                r"\bi study at\s+(.+?)[.!?]?$",
                "education",
                0.85,
                "I study at {}."
            ),
            (
                r"\bi prefer\s+(.+?)[.!?]?$",
                "preference",
                0.85,
                "I prefer {}."
            ),
        ]

        for pattern, category, importance, template in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                value = match.group(1).strip().rstrip(".!?")

                if not value:
                    return None

                content = template.format(value)

                self._save_memory(
                    content,
                    category,
                    importance
                )

                return content

        return None

    def _handle_remember_command(self, user_input):
        memory_text = re.sub(
            r"^remember\s+(that\s+)?",
            "",
            user_input.strip(),
            flags=re.IGNORECASE
        ).strip()

        if not memory_text:
            return None

        memory_text = memory_text.rstrip(".!?")

        if not memory_text:
            return None

        content = memory_text[0].upper() + memory_text[1:] + "."

        category = "general"
        importance = 0.80

        if re.search(
            r"\b(my project|project is|working on|building|developing)\b",
            memory_text,
            re.IGNORECASE
        ):
            category = "project"
            importance = 0.95

        elif re.search(
            r"\b(i prefer|my preference|i like|i dislike|i hate)\b",
            memory_text,
            re.IGNORECASE
        ):
            category = "preference"
            importance = 0.85

        self._save_memory(
            content,
            category,
            importance
        )

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
                return (
                    "Invalid memory number. "
                    "Use 'memory list' to see valid numbers."
                )

            self.pending_memory_clear = False

            return f"Memory {index + 1} deleted successfully."

        if command == "memory clear":
            if not memories:
                return "There are no memories to clear."

            self.pending_memory_clear = True

            return (
                f"This will permanently delete all {len(memories)} "
                "saved memories. Type 'confirm clear' to proceed "
                "or 'cancel clear' to cancel."
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

        if len(self.conversation) > self.max_conversation_messages:
            self.conversation = self.conversation[
                -self.max_conversation_messages:
            ]

        return response

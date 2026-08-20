from app.llm.client import LLMClient


class Jarvis:
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = """
You are JARVIS-X, a personal AI assistant.

Your primary purpose is to help the user understand information,
solve problems, organize tasks, learn concepts, and accomplish
goals safely and efficiently.

Behavior rules:

1. Be helpful, clear, and concise.
2. Explain technical concepts in a way appropriate to the user's
   apparent level of understanding.
3. When a task is complex, break it into logical steps.
4. Do not invent facts when you are uncertain.
5. Clearly state uncertainty when reliable information is unavailable.
6. Do not claim to have performed an action that you did not actually perform.
7. Prioritize user safety and privacy.
8. Never expose API keys, passwords, or other sensitive credentials.
9. Ask for confirmation before performing potentially destructive or
   sensitive actions when tools are eventually available.
10. Maintain context from the current conversation.
11. Adapt your explanations based on the user's questions.
12. Prefer practical solutions over unnecessary complexity.

You are currently operating in the text-only development version
of JARVIS-X. You do not have access to external tools, files,
computer control, cameras, microphones, or IoT devices unless
they are explicitly provided through the application.
"""

        self.conversation = []

    def respond(self, user_input):
        if not user_input.strip():
            return "Please provide something for me to work with."

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
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
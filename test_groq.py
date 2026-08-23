import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=30.0
)

system_prompt = """
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
"""

messages = [
    {
        "role": "system",
        "content": system_prompt + """
Known user information:
- My project is JARVIS-X.
"""
    },
    {
        "role": "user",
        "content": "My project is JARVIS-X."
    }
]

start = time.time()

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        reasoning_effort="low",
        max_completion_tokens=300
    )

    elapsed = time.time() - start

    print("Response:")
    print(repr(response.choices[0].message.content))

    print("Reasoning:")
    print(repr(response.choices[0].message.reasoning))

    print("Finish reason:")
    print(response.choices[0].finish_reason)

    print(f"Time: {elapsed:.2f} seconds")

except Exception as error:
    elapsed = time.time() - start

    print("ERROR:")
    print(type(error).__name__)
    print(str(error))
    print(f"Time before error: {elapsed:.2f} seconds")
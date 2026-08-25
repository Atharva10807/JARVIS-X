import os
import time

from groq import Groq


class GroqProvider:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY was not found in environment variables"
            )

        self.client = Groq(
            api_key=api_key,
            timeout=30.0
        )

        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )

    def generate_response(self, messages):
        for attempt in range(2):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    reasoning_effort="low",
                    max_completion_tokens=300
                )

                return response.choices[0].message.content

            except Exception:
                if attempt == 1:
                    raise

                time.sleep(1)
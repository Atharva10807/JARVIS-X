import ollama


class LLMClient:
    def __init__(self):
        self.model = "qwen3:4b"

    def generate_response(self, messages):
        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        return response["message"]["content"]
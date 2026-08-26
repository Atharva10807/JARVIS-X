import os

from dotenv import load_dotenv

from app.llm.providers.groq_provider import GroqProvider
from app.llm.providers.omniroute_provider import OmniRouteProvider


class LLMClient:

    def __init__(self):
        load_dotenv()

        self.provider_name = os.getenv(
            "LLM_PROVIDER",
            "groq"
        ).lower()

        self.provider = self._create_provider()

    def _create_provider(self):

        if self.provider_name == "groq":
            return GroqProvider()

        if self.provider_name == "omniroute":
            return OmniRouteProvider()

        raise ValueError(
            f"Unsupported LLM provider: {self.provider_name}"
        )

    def generate_response(self, messages):
        return self.provider.generate_response(messages)
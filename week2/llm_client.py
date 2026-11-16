from abc import ABC, abstractmethod
from typing import Any

import requests
from google import genai


class LLMProvider(ABC):
    """Base interface for all LLM providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the model."""
        pass


class GeminiProvider(LLMProvider):
    """Google Gemini cloud provider."""

    DEFAULT_MODEL = "gemini-3.8-flash"

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text


class OllamaProvider(LLMProvider):
    """Local Ollama provider."""

    DEFAULT_URL = "http://localhost:11434/api/generate"

    def __init__(
        self,
        model: str = "llama3.2",
        url: str = DEFAULT_URL,
    ) -> None:
        self.model = model
        self.url = url

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data: dict[str, Any] = response.json()
        return data["response"]


class LLMClient:
    """Client wrapper around any LLM provider."""

    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)
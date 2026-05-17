"""Ollama local provider (OpenAI-compatible API)."""
import os

from openai import OpenAI


class OllamaProvider:
    """Wraps Ollama's OpenAI-compatible chat completions endpoint."""

    def __init__(self) -> None:
        self._model = os.getenv("OLLAMA_MODEL", "llama3.2")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        # Ollama accepts any non-empty string as api_key
        self._client = OpenAI(base_url=base_url, api_key="ollama")

    def complete(self, messages: list[dict[str, str]]) -> str:
        """Send messages to the local Ollama instance and return the reply."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
        )
        return response.choices[0].message.content or ""

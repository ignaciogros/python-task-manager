"""Generic OpenAI-compatible provider (Qwen, Mistral-Small, etc.)."""
import os

from openai import OpenAI


class OpenAICompatProvider:
    """Wraps any OpenAI-compatible chat completions endpoint."""

    def __init__(self) -> None:
        endpoint = os.getenv("COMPAT_ENDPOINT")
        api_key = os.getenv("COMPAT_API_KEY")
        self._model = os.getenv("COMPAT_MODEL")
        if not endpoint or not api_key or not self._model:
            raise ValueError("COMPAT_ENDPOINT, COMPAT_API_KEY and COMPAT_MODEL must be set")
        self._client = OpenAI(base_url=endpoint, api_key=api_key)

    def complete(self, messages: list[dict[str, str]]) -> str:
        """Send messages to the configured endpoint and return the reply."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
        )
        return response.choices[0].message.content or ""

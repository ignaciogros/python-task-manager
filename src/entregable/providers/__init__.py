"""LLM provider abstraction: Protocol + factory."""
import os
from typing import Protocol


class LLMProvider(Protocol):
    """Common interface for all LLM backends."""

    def complete(self, messages: list[dict[str, str]]) -> str:
        """Send messages and return the assistant reply."""
        ...


def get_provider() -> LLMProvider:
    """Instantiate the provider selected via the PROVIDER env var."""
    name = os.getenv("PROVIDER", "azure").lower()
    if name == "azure":
        from src.entregable.providers.azure import AzureProvider
        return AzureProvider()
    if name == "ollama":
        from src.entregable.providers.ollama import OllamaProvider
        return OllamaProvider()
    if name == "openai_compat":
        from src.entregable.providers.openai_compat import OpenAICompatProvider
        return OpenAICompatProvider()
    raise ValueError(f"Unknown PROVIDER value: '{name}'. Valid options: azure, ollama, openai_compat")

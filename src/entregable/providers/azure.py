"""Azure OpenAI provider."""
import os

from openai import AzureOpenAI


class AzureProvider:
    """Wraps the Azure OpenAI chat completions API."""

    def __init__(self) -> None:
        endpoint = os.getenv("AZURE_ENDPOINT")
        api_key = os.getenv("AZURE_API_KEY")
        api_version = os.getenv("AZURE_API_VERSION", "2024-02-01")
        if not endpoint or not api_key:
            raise ValueError("AZURE_ENDPOINT and AZURE_API_KEY must be set")
        self._deployment = os.getenv("AZURE_DEPLOYMENT")
        if not self._deployment:
            raise ValueError("AZURE_DEPLOYMENT must be set")
        self._client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )

    def complete(self, messages: list[dict[str, str]]) -> str:
        """Send messages to Azure OpenAI and return the assistant reply."""
        response = self._client.chat.completions.create(
            model=self._deployment,
            messages=messages,  # type: ignore[arg-type]
        )
        return response.choices[0].message.content or ""

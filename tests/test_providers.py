"""Tests for LLM provider adapters and get_provider() factory."""
from unittest.mock import MagicMock, patch

import pytest

from src.entregable.providers import get_provider
from src.entregable.providers.azure import AzureProvider
from src.entregable.providers.ollama import OllamaProvider
from src.entregable.providers.openai_compat import OpenAICompatProvider

_AZURE_ENV = {
    "AZURE_ENDPOINT": "https://example.openai.azure.com/",
    "AZURE_API_KEY": "key",
    "AZURE_DEPLOYMENT": "gpt-4o-mini",
}
_COMPAT_ENV = {
    "COMPAT_ENDPOINT": "https://example.com/v1",
    "COMPAT_API_KEY": "key",
    "COMPAT_MODEL": "qwen",
}


def _mock_completion(content: str | None) -> MagicMock:
    mock = MagicMock()
    mock.choices[0].message.content = content
    return mock


# ── AzureProvider ─────────────────────────────────────────────────────────────

class TestAzureProvider:
    def test_raises_without_endpoint(self, monkeypatch) -> None:
        monkeypatch.delenv("AZURE_ENDPOINT", raising=False)
        monkeypatch.setenv("AZURE_API_KEY", "key")
        monkeypatch.setenv("AZURE_DEPLOYMENT", "dep")
        with pytest.raises(ValueError):
            AzureProvider()

    def test_raises_without_api_key(self, monkeypatch) -> None:
        monkeypatch.setenv("AZURE_ENDPOINT", "https://x.com/")
        monkeypatch.delenv("AZURE_API_KEY", raising=False)
        monkeypatch.setenv("AZURE_DEPLOYMENT", "dep")
        with pytest.raises(ValueError):
            AzureProvider()

    def test_raises_without_deployment(self, monkeypatch) -> None:
        monkeypatch.setenv("AZURE_ENDPOINT", "https://x.com/")
        monkeypatch.setenv("AZURE_API_KEY", "key")
        monkeypatch.delenv("AZURE_DEPLOYMENT", raising=False)
        with pytest.raises(ValueError):
            AzureProvider()

    def test_complete_returns_content(self, monkeypatch) -> None:
        for k, v in _AZURE_ENV.items():
            monkeypatch.setenv(k, v)
        with patch("src.entregable.providers.azure.AzureOpenAI") as mock_cls:
            mock_cls.return_value.chat.completions.create.return_value = _mock_completion("azure reply")
            result = AzureProvider().complete([{"role": "user", "content": "hi"}])
        assert result == "azure reply"

    def test_complete_returns_empty_string_on_none_content(self, monkeypatch) -> None:
        for k, v in _AZURE_ENV.items():
            monkeypatch.setenv(k, v)
        with patch("src.entregable.providers.azure.AzureOpenAI") as mock_cls:
            mock_cls.return_value.chat.completions.create.return_value = _mock_completion(None)
            result = AzureProvider().complete([])
        assert result == ""


# ── OllamaProvider ────────────────────────────────────────────────────────────

class TestOllamaProvider:
    def test_uses_default_model(self, monkeypatch) -> None:
        monkeypatch.delenv("OLLAMA_MODEL", raising=False)
        with patch("src.entregable.providers.ollama.OpenAI"):
            assert OllamaProvider()._model == "llama3.2"

    def test_uses_env_model(self, monkeypatch) -> None:
        monkeypatch.setenv("OLLAMA_MODEL", "mistral")
        with patch("src.entregable.providers.ollama.OpenAI"):
            assert OllamaProvider()._model == "mistral"

    def test_complete_returns_content(self, monkeypatch) -> None:
        with patch("src.entregable.providers.ollama.OpenAI") as mock_cls:
            mock_cls.return_value.chat.completions.create.return_value = _mock_completion("ollama reply")
            result = OllamaProvider().complete([{"role": "user", "content": "hi"}])
        assert result == "ollama reply"

    def test_complete_returns_empty_string_on_none_content(self) -> None:
        with patch("src.entregable.providers.ollama.OpenAI") as mock_cls:
            mock_cls.return_value.chat.completions.create.return_value = _mock_completion(None)
            result = OllamaProvider().complete([])
        assert result == ""


# ── OpenAICompatProvider ──────────────────────────────────────────────────────

class TestOpenAICompatProvider:
    def test_raises_without_endpoint(self, monkeypatch) -> None:
        monkeypatch.delenv("COMPAT_ENDPOINT", raising=False)
        monkeypatch.setenv("COMPAT_API_KEY", "key")
        monkeypatch.setenv("COMPAT_MODEL", "qwen")
        with pytest.raises(ValueError):
            OpenAICompatProvider()

    def test_raises_without_api_key(self, monkeypatch) -> None:
        monkeypatch.setenv("COMPAT_ENDPOINT", "https://x.com/v1")
        monkeypatch.delenv("COMPAT_API_KEY", raising=False)
        monkeypatch.setenv("COMPAT_MODEL", "qwen")
        with pytest.raises(ValueError):
            OpenAICompatProvider()

    def test_raises_without_model(self, monkeypatch) -> None:
        monkeypatch.setenv("COMPAT_ENDPOINT", "https://x.com/v1")
        monkeypatch.setenv("COMPAT_API_KEY", "key")
        monkeypatch.delenv("COMPAT_MODEL", raising=False)
        with pytest.raises(ValueError):
            OpenAICompatProvider()

    def test_complete_returns_content(self, monkeypatch) -> None:
        for k, v in _COMPAT_ENV.items():
            monkeypatch.setenv(k, v)
        with patch("src.entregable.providers.openai_compat.OpenAI") as mock_cls:
            mock_cls.return_value.chat.completions.create.return_value = _mock_completion("compat reply")
            result = OpenAICompatProvider().complete([{"role": "user", "content": "hi"}])
        assert result == "compat reply"

    def test_complete_returns_empty_string_on_none_content(self, monkeypatch) -> None:
        for k, v in _COMPAT_ENV.items():
            monkeypatch.setenv(k, v)
        with patch("src.entregable.providers.openai_compat.OpenAI") as mock_cls:
            mock_cls.return_value.chat.completions.create.return_value = _mock_completion(None)
            result = OpenAICompatProvider().complete([])
        assert result == ""


# ── get_provider() factory ────────────────────────────────────────────────────

class TestGetProvider:
    def test_returns_azure_provider(self, monkeypatch) -> None:
        monkeypatch.setenv("PROVIDER", "azure")
        for k, v in _AZURE_ENV.items():
            monkeypatch.setenv(k, v)
        with patch("src.entregable.providers.azure.AzureOpenAI"):
            assert isinstance(get_provider(), AzureProvider)

    def test_defaults_to_azure(self, monkeypatch) -> None:
        monkeypatch.delenv("PROVIDER", raising=False)
        for k, v in _AZURE_ENV.items():
            monkeypatch.setenv(k, v)
        with patch("src.entregable.providers.azure.AzureOpenAI"):
            assert isinstance(get_provider(), AzureProvider)

    def test_returns_ollama_provider(self, monkeypatch) -> None:
        monkeypatch.setenv("PROVIDER", "ollama")
        with patch("src.entregable.providers.ollama.OpenAI"):
            assert isinstance(get_provider(), OllamaProvider)

    def test_returns_openai_compat_provider(self, monkeypatch) -> None:
        monkeypatch.setenv("PROVIDER", "openai_compat")
        for k, v in _COMPAT_ENV.items():
            monkeypatch.setenv(k, v)
        with patch("src.entregable.providers.openai_compat.OpenAI"):
            assert isinstance(get_provider(), OpenAICompatProvider)

    def test_raises_for_unknown_provider(self, monkeypatch) -> None:
        monkeypatch.setenv("PROVIDER", "unknown")
        with pytest.raises(ValueError, match="unknown"):
            get_provider()

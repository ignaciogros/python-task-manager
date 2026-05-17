"""Tests for AI-powered task endpoints."""
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.entregable.main import app

client = TestClient(app)

TASK_PAYLOAD: dict = {
    "id": "test-id-123",
    "title": "Implement login",
    "description": "",
    "priority": "alta",
    "effort_hours": 0.0,
    "status": "pendiente",
    "assigned_to": "Ana",
    "category": None,
    "risk_analysis": None,
    "risk_mitigation": None,
}


def _mock_provider(reply: str | list[str]) -> MagicMock:
    """Return a provider mock whose complete() returns reply (or side_effect list)."""
    mock = MagicMock()
    if isinstance(reply, list):
        mock.complete.side_effect = reply
    else:
        mock.complete.return_value = reply
    return mock


# ── /describe ────────────────────────────────────────────────────────────────

def test_describe_fills_description() -> None:
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider("Login flow description.")):
        response = client.post("/ai/tasks/describe", json=TASK_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["description"] == "Login flow description."


def test_describe_preserves_other_fields() -> None:
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider("Desc.")):
        data = client.post("/ai/tasks/describe", json=TASK_PAYLOAD).json()
    assert data["title"] == TASK_PAYLOAD["title"]
    assert data["priority"] == TASK_PAYLOAD["priority"]


def test_describe_returns_502_on_provider_error() -> None:
    mock = MagicMock()
    mock.complete.side_effect = RuntimeError("connection refused")
    with patch("src.entregable.ai_router.get_provider", return_value=mock):
        response = client.post("/ai/tasks/describe", json=TASK_PAYLOAD)
    assert response.status_code == 502


# ── /categorize ──────────────────────────────────────────────────────────────

def test_categorize_fills_category() -> None:
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider("Backend")):
        response = client.post("/ai/tasks/categorize", json=TASK_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["category"] == "Backend"


def test_categorize_strips_whitespace() -> None:
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider("  Frontend  \n")):
        data = client.post("/ai/tasks/categorize", json=TASK_PAYLOAD).json()
    assert data["category"] == "Frontend"


def test_categorize_returns_502_on_provider_error() -> None:
    mock = MagicMock()
    mock.complete.side_effect = RuntimeError("timeout")
    with patch("src.entregable.ai_router.get_provider", return_value=mock):
        response = client.post("/ai/tasks/categorize", json=TASK_PAYLOAD)
    assert response.status_code == 502


# ── /estimate ─────────────────────────────────────────────────────────────────

def test_estimate_fills_effort_hours() -> None:
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider("8")):
        response = client.post("/ai/tasks/estimate", json=TASK_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["effort_hours"] == 8.0


def test_estimate_parses_decimal() -> None:
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider("3.5")):
        data = client.post("/ai/tasks/estimate", json=TASK_PAYLOAD).json()
    assert data["effort_hours"] == 3.5


def test_estimate_parses_number_from_prose() -> None:
    # LLM may return surrounding text; regex must extract the number
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider("approximately 12 hours")):
        data = client.post("/ai/tasks/estimate", json=TASK_PAYLOAD).json()
    assert data["effort_hours"] == 12.0


def test_estimate_returns_422_when_no_number() -> None:
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider("I cannot estimate this.")):
        response = client.post("/ai/tasks/estimate", json=TASK_PAYLOAD)
    assert response.status_code == 422


def test_estimate_returns_502_on_provider_error() -> None:
    mock = MagicMock()
    mock.complete.side_effect = RuntimeError("api error")
    with patch("src.entregable.ai_router.get_provider", return_value=mock):
        response = client.post("/ai/tasks/estimate", json=TASK_PAYLOAD)
    assert response.status_code == 502


# ── /audit ────────────────────────────────────────────────────────────────────

def test_audit_fills_risk_fields() -> None:
    replies = ["High complexity risk.", "Add code reviews."]
    with patch("src.entregable.ai_router.get_provider", return_value=_mock_provider(replies)):
        response = client.post("/ai/tasks/audit", json=TASK_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_analysis"] == "High complexity risk."
    assert data["risk_mitigation"] == "Add code reviews."


def test_audit_makes_two_llm_calls() -> None:
    mock_provider = _mock_provider(["analysis", "mitigation"])
    with patch("src.entregable.ai_router.get_provider", return_value=mock_provider):
        client.post("/ai/tasks/audit", json=TASK_PAYLOAD)
    assert mock_provider.complete.call_count == 2


def test_audit_second_call_includes_risk_analysis() -> None:
    """The mitigation prompt must contain the risk analysis from the first call."""
    mock_provider = _mock_provider(["specific risk text", "mitigation plan"])
    with patch("src.entregable.ai_router.get_provider", return_value=mock_provider):
        client.post("/ai/tasks/audit", json=TASK_PAYLOAD)
    second_call_messages = mock_provider.complete.call_args_list[1][0][0]
    combined = " ".join(m["content"] for m in second_call_messages)
    assert "specific risk text" in combined


def test_audit_returns_502_on_first_call_error() -> None:
    mock = MagicMock()
    mock.complete.side_effect = RuntimeError("fail")
    with patch("src.entregable.ai_router.get_provider", return_value=mock):
        response = client.post("/ai/tasks/audit", json=TASK_PAYLOAD)
    assert response.status_code == 502

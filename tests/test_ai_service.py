"""Tests for the AI generation service."""
import json
from unittest.mock import MagicMock, patch

import pytest

from src.entregable.models import Priority, Status, UserStory
from src.entregable.schemas import UserStoryCreate
from src.entregable.services.ai_service import generate_tasks, generate_user_story

_STORY_JSON = {
    "project": "Portal",
    "role": "admin",
    "goal": "manage users",
    "reason": "reduce tickets",
    "description": "Full description.",
    "priority": "alta",
    "story_points": 5,
    "effort_hours": 8.0,
}

_TASK_JSON = [
    {
        "title": "Setup DB",
        "description": "Create schema.",
        "priority": "alta",
        "effort_hours": 4.0,
        "status": "pendiente",
        "assigned_to": None,
    }
]


def _mock_provider(reply: str) -> MagicMock:
    mock = MagicMock()
    mock.complete.return_value = reply
    return mock


def _dummy_story() -> UserStory:
    return UserStory(
        project="Portal",
        role="admin",
        goal="manage users",
        reason="reduce tickets",
        description="Full description.",
        priority=Priority.alta,
        story_points=5,
        effort_hours=8.0,
    )


class TestGenerateUserStory:
    def test_returns_user_story_create(self) -> None:
        with patch("src.entregable.services.ai_service.get_provider", return_value=_mock_provider(json.dumps(_STORY_JSON))):
            result = generate_user_story("Build a user portal")
        assert isinstance(result, UserStoryCreate)
        assert result.project == "Portal"

    def test_invalid_json_raises(self) -> None:
        with patch("src.entregable.services.ai_service.get_provider", return_value=_mock_provider("not json")):
            with pytest.raises(ValueError, match="invalid JSON"):
                generate_user_story("prompt")

    def test_schema_mismatch_raises(self) -> None:
        with patch("src.entregable.services.ai_service.get_provider", return_value=_mock_provider('{"foo": "bar"}')):
            with pytest.raises(ValueError, match="schema"):
                generate_user_story("prompt")


class TestGenerateTasks:
    def test_returns_list_of_task_create(self) -> None:
        with patch("src.entregable.services.ai_service.get_provider", return_value=_mock_provider(json.dumps(_TASK_JSON))):
            result = generate_tasks(_dummy_story())
        assert len(result) == 1
        assert result[0].title == "Setup DB"

    def test_non_array_raises(self) -> None:
        with patch("src.entregable.services.ai_service.get_provider", return_value=_mock_provider(json.dumps(_STORY_JSON))):
            with pytest.raises(ValueError, match="array"):
                generate_tasks(_dummy_story())

    def test_invalid_json_raises(self) -> None:
        with patch("src.entregable.services.ai_service.get_provider", return_value=_mock_provider("bad")):
            with pytest.raises(ValueError, match="invalid JSON"):
                generate_tasks(_dummy_story())

    def test_schema_mismatch_raises(self) -> None:
        bad = json.dumps([{"foo": "bar"}])
        with patch("src.entregable.services.ai_service.get_provider", return_value=_mock_provider(bad)):
            with pytest.raises(ValueError, match="schema"):
                generate_tasks(_dummy_story())

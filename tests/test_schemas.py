"""Tests for Pydantic schemas."""
import pytest
from pydantic import ValidationError

from src.entregable.models import Priority, Status
from src.entregable.schemas import TaskCreate, TaskSchema, UserStoryCreate, UserStorySchema

_STORY_DATA = {
    "project": "Portal",
    "role": "admin",
    "goal": "manage users",
    "reason": "reduce support tickets",
    "description": "Full description here.",
    "priority": "alta",
    "story_points": 5,
    "effort_hours": 8.0,
}

_TASK_DATA = {
    "title": "Implement endpoint",
    "description": "Full details.",
    "priority": "media",
    "effort_hours": 3.0,
}


class TestUserStoryCreate:
    def test_valid(self) -> None:
        us = UserStoryCreate(**_STORY_DATA)
        assert us.priority == Priority.alta
        assert us.story_points == 5

    def test_invalid_priority(self) -> None:
        with pytest.raises(ValidationError):
            UserStoryCreate(**{**_STORY_DATA, "priority": "urgente"})

    def test_story_points_below_range(self) -> None:
        with pytest.raises(ValidationError):
            UserStoryCreate(**{**_STORY_DATA, "story_points": 0})

    def test_story_points_above_range(self) -> None:
        with pytest.raises(ValidationError):
            UserStoryCreate(**{**_STORY_DATA, "story_points": 9})

    def test_effort_hours_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            UserStoryCreate(**{**_STORY_DATA, "effort_hours": 0})


class TestTaskCreate:
    def test_valid(self) -> None:
        task = TaskCreate(**_TASK_DATA)
        assert task.status == Status.pendiente
        assert task.assigned_to is None

    def test_invalid_priority(self) -> None:
        with pytest.raises(ValidationError):
            TaskCreate(**{**_TASK_DATA, "priority": "crítica"})

    def test_effort_hours_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            TaskCreate(**{**_TASK_DATA, "effort_hours": -1})

    def test_explicit_status(self) -> None:
        task = TaskCreate(**{**_TASK_DATA, "status": "completada"})
        assert task.status == Status.completada

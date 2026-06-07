"""Tests for SQLAlchemy models and domain enums."""
import pytest

from src.entregable.models import Priority, Status, Task, UserStory


class TestPriority:
    def test_all_values(self) -> None:
        assert [p.value for p in Priority] == ["baja", "media", "alta", "bloqueante"]

    def test_is_str(self) -> None:
        assert isinstance(Priority.alta, str)


class TestStatus:
    def test_all_values(self) -> None:
        assert [s.value for s in Status] == ["pendiente", "en progreso", "en revisión", "completada"]

    def test_is_str(self) -> None:
        assert isinstance(Status.pendiente, str)


class TestUserStoryModel:
    def test_instantiation(self) -> None:
        story = UserStory(
            project="Portal",
            role="admin",
            goal="manage users",
            reason="reduce tickets",
            description="Full description.",
            priority=Priority.alta,
            story_points=5,
            effort_hours=8.0,
        )
        assert story.project == "Portal"
        assert story.priority == Priority.alta

    def test_tasks_relationship_default_empty(self) -> None:
        story = UserStory(
            project="P", role="r", goal="g", reason="r2",
            description="d", priority=Priority.baja,
            story_points=1, effort_hours=1.0,
        )
        assert story.tasks == []


class TestTaskModel:
    def test_instantiation(self) -> None:
        task = Task(
            title="Do something",
            description="Details here.",
            priority=Priority.media,
            effort_hours=3.0,
            status=Status.pendiente,
            assigned_to="Ana",
            user_story_id=1,
        )
        assert task.title == "Do something"
        assert task.status == Status.pendiente
        assert task.assigned_to == "Ana"

    def test_assigned_to_optional(self) -> None:
        task = Task(
            title="T", description="D", priority=Priority.baja,
            effort_hours=1.0, status=Status.pendiente, user_story_id=1,
        )
        assert task.assigned_to is None

"""Tests for Flask MVC routes."""
from unittest.mock import patch

import pytest

from src.entregable.database import db
from src.entregable.models import Priority, Status, Task, UserStory
from src.entregable.schemas import TaskCreate, UserStoryCreate

_STORY_CREATE = UserStoryCreate(
    project="Portal",
    role="admin",
    goal="manage users",
    reason="reduce tickets",
    description="Full description.",
    priority=Priority.alta,
    story_points=5,
    effort_hours=8.0,
)

_TASK_CREATE = TaskCreate(
    title="Setup DB",
    description="Create schema.",
    priority=Priority.alta,
    effort_hours=4.0,
)


def _add_story(app) -> int:
    """Insert a UserStory and return its id."""
    with app.app_context():
        story = UserStory(**_STORY_CREATE.model_dump())
        db.session.add(story)
        db.session.commit()
        return story.id


def _add_task(app, story_id: int) -> None:
    """Insert a Task linked to story_id."""
    with app.app_context():
        task = Task(**_TASK_CREATE.model_dump(), user_story_id=story_id)
        db.session.add(task)
        db.session.commit()


class TestListUserStories:
    def test_returns_200(self, client) -> None:
        assert client.get("/user-stories").status_code == 200

    def test_shows_empty_message(self, client) -> None:
        response = client.get("/user-stories")
        assert b"No hay historias" in response.data

    def test_shows_story_in_list(self, app, client) -> None:
        _add_story(app)
        response = client.get("/user-stories")
        assert b"Portal" in response.data
        assert b"Generar tareas" in response.data


class TestCreateUserStory:
    def test_empty_prompt_redirects_with_error(self, client) -> None:
        response = client.post("/user-stories", data={"prompt": ""})
        assert response.status_code == 302

    def test_valid_prompt_creates_story(self, app, client) -> None:
        with patch("src.entregable.routes.user_stories.generate_user_story", return_value=_STORY_CREATE):
            response = client.post("/user-stories", data={"prompt": "Build a portal"})
        assert response.status_code == 302
        with app.app_context():
            assert db.session.execute(db.select(UserStory)).scalar() is not None

    def test_ai_error_redirects_with_flash(self, client) -> None:
        with patch("src.entregable.routes.user_stories.generate_user_story", side_effect=ValueError("LLM failed")):
            response = client.post("/user-stories", data={"prompt": "some prompt"})
        assert response.status_code == 302


class TestListTasks:
    def test_returns_200_for_existing_story(self, app, client) -> None:
        story_id = _add_story(app)
        assert client.get(f"/user-stories/{story_id}/tasks").status_code == 200

    def test_returns_404_for_missing_story(self, client) -> None:
        assert client.get("/user-stories/999/tasks").status_code == 404

    def test_shows_empty_message_when_no_tasks(self, app, client) -> None:
        story_id = _add_story(app)
        response = client.get(f"/user-stories/{story_id}/tasks")
        assert b"No hay tareas" in response.data

    def test_shows_tasks_in_list(self, app, client) -> None:
        story_id = _add_story(app)
        _add_task(app, story_id)
        response = client.get(f"/user-stories/{story_id}/tasks")
        assert b"Setup DB" in response.data


class TestGenerateStoryTasks:
    def test_returns_404_for_missing_story(self, client) -> None:
        assert client.post("/user-stories/999/generate-tasks").status_code == 404

    def test_creates_tasks_and_redirects(self, app, client) -> None:
        story_id = _add_story(app)
        with patch("src.entregable.routes.user_stories.generate_tasks", return_value=[_TASK_CREATE]):
            response = client.post(f"/user-stories/{story_id}/generate-tasks")
        assert response.status_code == 302

    def test_ai_error_redirects_with_flash(self, app, client) -> None:
        story_id = _add_story(app)
        with patch("src.entregable.routes.user_stories.generate_tasks", side_effect=ValueError("fail")):
            response = client.post(f"/user-stories/{story_id}/generate-tasks")
        assert response.status_code == 302

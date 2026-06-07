"""AI generation service for user stories and tasks."""
import json
import logging
from typing import Any

from pydantic import ValidationError

from src.entregable.models import UserStory
from src.entregable.providers import get_provider
from src.entregable.schemas import TaskCreate, UserStoryCreate

logger = logging.getLogger(__name__)

_USER_STORY_SYSTEM = """
You are a software project assistant. Given a prompt, generate a user story as a JSON object.
Respond with valid JSON only — no markdown, no explanation.

Required fields:
- project (string): project name inferred from the prompt
- role (string): user role (e.g. "registered user", "admin")
- goal (string): what the user wants to achieve
- reason (string): why the user needs it
- description (string): full user story narrative
- priority (string): one of baja, media, alta, bloqueante
- story_points (integer): 1 to 8
- effort_hours (number): estimated hours > 0
""".strip()

_TASKS_SYSTEM = """
You are a software project assistant. Given a user story, generate a list of development tasks as a JSON array.
Respond with valid JSON only — no markdown, no explanation.

Each task object must have:
- title (string)
- description (string): detailed explanation
- priority (string): one of baja, media, alta, bloqueante
- effort_hours (number): estimated hours > 0
- status (string): pendiente
- assigned_to (string or null)
""".strip()


def _call_llm(system: str, user: str) -> Any:
    """Call the LLM and parse the response as JSON."""
    raw = get_provider().complete([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ])
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("LLM returned invalid JSON: %s", raw)
        raise ValueError(f"LLM returned invalid JSON: {exc}") from exc


def generate_user_story(prompt: str) -> UserStoryCreate:
    """Generate and validate a user story from a free-text prompt."""
    data = _call_llm(_USER_STORY_SYSTEM, prompt)
    try:
        return UserStoryCreate(**data)
    except (ValidationError, TypeError) as exc:
        logger.error("User story validation failed: %s", exc)
        raise ValueError(f"LLM response does not match UserStory schema: {exc}") from exc


def generate_tasks(user_story: UserStory) -> list[TaskCreate]:
    """Generate and validate tasks for a given user story."""
    user_prompt = (
        f"Project: {user_story.project}\n"
        f"Role: {user_story.role}\n"
        f"Goal: {user_story.goal}\n"
        f"Reason: {user_story.reason}\n"
        f"Description: {user_story.description}\n"
        f"Priority: {user_story.priority.value}\n"
        f"Story points: {user_story.story_points}\n"
        f"Effort hours: {user_story.effort_hours}"
    )
    data = _call_llm(_TASKS_SYSTEM, user_prompt)
    if not isinstance(data, list):
        raise ValueError("LLM response for tasks must be a JSON array")
    try:
        return [TaskCreate(**item) for item in data]
    except (ValidationError, TypeError) as exc:
        logger.error("Task validation failed: %s", exc)
        raise ValueError(f"LLM response does not match Task schema: {exc}") from exc

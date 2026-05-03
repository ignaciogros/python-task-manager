"""Task persistence layer."""
import json
import logging
import os
from pathlib import Path

from src.entregable1.models import Task

logger = logging.getLogger(__name__)


def _tasks_file() -> Path:
    # Resolved at call time so tests can override TASKS_FILE via environment
    return Path(os.getenv("TASKS_FILE", "tasks.json"))


class TaskManager:
    """Manages loading and saving tasks to a JSON file."""

    @staticmethod
    def load_tasks() -> list[Task]:
        """Load all tasks from the JSON file."""
        path = _tasks_file()
        if not path.exists():
            # Missing file is not an error; the list is simply empty
            return []
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return [Task.from_dict(item) for item in data]
        except json.JSONDecodeError:
            logger.warning("Malformed JSON in %s; returning empty list", path)
            return []

    @staticmethod
    def save_tasks(tasks: list[Task]) -> None:
        """Save the task list to the JSON file."""
        path = _tasks_file()
        with path.open("w", encoding="utf-8") as f:
            # ensure_ascii=False preserves accented characters in status/description values
            json.dump([task.to_dict() for task in tasks], f, indent=2, ensure_ascii=False)

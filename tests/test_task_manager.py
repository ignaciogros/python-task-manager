"""Unit tests for TaskManager."""
import json

import pytest

from src.entregable1.models import Priority, Status, Task
from src.entregable1.task_manager import TaskManager


# Redirects TASKS_FILE to a temp path so tests never touch the real tasks.json
@pytest.fixture
def task_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    monkeypatch.setenv("TASKS_FILE", str(path))
    return path


@pytest.fixture
def sample_task() -> Task:
    return Task(
        title="Sample",
        description="Desc",
        priority=Priority.alta,
        effort_hours=2.0,
        status=Status.pendiente,
        assigned_to="Bob",
    )


def test_load_missing_file(task_file) -> None:
    # A missing file is a valid initial state; must return [] without raising
    assert TaskManager.load_tasks() == []


def test_load_malformed_json(task_file) -> None:
    # Corrupt file must not crash the app; warning is logged and [] is returned
    task_file.write_text("not valid json", encoding="utf-8")
    assert TaskManager.load_tasks() == []


def test_save_and_load_round_trip(task_file, sample_task) -> None:
    # Every field must survive a save → load cycle unchanged
    TaskManager.save_tasks([sample_task])
    assert TaskManager.load_tasks() == [sample_task]


def test_save_writes_valid_json(task_file, sample_task) -> None:
    # The file on disk must be a JSON array with the correct field values
    TaskManager.save_tasks([sample_task])
    data = json.loads(task_file.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert data[0]["title"] == "Sample"


def test_save_multiple_tasks(task_file, sample_task) -> None:
    tasks = [
        sample_task,
        Task(
            title="Second",
            description="Desc2",
            priority=Priority.baja,
            effort_hours=1.0,
            status=Status.completada,
            assigned_to="Eve",
        ),
    ]
    TaskManager.save_tasks(tasks)
    assert len(TaskManager.load_tasks()) == 2


def test_save_empty_list(task_file) -> None:
    # Saving an empty list must produce a readable empty array, not raise
    TaskManager.save_tasks([])
    assert TaskManager.load_tasks() == []

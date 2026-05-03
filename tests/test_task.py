"""Unit tests for the Task model."""
import pytest
from pydantic import ValidationError

from src.entregable1.models import Priority, Status, Task


# Shared valid payload; each test receives a fresh copy via the fixture
@pytest.fixture
def task_data() -> dict:
    return {
        "title": "Test task",
        "description": "A detailed description",
        "priority": "alta",
        "effort_hours": 3.5,
        "status": "pendiente",
        "assigned_to": "Ana",
    }


def test_task_creation(task_data: dict) -> None:
    # Verify fields are stored with the correct types after Pydantic coercion
    task = Task(**task_data)
    assert task.title == "Test task"
    assert task.priority == Priority.alta   # string "alta" is coerced to the enum member
    assert task.status == Status.pendiente
    assert task.id is not None              # id is auto-generated


def test_task_auto_id(task_data: dict) -> None:
    # Each instantiation must produce a unique id (UUID4 collision is astronomically unlikely)
    t1 = Task(**task_data)
    t2 = Task(**task_data)
    assert t1.id != t2.id


def test_to_dict_contains_all_fields(task_data: dict) -> None:
    # All seven model fields must appear in the serialized dictionary
    task = Task(**task_data)
    d = task.to_dict()
    for key in ("id", "title", "description", "priority", "effort_hours", "status", "assigned_to"):
        assert key in d


def test_to_dict_enum_values_are_strings(task_data: dict) -> None:
    # Enum members must serialize to plain strings so the dict is JSON-serializable
    task = Task(**task_data)
    d = task.to_dict()
    assert d["priority"] == "alta"
    assert d["status"] == "pendiente"


def test_round_trip(task_data: dict) -> None:
    # A task reconstructed from its own dict must equal the original
    task = Task(**task_data)
    assert Task.from_dict(task.to_dict()) == task


def test_invalid_priority(task_data: dict) -> None:
    # Values outside the Priority enum must be rejected at construction time
    task_data["priority"] = "urgente"
    with pytest.raises(ValidationError):
        Task(**task_data)


def test_invalid_status(task_data: dict) -> None:
    # Values outside the Status enum must be rejected at construction time
    task_data["status"] = "cancelada"
    with pytest.raises(ValidationError):
        Task(**task_data)


def test_effort_hours_decimal(task_data: dict) -> None:
    # effort_hours is a float; fractional values must be stored without truncation
    task_data["effort_hours"] = 1.25
    task = Task(**task_data)
    assert task.effort_hours == 1.25

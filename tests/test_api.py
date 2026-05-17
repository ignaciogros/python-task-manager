"""Integration tests for the Task API endpoints."""
import pytest
from fastapi.testclient import TestClient

from src.entregable.main import app

client = TestClient(app)

TASK_PAYLOAD = {
    "title": "Test task",
    "description": "Details",
    "priority": "media",
    "effort_hours": 2.5,
    "status": "pendiente",
    "assigned_to": "Ana",
}


# Isolates every test to its own empty tasks file
@pytest.fixture(autouse=True)
def isolated_tasks_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("TASKS_FILE", str(tmp_path / "tasks.json"))


def test_list_tasks_empty() -> None:
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task() -> None:
    response = client.post("/tasks/", json=TASK_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert "id" in data


def test_list_tasks_after_create() -> None:
    client.post("/tasks/", json=TASK_PAYLOAD)
    client.post("/tasks/", json=TASK_PAYLOAD)
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task() -> None:
    created = client.post("/tasks/", json=TASK_PAYLOAD).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_task_not_found() -> None:
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404


def test_update_task() -> None:
    created = client.post("/tasks/", json=TASK_PAYLOAD).json()
    updated_payload = {**TASK_PAYLOAD, "title": "Updated", "status": "completada"}
    response = client.put(f"/tasks/{created['id']}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["status"] == "completada"
    assert data["id"] == created["id"]  # id must not change on update


def test_update_task_not_found() -> None:
    response = client.put("/tasks/nonexistent-id", json=TASK_PAYLOAD)
    assert response.status_code == 404


def test_delete_task() -> None:
    created = client.post("/tasks/", json=TASK_PAYLOAD).json()
    assert client.delete(f"/tasks/{created['id']}").status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_task_not_found() -> None:
    response = client.delete("/tasks/nonexistent-id")
    assert response.status_code == 404

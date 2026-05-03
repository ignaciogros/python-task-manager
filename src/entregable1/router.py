"""Task CRUD router."""
from fastapi import APIRouter, HTTPException, status

from src.entregable1.models import Task
from src.entregable1.schemas import TaskCreate
from src.entregable1.task_manager import TaskManager

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[Task])
def list_tasks() -> list[Task]:
    """Return all tasks."""
    return TaskManager.load_tasks()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    """Return a single task by id."""
    for task in TaskManager.load_tasks():
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate) -> Task:
    """Create a new task and persist it."""
    task = Task(**body.model_dump())
    tasks = TaskManager.load_tasks()
    tasks.append(task)
    TaskManager.save_tasks(tasks)
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: str, body: TaskCreate) -> Task:
    """Replace an existing task's fields. Returns 404 if not found."""
    tasks = TaskManager.load_tasks()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            # Preserve the original id; replace all other fields
            updated = Task(id=task_id, **body.model_dump())
            tasks[i] = updated
            TaskManager.save_tasks(tasks)
            return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    """Delete a task by id. Returns 404 if not found."""
    tasks = TaskManager.load_tasks()
    remaining = [t for t in tasks if t.id != task_id]
    if len(remaining) == len(tasks):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    TaskManager.save_tasks(remaining)

"""Request body schemas for the tasks API."""
from pydantic import BaseModel

from src.entregable.models import Priority, Status


class TaskCreate(BaseModel):
    """Schema for task creation and full update requests (excludes auto-generated id)."""

    title: str
    description: str
    priority: Priority
    effort_hours: float
    status: Status
    assigned_to: str

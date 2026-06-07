"""Pydantic schemas for request validation and response serialization."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.entregable.models import Priority, Status


class UserStoryCreate(BaseModel):
    """Validates AI-generated user story data before DB persistence."""

    project: str
    role: str
    goal: str
    reason: str
    description: str
    priority: Priority
    story_points: int = Field(ge=1, le=8)
    effort_hours: float = Field(gt=0)


class UserStorySchema(BaseModel):
    """Full user story representation (DB → response)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project: str
    role: str
    goal: str
    reason: str
    description: str
    priority: Priority
    story_points: int
    effort_hours: float
    created_at: datetime


class UserStorySchemas(BaseModel):
    """List of user stories."""

    model_config = ConfigDict(from_attributes=True)

    items: list[UserStorySchema]


class TaskCreate(BaseModel):
    """Validates AI-generated task data before DB persistence."""

    title: str
    description: str
    priority: Priority
    effort_hours: float = Field(gt=0)
    status: Status = Status.pendiente
    assigned_to: Optional[str] = None


class TaskSchema(BaseModel):
    """Full task representation (DB → response)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: Priority
    effort_hours: float
    status: Status
    assigned_to: Optional[str]
    user_story_id: int
    created_at: datetime


class TaskSchemas(BaseModel):
    """List of tasks."""

    model_config = ConfigDict(from_attributes=True)

    items: list[TaskSchema]

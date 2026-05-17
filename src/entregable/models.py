"""Task domain model."""
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


# str + Enum makes Pydantic serialize the value as a plain string (e.g. "alta"), not "Priority.alta"
class Priority(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    bloqueante = "bloqueante"


class Status(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en progreso"   # internal name uses underscore; JSON value preserves the space
    en_revision = "en revisión"   # internal name is ASCII; JSON value keeps the accent
    completada = "completada"


class Task(BaseModel):
    """Represents a task assigned to a user."""

    # default_factory generates a new UUID per instance instead of sharing one across all instances
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    priority: Priority
    effort_hours: float
    status: Status
    assigned_to: str
    category: Optional[str] = None
    risk_analysis: Optional[str] = None
    risk_mitigation: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize the task to a plain dictionary."""
        # model_dump() resolves enums to their string values automatically
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize a task from a plain dictionary."""
        # cls(**data) lets Pydantic validate and coerce each field on construction
        return cls(**data)

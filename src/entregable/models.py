"""SQLAlchemy domain models."""
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum as SAEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.entregable.database import db


class Priority(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    bloqueante = "bloqueante"


class Status(str, enum.Enum):
    pendiente = "pendiente"
    en_progreso = "en progreso"
    en_revision = "en revisión"
    completada = "completada"


class UserStory(db.Model):
    """User story linked to one or more tasks."""

    __tablename__ = "user_stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    goal: Mapped[str] = mapped_column(String(500), nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[Priority] = mapped_column(SAEnum(Priority), nullable=False)
    story_points: Mapped[int] = mapped_column(Integer, nullable=False)
    effort_hours: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user_story", cascade="all, delete-orphan")


class Task(db.Model):
    """Task associated with a user story."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[Priority] = mapped_column(SAEnum(Priority), nullable=False)
    effort_hours: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[Status] = mapped_column(SAEnum(Status), nullable=False)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_story_id: Mapped[int] = mapped_column(ForeignKey("user_stories.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    user_story: Mapped["UserStory"] = relationship("UserStory", back_populates="tasks")

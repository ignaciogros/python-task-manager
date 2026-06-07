"""User stories and tasks MVC routes."""
import logging

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from src.entregable.database import db
from src.entregable.models import Task, UserStory
from src.entregable.services.ai_service import generate_tasks, generate_user_story

logger = logging.getLogger(__name__)

bp = Blueprint("user_stories", __name__)


@bp.get("/user-stories")
def list_user_stories():
    """Render all user stories with a prompt form."""
    stories = db.session.execute(db.select(UserStory).order_by(UserStory.created_at.desc())).scalars().all()
    return render_template("user-stories.html", stories=stories)


@bp.post("/user-stories")
def create_user_story():
    """Generate a user story from the submitted prompt and persist it."""
    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        flash("El prompt no puede estar vacío.", "danger")
        return redirect(url_for("user_stories.list_user_stories"))
    try:
        data = generate_user_story(prompt)
        story = UserStory(**data.model_dump())
        db.session.add(story)
        db.session.commit()
    except ValueError as exc:
        logger.error("User story generation failed: %s", exc)
        flash(f"Error al generar la historia de usuario: {exc}", "danger")
    return redirect(url_for("user_stories.list_user_stories"))


@bp.get("/user-stories/<int:story_id>/tasks")
def list_tasks(story_id: int):
    """Render tasks associated with a user story."""
    story = db.session.get(UserStory, story_id)
    if story is None:
        abort(404)
    tasks = db.session.execute(
        db.select(Task).where(Task.user_story_id == story_id).order_by(Task.created_at)
    ).scalars().all()
    return render_template("tasks.html", story=story, tasks=tasks)


@bp.post("/user-stories/<int:story_id>/generate-tasks")
def generate_story_tasks(story_id: int):
    """Generate and persist AI tasks for a user story, then redirect to task list."""
    story = db.session.get(UserStory, story_id)
    if story is None:
        abort(404)
    try:
        task_schemas = generate_tasks(story)
        for task_data in task_schemas:
            task = Task(**task_data.model_dump(), user_story_id=story_id)
            db.session.add(task)
        db.session.commit()
    except ValueError as exc:
        logger.error("Task generation failed: %s", exc)
        flash(f"Error al generar tareas: {exc}", "danger")
    return redirect(url_for("user_stories.list_tasks", story_id=story_id))

"""AI-powered task endpoints."""
import logging
import re

from fastapi import APIRouter, HTTPException, status

from src.entregable.models import Task
from src.entregable.providers import get_provider

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/tasks", tags=["ai"])


def _task_context(task: Task) -> str:
    """Format task fields as readable text for LLM prompts."""
    return (
        f"Title: {task.title}\n"
        f"Priority: {task.priority.value}\n"
        f"Status: {task.status.value}\n"
        f"Assigned to: {task.assigned_to}\n"
        f"Effort hours: {task.effort_hours}\n"
        f"Category: {task.category or 'N/A'}\n"
        f"Description: {task.description or 'N/A'}"
    )


def _call_llm(messages: list[dict[str, str]]) -> str:
    """Call the configured LLM provider; raise 502 on failure."""
    try:
        return get_provider().complete(messages)
    except Exception as exc:
        logger.error("LLM call failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM provider error: {exc}",
        ) from exc


@router.post("/describe", response_model=Task)
def describe_task(task: Task) -> Task:
    """Generate a description for a task whose description field is empty."""
    reply = _call_llm([
        {
            "role": "system",
            "content": (
                "You are a project management assistant. "
                "Write a concise task description (2-4 sentences) based on the provided task data. "
                "Reply with the description text only, no additional commentary."
            ),
        },
        {
            "role": "user",
            "content": f"Generate a description for this task:\n\n{_task_context(task)}",
        },
    ])
    return task.model_copy(update={"description": reply.strip()})


@router.post("/categorize", response_model=Task)
def categorize_task(task: Task) -> Task:
    """Classify a task into a category using the LLM."""
    reply = _call_llm([
        {
            "role": "system",
            "content": (
                "You are a project management assistant. "
                "Classify the task into exactly one of these categories: "
                "Frontend, Backend, Testing, Infra, Database, DevOps, Design, Documentation, Security, Other. "
                "Reply with the category name only, no additional text."
            ),
        },
        {
            "role": "user",
            "content": f"Classify this task:\n\n{_task_context(task)}",
        },
    ])
    return task.model_copy(update={"category": reply.strip()})


@router.post("/estimate", response_model=Task)
def estimate_task(task: Task) -> Task:
    """Estimate effort in hours for a task using the LLM."""
    reply = _call_llm([
        {
            "role": "system",
            "content": (
                "You are a software project estimation assistant. "
                "Estimate the effort required to complete the task in hours. "
                "Reply with a single positive number (integer or decimal). No units, no explanation."
            ),
        },
        {
            "role": "user",
            "content": f"Estimate the effort in hours for this task:\n\n{_task_context(task)}",
        },
    ])
    match = re.search(r"\d+(?:\.\d+)?", reply)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"LLM returned a non-numeric estimate: '{reply.strip()}'",
        )
    return task.model_copy(update={"effort_hours": float(match.group())})


@router.post("/audit", response_model=Task)
def audit_task(task: Task) -> Task:
    """Generate risk_analysis and risk_mitigation via two sequential LLM calls."""
    context = _task_context(task)

    risk_analysis = _call_llm([
        {
            "role": "system",
            "content": (
                "You are a project risk analyst. "
                "Identify the main risks associated with the given task. "
                "Be concise and specific. Reply with the risk analysis text only."
            ),
        },
        {
            "role": "user",
            "content": f"Identify the risks for this task:\n\n{context}",
        },
    ])

    risk_mitigation = _call_llm([
        {
            "role": "system",
            "content": (
                "You are a project risk analyst. "
                "Propose concrete mitigation actions for the provided risks. "
                "Reply with the mitigation plan text only."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Task details:\n\n{context}\n\n"
                f"Identified risks:\n{risk_analysis.strip()}\n\n"
                "Propose a mitigation plan for these risks."
            ),
        },
    ])

    return task.model_copy(update={
        "risk_analysis": risk_analysis.strip(),
        "risk_mitigation": risk_mitigation.strip(),
    })

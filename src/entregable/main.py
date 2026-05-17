"""FastAPI application entry point."""
from fastapi import FastAPI

from src.entregable.ai_router import router as ai_router
from src.entregable.router import router

app = FastAPI(
    title="Task Manager API",
    description="REST API for task management with JSON persistence and AI integrations.",
    version="2.0.0",
)

app.include_router(router)
app.include_router(ai_router)

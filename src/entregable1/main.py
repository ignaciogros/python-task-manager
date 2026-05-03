"""FastAPI application entry point."""
from fastapi import FastAPI

from src.entregable1.router import router

app = FastAPI(
    title="Task Manager API",
    description="REST API for task management with JSON persistence.",
    version="1.0.0",
)

app.include_router(router)

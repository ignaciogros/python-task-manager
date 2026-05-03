"""FastAPI application entry point."""
from fastapi import FastAPI

app = FastAPI(
    title="Task Manager API",
    description="REST API for task management with JSON persistence.",
    version="1.0.0",
)

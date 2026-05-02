# Task Management API

Multi-deliverable project building a task management API with AI integrations, containerisation, and cloud deployment.

## Objective

Develop a production-ready backend application that manages tasks assigned to users, evolving across five deliverables from a basic REST API to a fully deployed, AI-augmented cloud service.

## Phases

| # | Deliverable | Summary |
| :---: | :--- | :--- |
| 1 | **REST API** | FastAPI + JSON persistence. CRUD endpoints for `Task`. |
| 2 | **AI Endpoints** | LLM-powered endpoints for description generation, categorisation, effort estimation, and risk audit (Azure OpenAI / Anthropic). |
| 3 | **UI + Database** | Jinja2 interface, MySQL via SQLAlchemy, user story generation and task breakdown. |
| 4 | **Docker + CI/CD** | Dockerfile, GitHub Actions pipeline, image pushed to Docker Hub. |
| 5 | **Cloud Deployment** | Docker Compose, Azure Container Registry, Azure Container Apps, full CI/CD pipeline. |

## Project Structure

```
├── .agents/        # Agent role definitions (planner, architect, developer, reviewer)
├── instructions/   # Deliverable specifications
├── plans/          # Step-by-step implementation plans
├── prompts/        # Reusable prompt templates for agents
├── sessions/       # Conversation and decision log
├── skills/         # Reusable API interaction patterns
├── src/            # Application source code
└── tests/          # Test suites
```

## Stack

- **Framework:** FastAPI
- **Validation:** Pydantic
- **Testing:** pytest
- **Database (phase 3+):** MySQL + SQLAlchemy
- **AI (phase 2+):** Azure OpenAI / Anthropic
- **Infra (phase 4+):** Docker, GitHub Actions, Azure

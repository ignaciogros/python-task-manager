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

## Getting Started

> **All commands below assume a Bash-compatible shell.**
> On Windows, use **Git Bash** (not CMD or PowerShell) to avoid compatibility issues.

```bash
python -m venv venv
```

Activate the virtual environment:

| Terminal | Command |
|---|---|
| PowerShell | `venv\Scripts\Activate.ps1` |
| PowerShell (first time, if blocked) | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| CMD | `venv\Scripts\activate.bat` |
| Git Bash / WSL | `source venv/Scripts/activate` |
| macOS / Linux | `source venv/bin/activate` |

If activation succeeded, your prompt will show `(venv)` at the start of the line. If it does not appear, the environment is not active and commands will use the system Python.

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Validation by Phase

### Entregable 1 — REST API

**Step 2 — Project structure** ✅

```bash
uvicorn src.entregable1.main:app --reload
```

Open `http://127.0.0.1:8000/docs` — Swagger UI must load.

**Step 3 — Data model** ✅

```bash
pytest tests/test_task.py -v
```

All 8 tests must pass, including the round-trip `from_dict(task.to_dict()) == task`.

**Step 4 — Persistence (`TaskManager`)** ✅

```bash
pytest tests/test_task_manager.py -v
```

**Step 5 — API endpoints** ✅

```bash
pytest tests/ -v --cov=src/entregable1 --cov-report=term-missing
```

Coverage must be ≥ 80 %.

---

### Manual CRUD testing

Start the server first:

```bash
uvicorn src.entregable1.main:app --reload
```

#### Via Swagger UI (`http://127.0.0.1:8000/docs`)

1. Expand the endpoint you want to call and click **Try it out**.
2. Fill in the request body or parameters and click **Execute**.
3. The response (status code + JSON body) appears below.

Suggested sequence:
- `POST /tasks/` — create a task.
- `GET /tasks/` — confirm it appears in the list.
- `GET /tasks/{task_id}` — copy the `id` from the previous response and retrieve the task.
- `PUT /tasks/{task_id}` — update one or more fields (e.g. change `status` to `"completada"`).
- `DELETE /tasks/{task_id}` — delete it.
- `GET /tasks/{task_id}` — confirm it returns 404.

#### Via curl (Bash)

```bash
# Create a task — save the returned id for the commands below
curl -s -X POST http://127.0.0.1:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"My task","description":"Details","priority":"media","effort_hours":2.5,"status":"pendiente","assigned_to":"Ana"}'

# List all tasks
curl -s http://127.0.0.1:8000/tasks/

# Get a specific task  (replace <id> with the actual id)
curl -s http://127.0.0.1:8000/tasks/<id>

# Update a task
curl -s -X PUT http://127.0.0.1:8000/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated task","description":"New details","priority":"alta","effort_hours":4.0,"status":"completada","assigned_to":"Ana"}'

# Delete a task
curl -s -X DELETE http://127.0.0.1:8000/tasks/<id>

# Confirm deletion returns 404
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/tasks/<id>
```

### Entregable 2 — AI Endpoints

*To be completed.*

### Entregable 3 — UI + Database

*To be completed.*

### Entregable 4 — Docker

*To be completed.*

### Entregable 5 — Cloud Deployment

*To be completed.*

## Stack

- **Framework:** FastAPI
- **Validation:** Pydantic
- **Testing:** pytest
- **Database (phase 3+):** MySQL + SQLAlchemy
- **AI (phase 2+):** Azure OpenAI / Anthropic
- **Infra (phase 4+):** Docker, GitHub Actions, Azure

# Task Management API

> 🇪🇸 [Versión en español](README_es.md)

REST API for managing tasks assigned to users. Built with FastAPI and JSON file persistence.

## Features

- Full CRUD for tasks: create, list, retrieve, update, delete.
- Automatic request validation via Pydantic.
- Interactive API docs at `/docs` (Swagger UI).
- Configurable persistence path via environment variable.

## Installation

> **All commands assume a Bash-compatible shell.**
> On Windows, use **Git Bash** (not CMD or PowerShell).

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

If activation succeeded, your prompt will show `(venv)`. If it does not appear, the environment is not active and commands will use the system Python.

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Running

```bash
uvicorn src.entregable1.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

## Testing

Run the test suite with coverage:

```bash
pytest tests/ -v --cov=src/entregable1 --cov-report=term-missing
```

## Usage

### Swagger UI

Open `http://127.0.0.1:8000/docs` in your browser.

1. Expand an endpoint and click **Try it out**.
2. Fill in the request body or parameters and click **Execute**.
3. The response (status code + JSON body) appears below.

Suggested sequence to exercise the full CRUD:

- `POST /tasks/` — create a task.
- `GET /tasks/` — confirm it appears in the list.
- `GET /tasks/{task_id}` — retrieve the task by id.
- `PUT /tasks/{task_id}` — update fields (e.g. change `status` to `"completada"`).
- `DELETE /tasks/{task_id}` — delete it.
- `GET /tasks/{task_id}` — confirm it returns 404.

### curl

```bash
# Create a task — note the returned id for the commands below
curl -s -X POST http://127.0.0.1:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"My task","description":"Details","priority":"media","effort_hours":2.5,"status":"pendiente","assigned_to":"Ana"}'

# List all tasks
curl -s http://127.0.0.1:8000/tasks/

# Get a specific task (replace <id> with the actual id)
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

## Task fields

| Field | Type | Values |
|---|---|---|
| `title` | string | any |
| `description` | string | any |
| `priority` | string | `baja` · `media` · `alta` · `bloqueante` |
| `effort_hours` | float | estimated hours |
| `status` | string | `pendiente` · `en progreso` · `en revisión` · `completada` |
| `assigned_to` | string | assignee name |

## Roadmap

| # | Deliverable | Summary |
| :---: | :--- | :--- |
| 1 | **REST API** ✅ | FastAPI + JSON persistence. CRUD endpoints for `Task`. |
| 2 | **AI Endpoints** | LLM-powered endpoints: description generation, effort estimation, risk audit (Azure OpenAI / Anthropic). |
| 3 | **UI + Database** | Jinja2 interface, MySQL via SQLAlchemy, user story generation and task breakdown. |
| 4 | **Docker + CI/CD** | Dockerfile, GitHub Actions pipeline, image pushed to Docker Hub. |
| 5 | **Cloud Deployment** | Docker Compose, Azure Container Registry, Azure Container Apps, full CI/CD pipeline. |

## Distribution

Files included in the delivery package (`m2_proyecto_ignacio_gros.zip`):

| Path | Description |
|---|---|
| `src/` | Application source code |
| `tests/` | Test suite |
| `requirements.txt` | Pinned dependencies |
| `.env.example` | Environment variables template |
| `pytest.ini` | pytest configuration |
| `README.md` | English documentation |
| `README_es.md` | Spanish documentation |

## Stack

- **Framework:** FastAPI
- **Validation:** Pydantic
- **Testing:** pytest
- **Database (phase 3+):** MySQL + SQLAlchemy
- **AI (phase 2+):** Azure OpenAI / Anthropic
- **Infra (phase 4+):** Docker, GitHub Actions, Azure

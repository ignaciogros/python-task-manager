# Task Management API

> [Versión en español](README_es.md)

REST API for managing tasks assigned to users. Built with FastAPI, JSON file persistence, and LLM-powered AI endpoints.

## Features

- Full CRUD for tasks: create, list, retrieve, update, delete.
- Automatic request validation via Pydantic.
- Interactive API docs at `/docs` (Swagger UI).
- Configurable persistence path via environment variable.
- AI endpoints for description generation, categorisation, effort estimation, and risk auditing.
- Pluggable LLM provider: Azure OpenAI, Ollama (local), or any OpenAI-compatible endpoint.

## Installation

> **All commands must be run from the project root directory** (the folder that contains `requirements.txt`).
> **All commands assume a Bash-compatible shell.**
> On Windows, use **Git Bash** (not CMD or PowerShell).

```bash
python -m venv venv
```

Activate the virtual environment:

| Terminal | Command |
|---|---|
| Git Bash / WSL | `source venv/Scripts/activate` |
| macOS / Linux | `source venv/bin/activate` |

If activation succeeded, your prompt will show `(venv)`. If it does not appear, the environment is not active and commands will use the system Python.

```bash
pip install -r requirements.txt
cp .env.dist .env
```

Edit `.env` and fill in the LLM provider credentials (see [LLM configuration](#llm-configuration)).

## Running

```bash
uvicorn src.entregable.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

## Testing

Run the test suite with coverage:

```bash
pytest tests/ -v --cov=src/entregable --cov-report=term-missing
```

## LLM configuration

Set `PROVIDER` in `.env` to select the backend. Only the variables for the chosen provider are required.

### Azure OpenAI

```env
PROVIDER=azure
AZURE_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_API_KEY=<your-key>
AZURE_DEPLOYMENT=gpt-4o-mini
AZURE_API_VERSION=2024-02-01
```

### Ollama (local)

```env
PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### OpenAI-compatible endpoint (Qwen, Mistral-Small, …)

```env
PROVIDER=openai_compat
COMPAT_ENDPOINT=https://<your-endpoint>/v1
COMPAT_API_KEY=<your-key>
COMPAT_MODEL=<model-name>
```

## Usage

### Swagger UI

Open `http://127.0.0.1:8000/docs` in your browser.

1. Expand an endpoint and click **Try it out**.
2. Fill in the request body or parameters and click **Execute**.
3. The response (status code + JSON body) appears below.

### CRUD endpoints

Suggested sequence to exercise the full CRUD:

- `POST /tasks/` — create a task.
- `GET /tasks/` — confirm it appears in the list.
- `GET /tasks/{task_id}` — retrieve the task by id.
- `PUT /tasks/{task_id}` — update fields (e.g. change `status` to `"completada"`).
- `DELETE /tasks/{task_id}` — delete it.
- `GET /tasks/{task_id}` — confirm it returns 404.

### AI endpoints

All AI endpoints accept a full `Task` JSON body and return the same task with the AI-generated field(s) filled in.

| Method | Endpoint | Fills in |
|---|---|---|
| POST | `/ai/tasks/describe` | `description` |
| POST | `/ai/tasks/categorize` | `category` |
| POST | `/ai/tasks/estimate` | `effort_hours` |
| POST | `/ai/tasks/audit` | `risk_analysis` + `risk_mitigation` |

**Example — generate a description:**

```bash
curl -s -X POST http://127.0.0.1:8000/ai/tasks/describe \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement JWT authentication",
    "description": "",
    "priority": "alta",
    "effort_hours": 0,
    "status": "pendiente",
    "assigned_to": "Ana"
  }'
```

**Example — categorise a task:**

```bash
curl -s -X POST http://127.0.0.1:8000/ai/tasks/categorize \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Set up GitHub Actions pipeline",
    "description": "Create a CI workflow that runs tests on every push.",
    "priority": "media",
    "effort_hours": 3,
    "status": "pendiente",
    "assigned_to": "Carlos"
  }'
```

**Example — estimate effort:**

```bash
curl -s -X POST http://127.0.0.1:8000/ai/tasks/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design database schema",
    "description": "Model all entities for the task management system.",
    "priority": "alta",
    "effort_hours": 0,
    "status": "pendiente",
    "assigned_to": "Marta",
    "category": "Database"
  }'
```

**Example — risk audit:**

```bash
curl -s -X POST http://127.0.0.1:8000/ai/tasks/audit \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Migrate production database",
    "description": "Move all data from the legacy system to MySQL.",
    "priority": "bloqueante",
    "effort_hours": 8,
    "status": "pendiente",
    "assigned_to": "Luis",
    "category": "Database"
  }'
```

### curl — CRUD

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
| `description` | string | any (generated by `/ai/tasks/describe`) |
| `priority` | string | `baja` · `media` · `alta` · `bloqueante` |
| `effort_hours` | float | estimated hours (generated by `/ai/tasks/estimate`) |
| `status` | string | `pendiente` · `en progreso` · `en revisión` · `completada` |
| `assigned_to` | string | assignee name |
| `category` | string · optional | generated by `/ai/tasks/categorize` |
| `risk_analysis` | string · optional | generated by `/ai/tasks/audit` |
| `risk_mitigation` | string · optional | generated by `/ai/tasks/audit` |

## Roadmap

| # | Deliverable | Summary |
| :---: | :--- | :--- |
| 1 | **REST API** ✅ | FastAPI + JSON persistence. CRUD endpoints for `Task`. |
| 2 | **AI Endpoints** ✅ | LLM-powered endpoints: description generation, categorisation, effort estimation, risk audit. Pluggable provider (Azure OpenAI, Ollama, OpenAI-compatible). |
| 3 | **UI + Database** | Jinja2 interface, MySQL via SQLAlchemy. |
| 4 | **Docker + CI/CD** | Dockerfile, GitHub Actions pipeline, image pushed to Docker Hub. |
| 5 | **Cloud Deployment** | Docker Compose, Azure Container Registry, Azure Container Apps, full CI/CD pipeline. |

## Distribution

Files included in the delivery package (`m2_proyecto_ignacio_gros.zip`):

| Path | Description |
|---|---|
| `src/` | Application source code |
| `tests/` | Test suite |
| `requirements.txt` | Dependencies |
| `.env.dist` | Environment variables template |
| `pytest.ini` | pytest configuration |
| `conftest.py` | pytest root configuration (mock for optional dependencies) |
| `README.md` | English documentation |
| `README_es.md` | Spanish documentation |

## Stack

- **Framework:** FastAPI
- **Validation:** Pydantic
- **Testing:** pytest
- **LLM SDK:** openai (`pip install openai`)
- **Database (phase 3+):** MySQL + SQLAlchemy
- **Infra (phase 4+):** Docker, GitHub Actions, Azure

# Task Manager

> [Versión en español](README_es.md)

Web application for generating and managing user stories and tasks with AI assistance. Built with Flask, MySQL, SQLAlchemy, and Jinja2.

## Requirements

- Python 3.13
- MySQL 8+ (local or remote)
- An LLM provider: Azure OpenAI, Ollama, or any OpenAI-compatible endpoint

## Installation

### 1. Create and activate a virtual environment

**With uv (recommended):**

```bash
uv venv
```

| OS | Activate |
|----|----------|
| macOS / Linux | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `.venv\Scripts\activate.bat` |

**With pip:**

| OS | Create | Activate |
|----|--------|----------|
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Windows (PowerShell) | `python -m venv .venv` | `.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `python -m venv .venv` | `.venv\Scripts\activate.bat` |

### 2. Install dependencies

```bash
# uv
uv sync --group dev

# pip
pip install -r requirements.txt
```

### 3. Configure environment

```bash
# macOS / Linux
cp .env.dist .env

# Windows (PowerShell)
Copy-Item .env.dist .env
```

Edit `.env` and fill in:
- `DATABASE_URL` — MySQL connection string
- `SECRET_KEY` — any random string
- LLM provider credentials (see [LLM configuration](#llm-configuration))

### 4. Create the database

Create an empty database named `taskmanager` (or the name used in `DATABASE_URL`) in your MySQL server. The application creates the tables automatically on first run.

```sql
CREATE DATABASE taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Running

```bash
flask --app src.entregable.main run --debug
```

Open `http://127.0.0.1:5000/user-stories` in your browser.

## Testing

```bash
pytest
```

Coverage report is shown automatically (configured in `pytest.ini`).

## LLM configuration

Set `PROVIDER` in `.env`. Only the variables for the chosen provider are required.

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

### OpenAI-compatible endpoint

```env
PROVIDER=openai_compat
COMPAT_ENDPOINT=https://<your-endpoint>/v1
COMPAT_API_KEY=<your-key>
COMPAT_MODEL=<model-name>
```

## Usage

| URL | Action |
|-----|--------|
| `GET /user-stories` | List all user stories. Enter a prompt to generate a new one. |
| `GET /user-stories/<id>/tasks` | View tasks for a user story. |

From the user stories list:
1. Write a prompt describing the feature you need and click **Generar historia**.
2. Once the story appears, click **Ver tareas** to view existing tasks or **+ Generar** to generate new ones via AI.

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | Flask 3.1 |
| Database | MySQL 8 + SQLAlchemy 3 + PyMySQL |
| Validation | Pydantic 2 |
| Templates | Jinja2 + Bootstrap 5.3 |
| LLM SDK | openai |
| Testing | pytest + pytest-cov |

## Roadmap

| # | Deliverable | Status |
|:-:|-------------|--------|
| 1 | REST API — FastAPI + JSON persistence | ✅ |
| 2 | AI endpoints — description, categorisation, estimation, risk audit | ✅ |
| 3 | UI + Database — Flask, MySQL, Jinja2 | ✅ |
| 4 | Docker + CI/CD | — |
| 5 | Cloud deployment (Azure) | — |

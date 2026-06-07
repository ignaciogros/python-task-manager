# Task Manager

> [English version](README.md)

Aplicación web para generar y gestionar historias de usuario y tareas con asistencia de IA. Desarrollada con Flask, MySQL, SQLAlchemy y Jinja2.

## Requisitos

- Python 3.13
- MySQL 8+ (local o remoto)
- Proveedor LLM: Azure OpenAI, Ollama o cualquier endpoint compatible con OpenAI

## Instalación

### 1. Crear y activar entorno virtual

**Con uv (recomendado):**

```bash
uv venv
```

| Sistema operativo | Activar |
|-------------------|---------|
| macOS / Linux | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `.venv\Scripts\activate.bat` |

**Con pip:**

| Sistema operativo | Crear | Activar |
|-------------------|-------|---------|
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Windows (PowerShell) | `python -m venv .venv` | `.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `python -m venv .venv` | `.venv\Scripts\activate.bat` |

### 2. Instalar dependencias

```bash
# uv
uv sync --group dev

# pip
pip install -r requirements.txt
```

### 3. Configurar entorno

```bash
# macOS / Linux
cp .env.dist .env

# Windows (PowerShell)
Copy-Item .env.dist .env
```

Edita `.env` y rellena:
- `DATABASE_URL` — cadena de conexión MySQL
- `SECRET_KEY` — cadena aleatoria
- Credenciales del proveedor LLM (ver [Configuración del LLM](#configuración-del-llm))

### 4. Crear la base de datos

Crea una base de datos vacía en tu servidor MySQL. La aplicación crea las tablas automáticamente al arrancar.

```sql
CREATE DATABASE taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Ejecución

```bash
flask --app src.entregable.main run --debug
```

Abre `http://127.0.0.1:5000/user-stories` en el navegador.

## Tests

```bash
pytest
```

El informe de cobertura se muestra automáticamente (configurado en `pytest.ini`).

## Configuración del LLM

Establece `PROVIDER` en `.env`. Solo son necesarias las variables del proveedor elegido.

### Azure OpenAI

```env
PROVIDER=azure
AZURE_ENDPOINT=https://<tu-recurso>.openai.azure.com/
AZURE_API_KEY=<tu-clave>
AZURE_DEPLOYMENT=gpt-4o-mini
AZURE_API_VERSION=2024-02-01
```

### Ollama (local)

```env
PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### Endpoint compatible con OpenAI

```env
PROVIDER=openai_compat
COMPAT_ENDPOINT=https://<tu-endpoint>/v1
COMPAT_API_KEY=<tu-clave>
COMPAT_MODEL=<nombre-del-modelo>
```

## Uso

| URL | Acción |
|-----|--------|
| `GET /user-stories` | Lista todas las historias. Escribe un prompt para generar una nueva. |
| `GET /user-stories/<id>/tasks` | Ver tareas de una historia. |

Desde el listado de historias:
1. Escribe un prompt describiendo la funcionalidad y pulsa **Generar historia**.
2. Una vez creada la historia, pulsa **Ver tareas** para ver las tareas existentes o **+ Generar** para generarlas con IA.

## Stack

| Capa | Tecnología |
|------|-----------|
| Framework | Flask 3.1 |
| Base de datos | MySQL 8 + SQLAlchemy 3 + PyMySQL |
| Validación | Pydantic 2 |
| Templates | Jinja2 + Bootstrap 5.3 |
| SDK LLM | openai |
| Tests | pytest + pytest-cov |

## Roadmap

| # | Entregable | Estado |
|:-:|------------|--------|
| 1 | REST API — FastAPI + persistencia JSON | ✅ |
| 2 | Endpoints IA — descripción, categorización, estimación, auditoría | ✅ |
| 3 | UI + Base de datos — Flask, MySQL, Jinja2 | ✅ |
| 4 | Docker + CI/CD | — |
| 5 | Despliegue en Azure | — |

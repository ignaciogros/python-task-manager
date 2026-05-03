# API de Gestión de Tareas

> [English version](README.md)

API REST para gestionar tareas asignadas a usuarios. Desarrollada con FastAPI y persistencia en fichero JSON.

## Funcionalidades

- CRUD completo de tareas: crear, listar, consultar, actualizar, eliminar.
- Validación automática de peticiones mediante Pydantic.
- Documentación interactiva en `/docs` (Swagger UI).
- Ruta de persistencia configurable por variable de entorno.

## Instalación

> **Todos los comandos deben ejecutarse desde la raíz del proyecto** (la carpeta que contiene `requirements.txt`).
> **Todos los comandos asumen una terminal compatible con Bash.**
> En Windows, usa **Git Bash** (no CMD ni PowerShell).

```bash
python -m venv venv
```

Activa el entorno virtual:

| Terminal | Comando |
|---|---|
| PowerShell | `venv\Scripts\Activate.ps1` |
| PowerShell (primera vez, si está bloqueado) | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| CMD | `venv\Scripts\activate.bat` |
| Git Bash / WSL | `source venv/Scripts/activate` |
| macOS / Linux | `source venv/bin/activate` |

Si la activación fue correcta, verás `(venv)` al inicio de la línea. Si no aparece, el entorno no está activo y los comandos usarán el Python del sistema.

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Ejecución

```bash
uvicorn src.entregable1.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Tests

Ejecuta la suite de tests con cobertura:

```bash
pytest tests/ -v --cov=src/entregable1 --cov-report=term-missing
```

## Uso

### Swagger UI

Abre `http://127.0.0.1:8000/docs` en el navegador.

1. Despliega el endpoint que quieras probar y haz clic en **Try it out**.
2. Rellena el cuerpo de la petición o los parámetros y haz clic en **Execute**.
3. La respuesta (código de estado + cuerpo JSON) aparece a continuación.

Secuencia sugerida para probar el CRUD completo:

- `POST /tasks/` — crear una tarea.
- `GET /tasks/` — confirmar que aparece en el listado.
- `GET /tasks/{task_id}` — consultar la tarea por id.
- `PUT /tasks/{task_id}` — actualizar campos (p. ej. cambiar `status` a `"completada"`).
- `DELETE /tasks/{task_id}` — eliminarla.
- `GET /tasks/{task_id}` — confirmar que devuelve 404.

### curl

```bash
# Crear una tarea — anota el id devuelto para los comandos siguientes
curl -s -X POST http://127.0.0.1:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Mi tarea","description":"Detalles","priority":"media","effort_hours":2.5,"status":"pendiente","assigned_to":"Ana"}'

# Listar todas las tareas
curl -s http://127.0.0.1:8000/tasks/

# Consultar una tarea concreta (sustituye <id> por el id real)
curl -s http://127.0.0.1:8000/tasks/<id>

# Actualizar una tarea
curl -s -X PUT http://127.0.0.1:8000/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"title":"Tarea actualizada","description":"Nuevos detalles","priority":"alta","effort_hours":4.0,"status":"completada","assigned_to":"Ana"}'

# Eliminar una tarea
curl -s -X DELETE http://127.0.0.1:8000/tasks/<id>

# Confirmar que la eliminación devuelve 404
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/tasks/<id>
```

## Campos de una tarea

| Campo | Tipo | Valores |
|---|---|---|
| `title` | cadena | cualquiera |
| `description` | cadena | cualquiera |
| `priority` | cadena | `baja` · `media` · `alta` · `bloqueante` |
| `effort_hours` | decimal | horas estimadas |
| `status` | cadena | `pendiente` · `en progreso` · `en revisión` · `completada` |
| `assigned_to` | cadena | nombre del responsable |

## Hoja de ruta

| # | Entregable | Resumen |
| :---: | :--- | :--- |
| 1 | **API REST** ✅ | FastAPI + persistencia JSON. Endpoints CRUD para `Task`. |
| 2 | **Endpoints IA** | Endpoints con LLM: generación de descripciones, estimación de esfuerzo, auditoría de riesgos (Azure OpenAI / Anthropic). |
| 3 | **UI + Base de datos** | Interfaz Jinja2, MySQL con SQLAlchemy, generación de historias de usuario y desglose de tareas. |
| 4 | **Docker + CI/CD** | Dockerfile, pipeline de GitHub Actions, imagen publicada en Docker Hub. |
| 5 | **Despliegue en la nube** | Docker Compose, Azure Container Registry, Azure Container Apps, pipeline CI/CD completo. |

## Distribución

Ficheros incluidos en el paquete de entrega (`m2_proyecto_ignacio_gros.zip`):

| Ruta | Descripción |
|---|---|
| `src/` | Código fuente de la aplicación |
| `tests/` | Suite de tests |
| `requirements.txt` | Dependencias con versiones fijadas |
| `.env.example` | Plantilla de variables de entorno |
| `pytest.ini` | Configuración de pytest |
| `README.md` | Documentación en inglés |
| `README_es.md` | Documentación en español |

## Stack tecnológico

- **Framework:** FastAPI
- **Validación:** Pydantic
- **Tests:** pytest
- **Base de datos (fase 3+):** MySQL + SQLAlchemy
- **IA (fase 2+):** Azure OpenAI / Anthropic
- **Infraestructura (fase 4+):** Docker, GitHub Actions, Azure

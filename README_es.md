# API de Gestión de Tareas

> [English version](README.md)

API REST para gestionar tareas asignadas a usuarios. Desarrollada con FastAPI, persistencia en fichero JSON y endpoints de IA mediante LLMs.

## Funcionalidades

- CRUD completo de tareas: crear, listar, consultar, actualizar, eliminar.
- Validación automática de peticiones mediante Pydantic.
- Documentación interactiva en `/docs` (Swagger UI).
- Ruta de persistencia configurable por variable de entorno.
- Endpoints de IA para generar descripciones, categorizar, estimar esfuerzo y auditar riesgos.
- Proveedor de LLM intercambiable: Azure OpenAI, Ollama (local) o cualquier endpoint compatible con OpenAI.

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
| Git Bash / WSL | `source venv/Scripts/activate` |
| macOS / Linux | `source venv/bin/activate` |

Si la activación fue correcta, verás `(venv)` al inicio de la línea. Si no aparece, el entorno no está activo y los comandos usarán el Python del sistema.

```bash
pip install -r requirements.txt
cp .env.dist .env
```

Edita `.env` y rellena las credenciales del proveedor LLM (ver [Configuración del LLM](#configuración-del-llm)).

## Ejecución

```bash
uvicorn src.entregable.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Tests

Ejecuta la suite de tests con cobertura:

```bash
pytest tests/ -v --cov=src/entregable --cov-report=term-missing
```

## Configuración del LLM

Establece `PROVIDER` en `.env` para seleccionar el backend. Solo son obligatorias las variables del proveedor elegido.

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

### Endpoint compatible con OpenAI (Qwen, Mistral-Small, …)

```env
PROVIDER=openai_compat
COMPAT_ENDPOINT=https://<tu-endpoint>/v1
COMPAT_API_KEY=<tu-clave>
COMPAT_MODEL=<nombre-del-modelo>
```

## Uso

### Swagger UI

Abre `http://127.0.0.1:8000/docs` en el navegador.

1. Despliega el endpoint que quieras probar y haz clic en **Try it out**.
2. Rellena el cuerpo de la petición o los parámetros y haz clic en **Execute**.
3. La respuesta (código de estado + cuerpo JSON) aparece a continuación.

### Endpoints CRUD

Secuencia sugerida para probar el CRUD completo:

- `POST /tasks/` — crear una tarea.
- `GET /tasks/` — confirmar que aparece en el listado.
- `GET /tasks/{task_id}` — consultar la tarea por id.
- `PUT /tasks/{task_id}` — actualizar campos (p. ej. cambiar `status` a `"completada"`).
- `DELETE /tasks/{task_id}` — eliminarla.
- `GET /tasks/{task_id}` — confirmar que devuelve 404.

### Endpoints de IA

Todos los endpoints de IA aceptan un cuerpo JSON con la tarea completa y devuelven la misma tarea con el campo generado por IA relleno.

| Método | Endpoint | Rellena |
|---|---|---|
| POST | `/ai/tasks/describe` | `description` |
| POST | `/ai/tasks/categorize` | `category` |
| POST | `/ai/tasks/estimate` | `effort_hours` |
| POST | `/ai/tasks/audit` | `risk_analysis` + `risk_mitigation` |

**Ejemplo — generar descripción:**

```bash
curl -s -X POST http://127.0.0.1:8000/ai/tasks/describe \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar autenticación JWT",
    "description": "",
    "priority": "alta",
    "effort_hours": 0,
    "status": "pendiente",
    "assigned_to": "Ana"
  }'
```

**Ejemplo — categorizar una tarea:**

```bash
curl -s -X POST http://127.0.0.1:8000/ai/tasks/categorize \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Configurar pipeline de GitHub Actions",
    "description": "Crear un workflow de CI que ejecute los tests en cada push.",
    "priority": "media",
    "effort_hours": 3,
    "status": "pendiente",
    "assigned_to": "Carlos"
  }'
```

**Ejemplo — estimar esfuerzo:**

```bash
curl -s -X POST http://127.0.0.1:8000/ai/tasks/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Diseñar esquema de base de datos",
    "description": "Modelar todas las entidades del sistema de gestión de tareas.",
    "priority": "alta",
    "effort_hours": 0,
    "status": "pendiente",
    "assigned_to": "Marta",
    "category": "Database"
  }'
```

**Ejemplo — auditoría de riesgos:**

```bash
curl -s -X POST http://127.0.0.1:8000/ai/tasks/audit \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Migrar base de datos de producción",
    "description": "Mover todos los datos del sistema legacy a MySQL.",
    "priority": "bloqueante",
    "effort_hours": 8,
    "status": "pendiente",
    "assigned_to": "Luis",
    "category": "Database"
  }'
```

### curl — CRUD

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
| `description` | cadena | cualquiera (generado por `/ai/tasks/describe`) |
| `priority` | cadena | `baja` · `media` · `alta` · `bloqueante` |
| `effort_hours` | decimal | horas estimadas (generado por `/ai/tasks/estimate`) |
| `status` | cadena | `pendiente` · `en progreso` · `en revisión` · `completada` |
| `assigned_to` | cadena | nombre del responsable |
| `category` | cadena · opcional | generado por `/ai/tasks/categorize` |
| `risk_analysis` | cadena · opcional | generado por `/ai/tasks/audit` |
| `risk_mitigation` | cadena · opcional | generado por `/ai/tasks/audit` |

## Hoja de ruta

| # | Entregable | Resumen |
| :---: | :--- | :--- |
| 1 | **API REST** ✅ | FastAPI + persistencia JSON. Endpoints CRUD para `Task`. |
| 2 | **Endpoints IA** ✅ | Endpoints con LLM: generación de descripciones, categorización, estimación de esfuerzo, auditoría de riesgos. Proveedor intercambiable (Azure OpenAI, Ollama, compatible con OpenAI). |
| 3 | **UI + Base de datos** | Interfaz Jinja2, MySQL con SQLAlchemy. |
| 4 | **Docker + CI/CD** | Dockerfile, pipeline de GitHub Actions, imagen publicada en Docker Hub. |
| 5 | **Despliegue en la nube** | Docker Compose, Azure Container Registry, Azure Container Apps, pipeline CI/CD completo. |

## Distribución

Ficheros incluidos en el paquete de entrega (`m2_proyecto_ignacio_gros.zip`):

| Ruta | Descripción |
|---|---|
| `src/` | Código fuente de la aplicación |
| `tests/` | Suite de tests |
| `requirements.txt` | Dependencias |
| `.env.dist` | Plantilla de variables de entorno |
| `pytest.ini` | Configuración de pytest |
| `conftest.py` | Configuración raíz de pytest (mock para dependencias opcionales) |
| `README.md` | Documentación en inglés |
| `README_es.md` | Documentación en español |

## Stack tecnológico

- **Framework:** FastAPI
- **Validación:** Pydantic
- **Tests:** pytest
- **SDK LLM:** openai (`pip install openai`)
- **Base de datos (fase 3+):** MySQL + SQLAlchemy
- **Infraestructura (fase 4+):** Docker, GitHub Actions, Azure

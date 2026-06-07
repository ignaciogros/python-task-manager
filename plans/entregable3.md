# Plan — Entregable 3

## Decisiones
- Framework: Flask (reemplaza FastAPI)
- DB: MySQL local via SQLAlchemy + PyMySQL
- CSS: Bootstrap local (sin CDN)
- Módulo: src/entregable/ (refactorizado)

## Fases

### Fase 1 — Dependencias y configuración [x]
- [x] requirements.txt: quitar FastAPI/uvicorn, añadir Flask, Flask-SQLAlchemy, PyMySQL
- [x] .env.dist: añadir DATABASE_URL
- [x] Descargar Bootstrap (CSS + JS bundle) a src/entregable/static/

#### Pruebas Fase 1
```powershell
# 1. Crear y activar entorno virtual
uv venv C:\ruta\a\tu\entorno
C:\ruta\a\tu\entorno\Scripts\activate

# 2. Instalar dependencias
uv sync --group dev
# o: pip install -r requirements.txt

# 3. Verificar Bootstrap
Test-Path src\entregable\static\css\bootstrap.min.css
Test-Path src\entregable\static\js\bootstrap.bundle.min.js

# 4. Copiar y editar .env
Copy-Item .env.dist .env
# Ajustar DATABASE_URL con tus credenciales MySQL
```

### Fase 2 — Modelos SQLAlchemy [x]
- [x] database.py: instancia SQLAlchemy (db) con DeclarativeBase
- [x] models.py: UserStory (id, project, role, goal, reason, description, priority, story_points, effort_hours, created_at)
- [x] models.py: Task (id, title, description, priority, effort_hours, status, assigned_to, user_story_id FK, created_at)
- [x] Eliminado modelo Pydantic Task que actuaba como dominio+persistencia (antipatrón)
      Pydantic permanece como capa de validación/serialización (Fase 3)
      Flujo: Request → Pydantic schema → SQLAlchemy model → Pydantic schema → Response

#### Pruebas Fase 2
```powershell
# Con entorno activo, desde raíz del proyecto:
python -c "from src.entregable.models import UserStory, Task, Priority, Status; print('OK')"
```

### Fase 3 — Schemas Pydantic [x]
- [x] schemas.py: UserStorySchema, UserStorySchemas, TaskSchema, TaskSchemas
- [x] schemas.py: UserStoryCreate, TaskCreate (validan salida del LLM antes de persistir)

#### Pruebas Fase 3
```powershell
# Con entorno activo, desde raíz del proyecto:
python -c "from src.entregable.schemas import UserStorySchema, UserStorySchemas, TaskSchema, TaskSchemas, UserStoryCreate, TaskCreate; print('OK')"
```

### Fase 4 — Servicio AI [ ]
- [ ] services/ai_service.py: generate_user_story(prompt) -> UserStory
- [ ] services/ai_service.py: generate_tasks(user_story) -> list[Task]
- [ ] Reutilizar providers/ existente; pedir JSON estructurado al LLM

### Fase 5 — Flask app y rutas [ ]
- [ ] __init__.py: create_app() con SQLAlchemy
- [ ] routes/user_stories.py: Blueprint con 4 endpoints
  - GET  /user-stories
  - POST /user-stories
  - GET  /user-stories/<id>/tasks
  - POST /user-stories/<id>/generate-tasks
- [ ] main.py: punto de entrada Flask

### Fase 6 — Templates Jinja2 [ ]
- [ ] templates/base.html: layout con Bootstrap
- [ ] templates/user-stories.html: listado + textarea prompt + botón "Generar tareas"
- [ ] templates/tasks.html: listado de tareas de una historia

### Fase 7 — Tests [ ]
- [ ] Eliminar tests FastAPI
- [ ] Añadir tests con Flask test client
- [ ] Mantener cobertura >= 80%

### Fase 8 — Limpieza y README [ ]
- [ ] Eliminar: task_manager.py, router.py, ai_router.py
- [ ] Actualizar README.md

## Archivos eliminados
- src/entregable/task_manager.py
- src/entregable/router.py
- src/entregable/ai_router.py

## Estructura nueva
- src/entregable/routes/
- src/entregable/services/
- src/entregable/templates/
- src/entregable/static/

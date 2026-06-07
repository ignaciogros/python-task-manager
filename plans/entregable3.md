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
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Verificar Bootstrap descargado
ls src/entregable/static/css/bootstrap.min.css
ls src/entregable/static/js/bootstrap.bundle.min.js

# 3. Copiar y editar .env
cp .env.dist .env
# Editar .env: ajustar DATABASE_URL con tus credenciales MySQL
```

### Fase 2 — Modelos SQLAlchemy [ ]
- [ ] models.py: UserStory (id, project, role, goal, reason, description, priority, story_points, effort_hours, created_at)
- [ ] models.py: Task (id, title, description, priority, effort_hours, status, assigned_to, user_story_id FK, created_at)
- [ ] Eliminar modelo Pydantic Task actual

### Fase 3 — Schemas Pydantic [ ]
- [ ] schemas.py: UserStorySchema, UserStorySchemas, TaskSchema, TaskSchemas

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

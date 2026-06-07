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

### Fase 4 — Servicio AI [x]
- [x] services/ai_service.py: generate_user_story(prompt) -> UserStoryCreate
- [x] services/ai_service.py: generate_tasks(user_story) -> list[TaskCreate]
- [x] Reutiliza providers/ existente; pide JSON puro al LLM y valida con Pydantic

#### Pruebas Fase 4
```powershell
# Con entorno activo, desde raíz del proyecto:
# 1. Verificar importación
python -c "from src.entregable.services.ai_service import generate_user_story, generate_tasks; print('OK')"

# 2. Prueba real (requiere .env con proveedor LLM válido) — guardar como test_ai_service.py y ejecutar:
#    from dotenv import load_dotenv; load_dotenv()
#    from src.entregable.services.ai_service import generate_user_story
#    us = generate_user_story("Sistema de reservas de salas de reuniones")
#    print(us.model_dump())
python test_ai_service.py
```

### Fase 5 — Flask app y rutas [x]
- [x] __init__.py: create_app() con SQLAlchemy, blueprint registrado, db.create_all()
- [x] routes/user_stories.py: Blueprint con 4 endpoints
  - GET  /user-stories
  - POST /user-stories
  - GET  /user-stories/<id>/tasks
  - POST /user-stories/<id>/generate-tasks
- [x] main.py: punto de entrada Flask (load_dotenv + create_app)

#### Pruebas Fase 5
```powershell
# Requiere MySQL corriendo y DATABASE_URL configurado en .env

# 1. Arrancar la app
flask --app src.entregable.main run --debug

# 2. Verificar en navegador:
#    http://127.0.0.1:5000/user-stories  → debe responder (aunque plantilla no existe aún)
#    Los logs deben mostrar que las tablas se crean en MySQL
```

### Fase 6 — Templates Jinja2 [x]
- [x] templates/base.html: navbar, flash messages, bloques title/content
- [x] templates/user-stories.html: formulario prompt + tabla de historias + botón "Generar tareas"
- [x] templates/tasks.html: cabecera con historia + tabla de tareas + enlace volver

#### Pruebas Fase 6
```powershell
# Requiere MySQL corriendo y .env configurado
flask --app src.entregable.main run --debug

# Verificar en navegador:
# http://127.0.0.1:5000/user-stories        → lista vacía + formulario
# Enviar prompt → genera historia y redirige
# Botón "Generar tareas" → genera tareas y redirige a /user-stories/{id}/tasks
```

### Fase 7 — Tests [x]
- [x] Eliminados: test_api.py, test_task.py, test_task_manager.py, test_ai.py
- [x] Conservado: test_providers.py (providers no cambiaron)
- [x] Creados: conftest.py, test_models.py, test_schemas.py, test_ai_service.py, test_routes.py
- [x] create_app() actualizado para aceptar test_config (SQLite in-memory)

#### Pruebas Fase 7
```powershell
# Con entorno activo, desde raíz del proyecto:
pytest
# Los parámetros de los tests están en pytest.ini
```

### Fase 8 — UI/UX (frontend-design) [x]
- [x] static/css/custom.css: tokens de diseño, navbar, tablas, badges, spinner, empty state
- [x] static/js/custom.js: loading state en formularios AI (spinner + disabled)
- [x] base.html: navbar clara, flash accesible, custom.css/js incluidos
- [x] user-stories.html: formulario con prompt-area, tabla con badges propios, conteo dinámico
- [x] tasks.html: story header con narrativa, tabla de tareas, descripción truncada con title

#### Pruebas Fase 8
```powershell
# Con MySQL corriendo y .env configurado:
flask --app src.entregable.main run --debug

# Verificar en navegador:
# http://127.0.0.1:5000/user-stories
# - Fondo cálido, navbar blanca con borde, tipografía serif en título
# - Formulario con textarea grande y botón oscuro
# - Botón "Generar historia" muestra spinner mientras genera
# - Tabla con badges de color por prioridad
# - Botón "Generar tareas" muestra spinner mientras genera
# - http://127.0.0.1:5000/user-stories/{id}/tasks → cabecera historia + tabla tareas
```

### Fase 9 — Limpieza y README [x]
- [x] Eliminados: task_manager.py, router.py, ai_router.py (adelantado en Fase 7)
- [x] README.md y README_es.md actualizados: instrucciones multi-OS, uv y pip

#### Pruebas Fase 9
```powershell
# Verificar que el README es correcto siguiendo sus propias instrucciones de instalación
```

## Archivos eliminados
- src/entregable/task_manager.py
- src/entregable/router.py
- src/entregable/ai_router.py

## Estructura nueva
- src/entregable/routes/
- src/entregable/services/
- src/entregable/templates/
- src/entregable/static/

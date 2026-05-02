# Proyecto: Entregable 3

## Objetivos
El objetivo de este entregable es completar el desarrollo de la aplicación con interfaz de usuario y base de datos. Se conectará la aplicación Flask a una base de datos relacional MySQL y se utilizarán salidas estructuradas de IA para almacenar resultados y mostrarlos a través de la interfaz de usuario.

## Pautas de elaboración

### 1. Arquitectura del Proyecto
Crea una aplicación Flask dividida en múltiples archivos que incluya conexión a base de datos MySQL, local o en Azure.

### 2. Modelos SQLAlchemy

**Modelo `UserStory`:**
*   **id**: Clave primaria.
*   **project**: Nombre del proyecto.
*   **role**: Rol del usuario en la historia.
*   **goal**: Objetivo de la historia de usuario.
*   **reason**: Razón de la historia de usuario.
*   **description**: Texto largo que describe en qué consiste toda la historia de usuario.
*   **priority**: Niveles: baja, media, alta, bloqueante.
*   **story_points**: Puntos de historia estimados (1–8).
*   **effort_hours**: Número decimal, horas estimadas para completar la historia.
*   **created_at**: Fecha de creación, generada automáticamente a nivel de base de datos.
*   Se pueden agregar más campos.

**Modelo `Task`:**
*   **id**: Clave primaria.
*   **title**: Título de la tarea.
*   **description**: Texto largo que describe completamente la tarea.
*   **priority**: Niveles: baja, media, alta, bloqueante.
*   **effort_hours**: Número decimal, horas estimadas para completar la tarea.
*   **status**: Estados: pendiente, en progreso, en revisión, completada.
*   **assigned_to**: String con el nombre de la persona asignada.
*   **user_story_id**: Asociación many-to-one con `UserStory`.
*   **created_at**: Fecha de creación, generada automáticamente a nivel de base de datos.
*   Se pueden agregar más campos.

### 3. Schemas con Pydantic
*   `UserStorySchema`
*   `UserStorySchemas`
*   `TaskSchema`
*   `TaskSchemas`

### 4. Endpoints MVC

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| **GET** | `/user-stories` | Devuelve `user-stories.html` con el listado de todas las historias de usuario y un `textarea` para escribir un prompt y solicitar la generación de nuevas historias. Cada historia incluye un botón **«Generar tareas»**. |
| **POST** | `/user-stories` | Recibe el formulario de `user-stories.html`, extrae el prompt y lo usa para generar una historia de usuario completa con IA, almacenándola en la base de datos. |
| **POST** | `/user-stories/{id}/generate-tasks` | Invocado al pulsar **«Generar tareas»** sobre una historia de usuario. Genera las tareas asociadas usando IA, las almacena en base de datos vinculadas a la historia y redirige a `GET /user-stories/{id}/tasks`. |
| **GET** | `/user-stories/{id}/tasks` | Devuelve `tasks.html` con el listado de tareas asociadas a la historia de usuario indicada. |

## Extensión y formato
Entrega un archivo `m4_proyecto_nombre_apellido.zip` que contenga una carpeta con el proyecto Flask y los archivos Python y HTML necesarios.

## Rúbrica de evaluación

| Criterio | Descripción | Puntuación Máxima | Peso |
| :--- | :--- | :---: | :---: |
| **Modelos y base de datos** | Modelos SQLAlchemy, schemas Pydantic y conexión a base de datos relacional. | 2 | 20% |
| **Historias de usuario** | Endpoints para gestionar, generar y mostrar historias de usuario en base de datos. | 3 | 30% |
| **Tareas** | Endpoints para gestionar, generar a partir de historias de usuario y mostrar tareas en base de datos. | 2 | 20% |
| **UI** | Interfaz de usuario con Jinja, HTML y Bootstrap o Tailwind CSS para mostrar y gestionar historias de usuario y tareas. No es necesario implementar edición ni borrado. | 3 | 30% |
| **Total** | | **10** | **100%** |

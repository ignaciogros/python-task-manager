Aquí tienes el contenido del **entregable1.docx** reescrito en formato **Markdown**:

# Proyecto: Entregable 1

## Objetivos
El objetivo de este proyecto es crear un sistema de generación de tareas asignadas a usuarios utilizando el framework **Flask**. En esta primera etapa, se desarrollará la arquitectura base y la lógica de programación inicial, organizando el proyecto mediante rutas que conecten con controladores para devolver resultados en formato **JSON**.

## Pautas de elaboración

### 1. Modelo de Datos: Clase `Task`
Se debe crear una aplicación Flask con rutas y controladores para gestionar tareas. La interfaz de la clase `Task` debe incluir los siguientes campos:

*   **id**: Clave primaria.
*   **title**: Título de la tarea.
*   **description**: Texto largo con la descripción completa.
*   **priority**: Niveles: baja, media, alta, bloqueante.
*   **effort_hours**: Número decimal (horas estimadas).
*   **status**: Estados: pendiente, en progreso, en revisión, completada.
*   **assigned_to**: String con el nombre de la persona asignada.

**Métodos requeridos para la clase `Task`:**
*   `to_dict()`: Convierte el objeto Task a un diccionario.
*   `from_dict()`: Crea un objeto Task a partir de un diccionario.

### 2. Gestión de Tareas: Clase `TaskManager`
Esta clase será la encargada de gestionar el almacenamiento de las tareas en un archivo **JSON**. Debe incluir los siguientes métodos estáticos:

*   `load_tasks()`: Carga las tareas desde `tasks.json` y las convierte en objetos `Task`.
*   `save_tasks()`: Guarda la lista de objetos `Task` en el archivo JSON.

### 3. Generación de Endpoints (Flask API)
Se deben implementar los siguientes puntos de acceso para el CRUD de tareas:

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| **POST** | `/tasks` | Crear una nueva tarea. |
| **GET** | `/tasks` | Leer todas las tareas. |
| **GET** | `/tasks/<id>` | Leer una tarea específica por su ID. |
| **PUT** | `/tasks/<id>` | Actualizar una tarea existente. |
| **DELETE** | `/tasks/<id>` | Eliminar una tarea. |

### 4. Arquitectura del Proyecto
Es necesario definir una estructura de ficheros organizada que incluya:
*   Entorno virtual y archivo de requerimientos (`requirements.txt`).
*   Fichero de rutas que conecte los endpoints con la lógica de `TaskManager`.
*   Uso de un archivo `tasks.json` para la persistencia de datos.

## Extensión y formato
La entrega consistirá en un archivo comprimido llamado `m2_proyecto_nombre_apellido.zip` que contenga la carpeta del proyecto Flask con todos los archivos Python necesarios.

## Rúbrica de evaluación

| Criterio | Descripción | Puntuación Máxima | Peso |
| :--- | :--- | :---: | :---: |
| **Arquitectura del proyecto** | Creación y organización del proyecto en Flask. | 2,5 | 25% |
| **Clase Tarea** | Implementación correcta de la clase `Task`. | 2,5 | 25% |
| **Clase TaskManager** | Implementación de la lógica de gestión y persistencia JSON. | 2,5 | 25% |
| **Crear rutas** | Definición de endpoints y respuestas en formato JSON. | 2,5 | 25% |
| **Total** | | **10** | **100%** |


# Proyecto: Entregable 2 — Integración de Endpoints de IA

## Objetivos
El objetivo de este entregable es implementar funcionalidades con IA Generativa en una aplicación API REST existente. Se comprenderán las ventajas de utilizar LLMs para diferentes tareas como generar descripciones, estimaciones y clasificaciones, y se practicarán técnicas de prompt engineering para obtener mejores resultados acordes a los objetivos del proyecto.

## Enunciado
Sobre el proyecto del entregable 1 (aplicación Flask o FastAPI con CRUD sobre el modelo `Task`), se agregarán nuevos endpoints que utilicen LLMs.

## Pautas de elaboración

### 1. Configuración del Entorno de Azure
Accede al portal de Azure e inicia sesión. Crea un recurso de **Azure OpenAI** o **Azure AI Foundry** y obtén las credenciales necesarias (clave API y endpoint) sobre un modelo a elección: `gpt-4o-mini`, `gpt-4.1-nano`, `gpt-4.1-mini` u otro. Opcionalmente, se puede usar directamente el proveedor **OpenAI**, **Anthropic** o cualquier otro de preferencia en lugar de Azure.

### 2. Preparación del Entorno de Desarrollo
Instala Python y un IDE (Visual Studio Code, Cursor, etc.). Configura un entorno virtual (`python -m venv venv`) y actívalo. Instala la biblioteca oficial de OpenAI (`pip install openai`) o el SDK de IA que se prefiera.

### 3. Nuevos Campos para el Modelo `Task`
Se mantienen los campos existentes y se añaden los siguientes:

*   **category**: Nuevo campo, puede ser `str` o `enum`.
*   **risk_analysis**: Nuevo campo de texto.
*   **risk_mitigation**: Nuevo campo de texto.

### 4. Nuevos Endpoints de IA

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| **POST** | `/ai/tasks/describe` | Recibe una tarea con `description` vacía y genera su descripción con LLM a partir del resto de campos (e.g., `title`). Devuelve la tarea con el campo `description` relleno. |
| **POST** | `/ai/tasks/categorize` | Recibe una tarea sin categoría y la clasifica con LLM bajo una categoría: Frontend, Backend, Testing, Infra, etc. Devuelve la tarea con el campo `category` relleno. |
| **POST** | `/ai/tasks/estimate` | Recibe una tarea sin `effort_hours` y estima su esfuerzo en horas a partir de `title`, `description` y `category`. Devuelve la tarea con `effort_hours` relleno (campo numérico; requiere parsing). |
| **POST** | `/ai/tasks/audit` | Recibe una tarea con todos los campos rellenos excepto `risk_analysis` y `risk_mitigation`. Lanza dos peticiones al LLM: la primera para obtener el análisis de riesgos (`risk_analysis`) y la segunda, usando esa información junto a los datos de la tarea, para obtener el plan de mitigación (`risk_mitigation`). |

### 5. Pruebas
Se aconseja probar los nuevos endpoints con **Postman**, **OpenAPI/Swagger** o cualquier otro sistema de pruebas de API REST.

## Extensión y formato
Entrega un archivo comprimido (`.zip`) que contenga:
*   La aplicación Flask o FastAPI completa.
*   Opcionalmente, la colección de Postman.

> **Nota:** Asegúrate de que el endpoint y la clave API estén configurados correctamente antes de probar el programa. No incluyas tus credenciales en la entrega.

## Rúbrica de evaluación

| Criterio | Descripción | Puntuación Máxima | Peso |
| :--- | :--- | :---: | :---: |
| **Endpoint `/ai/tasks/describe`** | Nuevo endpoint para generar descripciones de tareas. | 2,5 | 25% |
| **Endpoint `/ai/tasks/categorize`** | Nuevo endpoint para categorizar tareas. | 2,5 | 25% |
| **Endpoint `/ai/tasks/estimate`** | Nuevo endpoint para estimar horas de esfuerzo de una tarea. | 2,5 | 25% |
| **Endpoint `/ai/tasks/audit`** | Nuevo endpoint para estimar riesgos y su mitigación en una tarea. | 2,5 | 25% |
| **Total** | | **10** | **100%** |

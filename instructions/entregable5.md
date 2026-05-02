# Proyecto: Entregable 5

## Objetivos
El objetivo de este entregable es diseñar y configurar un pipeline CI/CD para el despliegue automatizado de una aplicación en la nube. Se implementará una aplicación backend con base de datos, contenida en Docker y gestionada con Docker Compose, y se desplegará en Azure utilizando **Azure Container Apps** o **Azure Container Instances**. Se integrarán buenas prácticas de configuración, seguridad, monitorización y validación del despliegue.

## Pautas de elaboración

### 1. Configuración del Entorno
*   Crea un repositorio en **Azure Repos** o GitHub.
*   Estructura el código de la aplicación backend usando **Python (Flask)** o **Node.js (Express)**.
*   Define un archivo `.env` con las credenciales y parámetros de conexión a la base de datos.

### 2. Contenerización de la Aplicación
*   Crea un `Dockerfile` para la imagen de la aplicación.
*   Implementa un `docker-compose.yml` que incluya:
    *   Un servicio para la aplicación backend.
    *   Un servicio de base de datos **MySQL** o **PostgreSQL**.
    *   Las variables de entorno necesarias para la conexión.
*   Prueba la aplicación en local con `docker-compose up --build`.

### 3. Registro y Gestión de Contenedores en Azure
Crea un **Azure Container Registry (ACR)** para almacenar la imagen del contenedor y súbela con los siguientes comandos:

```bash
az acr login --name <tu_acr>
docker tag mi-backend:v1 <tu_acr>.azurecr.io/mi-backend:v1
docker push <tu_acr>.azurecr.io/mi-backend:v1
```

### 4. Despliegue de la Aplicación en Azure
*   Configura un servicio en **Azure Container Apps** o **Azure Container Instances**.
*   Despliega la aplicación desde ACR asegurando que la base de datos esté accesible.
*   Define las variables de entorno en la configuración del servicio.

### 5. Automatización con CI/CD
Crea un pipeline en **Azure Pipelines** o **GitHub Actions** que automatice:
*   La compilación y construcción de la imagen del contenedor.
*   La ejecución de pruebas unitarias y de integración.
*   La subida de la imagen a ACR.
*   El despliegue automático de la nueva versión en Azure Container Apps o ACI.

### 6. Monitoreo y Validación
*   Verifica los logs de la aplicación con:
    ```bash
    az containerapp logs show --name mi-backend
    ```
*   Realiza pruebas de conexión con la base de datos desde la aplicación.

## Extensión y formato
Entrega un documento **PDF** o **Word** con capturas de pantalla del proceso. Extensión: 3 a 5 páginas. Fuente: Arial o Calibri 12, interlineado 1,5.

## Rúbrica de evaluación

| Criterio | Descripción | Puntuación Máxima | Peso |
| :--- | :--- | :---: | :---: |
| **Configuración y estructuración** | Correcta configuración del repositorio y estructura del código. | 1,5 | 15% |
| **Contenerización** | Creación adecuada del `Dockerfile` y `docker-compose.yml`. | 1,5 | 15% |
| **Registro en Azure** | Uso correcto de ACR para almacenamiento de la imagen. | 2 | 20% |
| **Despliegue en Azure** | Configuración y ejecución en Container Apps o Container Instances. | 2 | 20% |
| **Pipeline CI/CD** | Configuración del flujo de automatización con pruebas y despliegue continuo. | 2 | 20% |
| **Monitoreo y validación** | Implementación de logs y pruebas de conexión. | 1 | 10% |
| **Total** | | **10** | **100%** |

# Proyecto: Entregable 4

## Objetivos
El objetivo de este entregable es aprender a empaquetar aplicaciones en contenedores con **Docker** y automatizar la construcción, prueba y despliegue mediante pipelines de integración continua con **GitHub Actions** o **Azure Pipelines**. Se desarrollarán habilidades para garantizar la reproducibilidad y portabilidad de aplicaciones, y se evaluarán las ventajas de la integración continua en la automatización del ciclo de vida de las aplicaciones.

## Enunciado
Crear y desplegar una aplicación web utilizando **Flask**, contenerizada con **Docker** y configurada con un pipeline de integración continua usando **GitHub Actions**.

**Requisitos:**
*   Aplicación web simple en Python con Flask que responda con un mensaje de saludo en la ruta `/`.
*   `Dockerfile` que:
    *   Use una imagen base oficial de Python.
    *   Instale las dependencias desde `requirements.txt`.
    *   Exponga el puerto `5000`.
    *   Configure el comando de ejecución de la aplicación Flask.
*   Pipeline de GitHub Actions que:
    *   Descargue el código del repositorio.
    *   Construya la imagen Docker a partir del `Dockerfile`.
    *   Suba la imagen a Docker Hub.
*   **Opcional:** pruebas automatizadas con `pytest`.

## Pautas de elaboración

### 1. Preparación del Entorno
Crea un proyecto en **GitHub** o **Azure Repos**. Asegúrate de tener Docker configurado en tu máquina y una cuenta activa en Docker Hub.

### 2. Creación del `Dockerfile`
Escribe un `Dockerfile` que contenga:
*   Imagen base oficial de Python.
*   Instalación de dependencias.
*   Configuración del puerto expuesto.
*   Comando de ejecución de la aplicación.

### 3. Automatización del Pipeline
Define un pipeline de CI con las siguientes etapas:
*   **Build**: construcción de la imagen Docker.
*   **Test**: ejecución de pruebas unitarias dentro del contenedor.
*   **Push**: subida de la imagen a Docker Hub o Azure Container Registry.

Configura los secretos de Docker Hub en el repositorio de GitHub para permitir el acceso y la subida de imágenes.

### 4. Ejecución y Verificación
Ejecuta el pipeline desde el repositorio y verifica que todas las etapas se completen correctamente. Comprueba que la imagen esté disponible en Docker Hub o Azure Container Registry y que funcione al ser desplegada.

## Extensión y formato
Entrega un enlace a un repositorio público en **GitHub** o **Azure Repos** que contenga:
*   El archivo del pipeline (`.yaml`).
*   El `Dockerfile`.
*   `README.md` con la descripción del proyecto.

**Formato del `README.md`:** fuente Arial 12, interlineado 1,5, extensión mínima de dos páginas.

## Rúbrica de evaluación

| Criterio | Descripción | Puntuación Máxima | Peso |
| :--- | :--- | :---: | :---: |
| **Creación del `Dockerfile`** | El `Dockerfile` está bien estructurado y es funcional. | 2 | 20% |
| **Configuración del pipeline** | Pipeline bien definido con etapas claras. | 3 | 30% |
| **Automatización de pruebas** | Pruebas ejecutadas correctamente dentro del pipeline. | 2 | 20% |
| **Subida y despliegue del contenedor** | Imagen subida y funcional en Docker Hub o Azure Container Registry. | 2 | 20% |
| **Documentación en `README.md`** | Instrucciones claras y detalladas en el `README.md`. | 1 | 10% |
| **Total** | | **10** | **100%** |

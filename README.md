# Proyecto Flask modularizado para gestión de tareas con IA

Este proyecto permite gestionar tareas (Task) a través de un sistema modularizado en Flask, con almacenamiento en JSON y endpoints REST. Además, integra endpoints que utilizan modelos de lenguaje (LLM) para automatizar descripciones, categorización, estimación de esfuerzo y auditoría de riesgos en las tareas.

## Estructura
- env/: entorno virtual (no se sube al repositorio)
- htmlcov/: reportes de cobertura de tests (opcional)
- src/: Código fuente de la aplicación
    - managers/: gestión de carga y guardado de datos
    - models/: definición de modelos de datos
    - routes/: definición de endpoints REST
- ai/: Lógica de interacción con IA (OpenAI/Azure)
- tests/: Pruebas unitarias
- config.py: variables de configuración
- main.py: archivo principal de ejecución
- utils.py: funciones auxiliares (si fueran necesarias)

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Endpoints principales

### CRUD de tareas
- **POST /tasks**: Crear una tarea
- **GET /tasks**: Obtener todas las tareas
- **GET /tasks/<id>**: Obtener una tarea por ID
- **PUT /tasks/<id>**: Actualizar una tarea
- **DELETE /tasks/<id>**: Eliminar una tarea

### Endpoints con IA
- **POST /ai/tasks/describe**: Genera la descripción de una tarea a partir de su título y otros campos opcionales.
- **POST /ai/tasks/categorize**: Clasifica una tarea en una categoría (Backend, Frontend, Testing, Documentación, Otro) usando IA.
- **POST /ai/tasks/estimate**: Estima el esfuerzo en horas de una tarea a partir de su título, descripción, prioridad y categoría.
- **POST /ai/tasks/audit**: Genera un análisis de riesgos y un plan de mitigación para una tarea usando IA.

## Ejemplos de uso de la API

### Crear una tarea (POST)
```bash
curl -X POST http://127.0.0.1:5000/tasks \
-H "Content-Type: application/json" \
-d '{"title": "Tarea de ejemplo", "description": "Descripción", "priority": "alta", "effort_hours": 2, "status": "pendiente", "assigned_to": "Juan"}'
```

### Obtener todas las tareas (GET)
```bash
curl http://127.0.0.1:5000/tasks
```

### Obtener una tarea por ID (GET)
```bash
curl http://127.0.0.1:5000/tasks/1
```

### Actualizar una tarea (PUT)
```bash
curl -X PUT http://127.0.0.1:5000/tasks/1 \
-H "Content-Type: application/json" \
-d '{"title": "Tarea actualizada", "description": "Nueva descripción", "priority": "media", "effort_hours": 3, "status": "en progreso", "assigned_to": "Ana"}'
```

### Eliminar una tarea (DELETE)
```bash
curl -X DELETE http://127.0.0.1:5000/tasks/1
```

### Endpoint IA: Describir tarea (POST)
```bash
curl -X POST http://127.0.0.1:5000/ai/tasks/describe \
-H "Content-Type: application/json" \
-d '{"title": "Implementar autenticación JWT", "description": "", "priority": "alta", "category": "Backend"}'
```

### Endpoint IA: Categorizar tarea (POST)
```bash
curl -X POST http://127.0.0.1:5000/ai/tasks/categorize \
-H "Content-Type: application/json" \
-d '{"title": "Crear pruebas unitarias", "description": "Escribir tests para el módulo de usuarios"}'
```

### Endpoint IA: Estimar esfuerzo (POST)
```bash
curl -X POST http://127.0.0.1:5000/ai/tasks/estimate \
-H "Content-Type: application/json" \
-d '{"title": "Desarrollar API REST", "description": "Crear endpoints para gestión de usuarios", "priority": "media", "category": "Backend"}'
```

### Endpoint IA: Auditar tarea (POST)
```bash
curl -X POST http://127.0.0.1:5000/ai/tasks/audit \
-H "Content-Type: application/json" \
-d '{"title": "Actualizar librerías del proyecto", "description": "Actualizar dependencias a sus últimas versiones", "priority": "media", "category": "Backend"}'
```

## Ejecución de tests

1. Activa el entorno virtual:
    ```bash
    env\Scripts\activate
    ```

2. Ejecuta los tests con pytest:
    ```bash
    pytest
    ```

3. Para ver la cobertura de los tests:
    ```bash
    pytest --cov=src tests/ 
    ```
    que generará un informe en la terminal, o bien
    
    ```bash
    pytest --cov=src --cov-report=html tests/
    ```
    El informe detallado estará en la carpeta `htmlcov`.

---

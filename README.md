# Proyecto de Gestión Ágil de Tareas e Historias de Usuario con Flask, SQLAlchemy y Azure OpenAI

Este proyecto es una aplicación web modularizada en Flask para la gestión de historias de usuario y tareas, integrando:
- Backend en Flask con arquitectura limpia (managers, models, routes, schemas)
- Persistencia en base de datos relacional (SQLAlchemy + MySQL)
- Validación y serialización robusta con Pydantic
- Vistas HTML con Jinja2 para gestión visual
- Integración de IA (Azure OpenAI) para generación automática de historias de usuario y tareas
- Feedback visual y control de errores en frontend

## Estructura del proyecto
- `env/`: entorno virtual (no incluido en el repo)
- `src/`: código fuente principal
    - `models/`: modelos ORM (SQLAlchemy) para Task y UserStory
    - `schemas/`: Schemas Pydantic para validación y serialización
    - `managers/`: lógica de acceso a base de datos
    - `routes/`: endpoints REST y vistas HTML
    - `templates/`: vistas Jinja2 (`user-stories.html`, `tasks.html`)
    - `config.py`, `utils.py`, `__init__.py`
- `ai/`: lógica de integración con Azure OpenAI
- `tests/`: pruebas unitarias
- `main.py`: punto de entrada de la app

## Instalación

```bash
pip install -r requirements.txt
```

Configura tu base de datos MySQL y las variables de entorno necesarias en `config.py`.

## Ejecución

```bash
python main.py
```

## Endpoints principales

### CRUD de historias de usuario
- **POST /user_stories**: Crear una historia de usuario
- **GET /user_stories**: Obtener todas las historias de usuario
- **GET /user_stories/<id>**: Obtener una historia de usuario por ID
- **PUT /user_stories/<id>**: Actualizar una historia de usuario
- **DELETE /user_stories/<id>**: Eliminar una historia de usuario

### CRUD de tareas
- **POST /tasks**: Crear una tarea
- **GET /tasks**: Obtener todas las tareas
- **GET /tasks/<id>**: Obtener una tarea por ID
- **PUT /tasks/<id>**: Actualizar una tarea
- **DELETE /tasks/<id>**: Eliminar una tarea

### Endpoints de IA
- **POST /user-stories**: Generar historia de usuario desde prompt (IA)
- **POST /user-stories/<user_story_id>/generate-tasks**: Generar tareas para una historia de usuario (IA)

### Vistas HTML
- **GET /user-stories**: Vista HTML de historias de usuario
- **GET /user-stories/<user_story_id>/tasks**: Vista HTML de tareas asociadas a una historia de usuario

## Ejemplos de uso de la API

### Crear una historia de usuario
```bash
curl -X POST http://127.0.0.1:5000/user_stories \
-H "Content-Type: application/json" \
-d '{
  "project": "Proyecto Demo",
  "role": "Como usuario",
  "goal": "quiero poder registrarme",
  "reason": "para acceder a funcionalidades exclusivas",
  "description": "El usuario debe poder crear una cuenta con email y contraseña.",
  "priority": "alta",
  "story_points": 5,
  "effort_hours": 8,
  "created_at": null
}'
```

### Crear una tarea
```bash
curl -X POST http://127.0.0.1:5000/tasks \
-H "Content-Type: application/json" \
-d '{
  "title": "Implementar autenticación de usuarios",
  "description": "Desarrollar el sistema de login y registro para la aplicación.",
  "priority": "alta",
  "effort_hours": 3.5,
  "status": "pendiente",
  "assigned_to": "Backend",
  "user_story_id": 1
}'
```

### Generar historia de usuario desde prompt (IA)
- Desde la vista HTML `/user-stories` puedes introducir un prompt y la IA generará y guardará una historia de usuario.

### Generar tareas para una historia de usuario (IA)
- En la vista de historias de usuario, puedes pulsar "Generar tareas" y la IA descompondrá la historia en tareas técnicas, que se guardarán automáticamente.

### Ver tareas asociadas a una historia de usuario
- Accede a `/user-stories/<user_story_id>/tasks` para ver todas las tareas generadas o asociadas a esa historia.

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
    pytest --cov=src --cov-report=html tests/
    ```
    El informe detallado estará en la carpeta `htmlcov`.

---

**Notas:**
- El proyecto usa SQLAlchemy para la persistencia y Pydantic para validación/serialización.
- La integración con Azure OpenAI permite generación automática de historias de usuario y tareas, con control de errores y feedback visual en frontend.
- El frontend HTML usa Jinja2 y muestra feedback de carga y alertas tras operaciones.
- El código está modularizado y preparado para ampliaciones futuras.

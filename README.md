# Proyecto Flask modularizado para gestión de tareas
El proyecto, en su fase de entregable 1, tendrá que ser capaz de gestionar tareas (Task) a través de un Task_Manager que carge y guarde estas tareas en desde/hacia un JSON y el control de creación,modificado,borrado y consulta se hará a través del framework flask con endpoints.

## Estructura
- env/: entorno virtual, si es necesario (opcional)
- htmlcov/ carpeta de reportes html de coverage de tests de código (opcional)
- src/: Código fuente de la aplicación
    -managers/: gestiona la carga y descarga de datos
    -models/: define los modelos usados
    -routes/: define las rutas (endpoints) para gestionar los datos
- tests/: Pruebas unitarias
config.py: definimos variables del sistema/proyecto
main.py: archivo principal de ejecución
utils.py: funciones auxiliares, si hicieran falta.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python -m src.main
```

## Ejemplos de uso de la API

### Crear una tarea (POST)
```bash
curl -X POST http://127.0.0.1:5000/tasks \
-H "Content-Type: application/json" \
-d "{\"title\": \"Tarea de ejemplo\", \"description\": \"Descripción\", \"priority\": \"alta\", \"effort_hours\": 2, \"status\": \"pendiente\", \"assigned_to\": \"Juan\"}"
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
-d "{\"title\": \"Tarea actualizada\", \"description\": \"Nueva descripción\", \"priority\": \"media\", \"effort_hours\": 3, \"status\": \"en progreso\", \"assigned_to\": \"Ana\"}"
```

### Eliminar una tarea (DELETE)
```bash
curl -X DELETE http://127.0.0.1:5000/tasks/1
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

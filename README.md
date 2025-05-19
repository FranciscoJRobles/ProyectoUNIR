# Proyecto Flask modularizado para gestión de tareas
El proyecto, en su fase de entregable 1, tendrá que ser capaz de gestionar tareas (Task) a través de un Task_Manager que carge y guarde estas tareas en desde/hacia un JSON y el control de creación,modificado,borrado y consulta se hará a través del framework flask con endpoints.

## Estructura
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

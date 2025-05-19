import json
import os
from src.config import DATA_FILE
from src.models.task import Task

class TaskManager:
    @staticmethod
    def load_tasks():
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("El archivo de tareas no contiene una lista.")
                tasks = []
                for item in data:
                    try:
                        tasks.append(Task.from_dict(item))
                    except Exception as e:
                        # Puedes loguear el error aquí si lo deseas
                        continue  # Ignora tareas corruptas individuales
                return tasks
        except json.JSONDecodeError:
            # Archivo corrupto o vacío
            return []
        except Exception as e:
            # Otro error inesperado
            raise RuntimeError(f"Error al cargar las tareas: {e}")

    @staticmethod
    def save_tasks(tasks):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise RuntimeError(f"Error al guardar las tareas: {e}")
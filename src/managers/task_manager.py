import json
import os
from src.config import DATA_FILE
from src.models.task import Task

class TaskManager:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file

    def load_tasks(self):
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("El archivo de tareas no contiene una lista.")
                tasks = []
                for item in data:
                    try:
                        tasks.append(Task.from_dict(item))
                    except Exception:
                        continue  # Ignora tareas corruptas individuales
                return tasks
        except json.JSONDecodeError:
            return []
        except Exception as e:
            raise RuntimeError(f"Error al cargar las tareas: {e}")

    def save_tasks(self, tasks):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise RuntimeError(f"Error al guardar las tareas: {e}")
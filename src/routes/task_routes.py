from flask import Blueprint, request, jsonify
from src.models.task import Task, PriorityEnum, StatusEnum
from src.managers.task_manager import TaskManager

def create_tasks_blueprint(task_manager=None):
    tasks_bp = Blueprint('tasks', __name__)
    tm = task_manager or TaskManager()

    def validate_task_data(data, require_all_fields=True):
        required_fields = ["title", "description", "priority", "effort_hours", "status", "assigned_to"]
        errors = []

        for field in required_fields:
            if field not in data:
                if require_all_fields:
                    errors.append(f"Falta el campo: {field}")
            else:
                if field == "priority" and data[field] not in PriorityEnum._value2member_map_:
                    errors.append(f"Prioridad no válida: {data[field]}")
                if field == "status" and data[field] not in StatusEnum._value2member_map_:
                    errors.append(f"Estado no válido: {data[field]}")
                if field == "effort_hours":
                    try:
                        float(data[field])
                    except (ValueError, TypeError):
                        errors.append("El campo 'effort_hours' debe ser un número")

        return errors

    # Crear una tarea
    @tasks_bp.route('/tasks', methods=['POST'])
    def create_task():
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400

        errors = validate_task_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        try:
            tasks = tm.load_tasks()
            new_id = max([t.id for t in tasks], default=0) + 1
            task = Task(
                id=new_id,
                title=data['title'],
                description=data['description'],
                priority=PriorityEnum(data['priority']),
                effort_hours=float(data['effort_hours']),
                status=StatusEnum(data['status']),
                assigned_to=data['assigned_to']
            )
            tasks.append(task)
            tm.save_tasks(tasks)
            return jsonify(task.to_dict()), 201
        except Exception as e:
            return jsonify({"error": f"Error al crear la tarea(Task): {str(e)}"}), 500

    # Leer todas las tareas
    @tasks_bp.route('/tasks', methods=['GET'])
    def get_tasks():
        try:
            tasks = tm.load_tasks()
            return jsonify([task.to_dict() for task in tasks])
        except Exception as e:
            return jsonify({"error": f"Error al obtener las tareas: {str(e)}"}), 500

    # Leer una tarea específica
    @tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        try:
            tasks = tm.load_tasks()
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                return jsonify({'error': 'Tarea(Task) no encontrada'}), 404
            return jsonify(task.to_dict())
        except Exception as e:
            return jsonify({"error": f"Error al obtener la tarea(Task): {str(e)}"}), 500

    # Actualizar una tarea
    @tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400

        errors = validate_task_data(data, require_all_fields=False)
        if errors:
            return jsonify({"errors": errors}), 400

        try:
            tasks = tm.load_tasks()
            for i, t in enumerate(tasks):
                if t.id == task_id:
                    # Solo actualiza los campos presentes en data
                    updated_data = t.to_dict()
                    updated_data.update(data)
                    tasks[i] = Task(
                        id=task_id,
                        title=updated_data['title'],
                        description=updated_data['description'],
                        priority=PriorityEnum(updated_data['priority']),
                        effort_hours=float(updated_data['effort_hours']),
                        status=StatusEnum(updated_data['status']),
                        assigned_to=updated_data['assigned_to']
                    )
                    tm.save_tasks(tasks)
                    return jsonify(tasks[i].to_dict())
            return jsonify({'error': 'Tarea no encontrada'}), 404
        except Exception as e:
            return jsonify({"error": f"Error al actualizar la tarea: {str(e)}"}), 500

    # Eliminar una tarea
    @tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        try:
            tasks = tm.load_tasks()
            if not any(t.id == task_id for t in tasks):
                return jsonify({'error': 'Tarea no encontrada'}), 404
            tasks = [t for t in tasks if t.id != task_id]
            tm.save_tasks(tasks)
            return jsonify({'result': 'Tarea eliminada'})
        except Exception as e:
            return jsonify({"error": f"Error al eliminar la tarea: {str(e)}"}), 500

    return tasks_bp
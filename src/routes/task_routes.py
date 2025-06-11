from flask import Blueprint, request, jsonify
from src.models.task import Task, PriorityEnum, StatusEnum, CategoryEnum
from src.managers.task_manager import TaskManager
from ai.ia_task_manager import create_task_description, create_task_category, create_task_effort_estimate, create_task_audit

def create_tasks_blueprint(task_manager=None):
    tasks_bp = Blueprint('tasks', __name__)
    tm = task_manager or TaskManager()

    def validate_task_data(data, require_all_fields=True):
        required_fields = ["title", "description", "priority", "effort_hours", "status", "assigned_to"]
        optional_fields = ["category", "risk_analysis", "risk_mitigation"]
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
        # Validar category si está presente
        if "category" in data and data["category"] is not None:
            if data["category"] not in CategoryEnum._value2member_map_:
                errors.append(f"Categoría no válida: {data['category']}")
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
                assigned_to=data['assigned_to'],
                category=CategoryEnum(data['category']) if data.get('category') else None,
                risk_analysis=data.get('risk_analysis'),
                risk_mitigation=data.get('risk_mitigation')
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
                return jsonify({'error': 'Tarea no encontrada'}), 404
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
                    updated_data = t.to_dict()
                    updated_data.update(data)
                    tasks[i] = Task(
                        id=task_id,
                        title=updated_data['title'],
                        description=updated_data['description'],
                        priority=PriorityEnum(updated_data['priority']),
                        effort_hours=float(updated_data['effort_hours']),
                        status=StatusEnum(updated_data['status']),
                        assigned_to=updated_data['assigned_to'],
                        category=CategoryEnum(updated_data['category']) if updated_data.get('category') else None,
                        risk_analysis=updated_data.get('risk_analysis'),
                        risk_mitigation=updated_data.get('risk_mitigation')
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

    # Endpoint para describir una tarea usando IA
    @tasks_bp.route('/ai/tasks/describe', methods=['POST'])
    def describe_task_ai():
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400
        try:
            task_with_desc = create_task_description(data)
            return jsonify(task_with_desc)
        except Exception as e:
            return jsonify({"error": f"Error al generar la descripción con IA: {str(e)}"}), 500

    # Endpoint para categorizar una tarea usando IA
    @tasks_bp.route('/ai/tasks/categorize', methods=['POST'])
    def categorize_task_ai():
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400
        try:
            task_with_category = create_task_category(data)
            return jsonify(task_with_category)
        except Exception as e:
            return jsonify({"error": f"Error al categorizar la tarea con IA: {str(e)}"}), 500

    # Endpoint para estimar el esfuerzo de una tarea usando IA
    @tasks_bp.route('/ai/tasks/estimate', methods=['POST'])
    def estimate_task_effort_ai():
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400
        try:
            task_with_effort = create_task_effort_estimate(data)
            return jsonify(task_with_effort)
        except Exception as e:
            return jsonify({"error": f"Error al estimar el esfuerzo con IA: {str(e)}"}), 500

    # Endpoint para auditar una tarea usando IA
    @tasks_bp.route('/ai/tasks/audit', methods=['POST'])
    def audit_task_ai():
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400
        try:
            audited_task = create_task_audit(data)
            return jsonify(audited_task)
        except Exception as e:
            return jsonify({"error": f"Error al auditar la tarea con IA: {str(e)}"}), 500

    return tasks_bp


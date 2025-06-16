from flask import Blueprint, request, jsonify
from src.managers.task_manager import TaskManager
from src.schemas.task_schema import TaskSchema, TaskSchemas
from pydantic import ValidationError
from ai.ia_task_manager import create_task_description, create_task_category, create_task_effort_estimate, create_task_audit

def create_tasks_blueprint(task_manager=None):
    tasks_bp = Blueprint('tasks', __name__)
    tm = task_manager or TaskManager()

    # Crear una tarea
    @tasks_bp.route('/tasks', methods=['POST'])
    def create_task():
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400
        try:
            validated = TaskSchema(**data)
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 422
        task = tm.add_task(validated.model_dump())
        return jsonify(TaskSchema.model_validate(task.to_dict()).model_dump()), 201

    # Leer todas las tareas
    @tasks_bp.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = tm.get_all_tasks()
        return jsonify(TaskSchemas([TaskSchema.model_validate(t.to_dict()) for t in tasks]).model_dump())

    # Leer una tarea específica
    @tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        task = tm.get_task(task_id)
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        return jsonify(TaskSchema.model_validate(task.to_dict()).model_dump())

    # Actualizar una tarea
    @tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400
        try:
            validated = TaskSchema(**data)
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 422
        task = tm.update_task(task_id, validated.model_dump())
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        return jsonify(TaskSchema.model_validate(task.to_dict()).model_dump())

    # Eliminar una tarea
    @tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        success = tm.delete_task(task_id)
        if not success:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        return jsonify({'result': 'Tarea eliminada'})

    # Endpoints IA (se mantienen igual)
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


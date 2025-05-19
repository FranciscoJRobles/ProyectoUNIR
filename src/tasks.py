from flask import Blueprint, request, jsonify
from .utils import load_tasks, save_tasks
from .models import Task, PriorityEnum, StatusEnum

# Blueprint
tasks_bp = Blueprint('tasks', __name__)

# Helpers

def dicts_to_tasks(tasks_dicts):
    return [Task(
        id=t['id'],
        title=t['title'],
        description=t['description'],
        priority=PriorityEnum(t['priority']),
        effort_hours=t['effort_hours'],
        status=StatusEnum(t['status']),
        assigned_to=t['assigned_to']
    ) for t in tasks_dicts]

def tasks_to_dicts(tasks):
    return [task.to_dict() for task in tasks]

# Crear una tarea
@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    tasks = dicts_to_tasks(load_tasks())
    new_id = max([t.id for t in tasks], default=0) + 1
    task = Task(
        id=new_id,
        title=data['title'],
        description=data['description'],
        priority=PriorityEnum(data['priority']),
        effort_hours=data['effort_hours'],
        status=StatusEnum(data['status']),
        assigned_to=data['assigned_to']
    )
    tasks.append(task)
    save_tasks(tasks_to_dicts(tasks))
    return jsonify(task.to_dict()), 201

# Leer todas las tareas
@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = dicts_to_tasks(load_tasks())
    return jsonify(tasks_to_dicts(tasks))

# Leer una tarea específica
@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    tasks = dicts_to_tasks(load_tasks())
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict())

# Actualizar una tarea
@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    tasks = dicts_to_tasks(load_tasks())
    for task in tasks:
        if task.id == task_id:
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            if 'priority' in data:
                task.priority = PriorityEnum(data['priority'])
            if 'effort_hours' in data:
                task.effort_hours = data['effort_hours']
            if 'status' in data:
                task.status = StatusEnum(data['status'])
            if 'assigned_to' in data:
                task.assigned_to = data['assigned_to']
            save_tasks(tasks_to_dicts(tasks))
            return jsonify(task.to_dict())
    return jsonify({'error': 'Task not found'}), 404

# Eliminar una tarea
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = dicts_to_tasks(load_tasks())
    new_tasks = [t for t in tasks if t.id != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    save_tasks(tasks_to_dicts(new_tasks))
    return '', 204

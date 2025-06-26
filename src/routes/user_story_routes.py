from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from src.managers.user_story_manager import UserStoryManager
from src.schemas.user_story_schema import UserStorySchema, UserStorySchemas
from src.schemas.task_schema import TaskSchema, TaskSchemas
from src.managers.task_manager import TaskManager
from pydantic import ValidationError
from ai.ia_client import process_message_with_AI, ResponseType
import json

response_limit = 1500

#Rutas CRUD básicas para historias de usuario

def create_user_stories_blueprint(user_story_manager=None):
    user_stories_bp = Blueprint('user_stories', __name__)
    usm = user_story_manager or UserStoryManager()

    @user_stories_bp.route('/user_stories', methods=['POST'])
    def create_user_story():
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400
        try:
            validated = UserStorySchema(**data)
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 422
        user_story = usm.add_user_story(validated.model_dump())
        return jsonify(UserStorySchema.model_validate(user_story).model_dump()), 201

    @user_stories_bp.route('/user_stories', methods=['GET'])
    def get_user_stories():
        user_stories = usm.get_all_user_stories()
        return jsonify(UserStorySchemas(UserStorySchemasList=[UserStorySchema.model_validate(us) for us in user_stories]).model_dump())

    @user_stories_bp.route('/user_stories/<int:user_story_id>', methods=['GET'])
    def get_user_story(user_story_id):
        user_story = usm.get_user_story(user_story_id)
        if not user_story:
            return jsonify({"error": "Historia de usuario no encontrada"}), 404
        return jsonify(UserStorySchema.model_validate(user_story).model_dump())

    @user_stories_bp.route('/user_stories/<int:user_story_id>', methods=['PUT'])
    def update_user_story(user_story_id):
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos de entrada"}), 400
        try:
            validated = UserStorySchema(**data)
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 422
        user_story = usm.update_user_story(user_story_id, validated.model_dump())
        if not user_story:
            return jsonify({"error": "Historia de usuario no encontrada"}), 404
        return jsonify(UserStorySchema.model_validate(user_story).model_dump())
    
    @user_stories_bp.route('/user_stories/<int:user_story_id>', methods=['DELETE'])
    def delete_user_story(user_story_id):
        success = usm.delete_user_story(user_story_id)
        if not success:
            return jsonify({"error": "Historia de usuario no encontrada"}), 404
        return jsonify({"message": "Historia de usuario eliminada"})

    #####

    # #### Rutas para renderizar la plantilla HTML con las historias de usuario #####
    
    @user_stories_bp.route('/user-stories', methods=['GET'])
    def user_stories_html():
        user_stories = usm.get_all_user_stories()
        # Pasar los objetos ORM convertidos a diccionario para Jinja2
        try:
            user_stories_dicts = [us.to_dict() for us in user_stories]
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 422
        return render_template('user-stories.html', user_stories=user_stories_dicts)

    @user_stories_bp.route('/user-stories', methods=['POST'])
    def generate_user_story_from_prompt():
        prompt = request.form.get('prompt')
        if not prompt:
            return jsonify({'error': 'No se proporcionó prompt'}), 400
        # Contexto de rol system para la IA
        context = [
            {"role": "system", "content": "Eres un experto en desarrollo de software y en la creación de historias de usuario siguiendo buenas prácticas ágiles. Tu tarea es generar historias de usuario claras, concisas y útiles para equipos de desarrollo."}
        ]
        response = process_message_with_AI(prompt, context, ResponseType.ANALYTICS, UserStorySchema)
        try:
            user_story_data = json.loads(response)
            validated = UserStorySchema(**user_story_data)
        except Exception as e:
            return f"<script>alert('Respuesta IA inválida: {str(e)}'); window.location.href='{url_for('user_stories.user_stories_html')}';</script>"
        usm = UserStoryManager()
        user_story = usm.add_user_story(validated.model_dump())
        return f"<script>alert('Historia de usuario generada y guardada correctamente'); window.location.href='{url_for('user_stories.user_stories_html')}';</script>"

    @user_stories_bp.route('/user-stories/<int:user_story_id>/generate-tasks', methods=['POST'])
    def generate_tasks_for_user_story(user_story_id):
        # Obtener la historia de usuario
        usm = UserStoryManager()
        user_story = usm.get_user_story(user_story_id)
        if not user_story:
            return f"<script>alert('Historia de usuario no encontrada'); window.location.href='{url_for('user_stories.user_stories_html')}';</script>"
        # Construir prompt para la IA
        prompt = f"Genera una lista de tareas detalladas para la siguiente historia de usuario: {user_story.to_dict()}"

        context = [
            {"role": "system", "content": "Eres un experto en gestión de proyectos ágiles y descomposición de historias de usuario en tareas técnicas. Se te va a dar una historia de usuario en formato json y debes devolver SOLO un array de objetos JSON puros (sin saltos de linea) en base al model que tienes en el parámetro response_format. Creame al menos 2 tasks dentro del array pero no más de 4, y cada task que no tenga más de 200 palabras. En cualquier caso el límite total en tu respuesta no puede superar las {response_limit} palabras"},]

        response = process_message_with_AI(prompt, context, ResponseType.CREATIVE, TaskSchemas)
        try:
            tasks_data = json.loads(response)
            validated_tasks = TaskSchemas(**tasks_data)
        except Exception as e:
            return f"<script>alert('Respuesta IA inválida: {str(e)}'); window.location.href='{url_for('user_stories.user_stories_html')}';</script>"
        # Guardar tareas en base de datos
        tm = TaskManager()
        for task in validated_tasks.TaskSchemasList:
            # Crea una copia del modelo con el user_story_id actualizado
            task_with_us = task.model_copy(update={'user_story_id': user_story_id})
            tm.add_task(task_with_us.model_dump())
        return redirect(url_for('user_stories.tasks_for_user_story', user_story_id=user_story_id))

    @user_stories_bp.route('/user-stories/<int:user_story_id>/tasks', methods=['GET'])
    def tasks_for_user_story(user_story_id):
        from src.managers.task_manager import TaskManager
        tm = TaskManager()
        tasks = [t for t in tm.get_all_tasks() if t.user_story_id == user_story_id]
        # Convertir a dict para Jinja2
        tasks_dicts = [t.to_dict() for t in tasks]
        return render_template('tasks.html', tasks=tasks_dicts, user_story_id=user_story_id)

    return user_stories_bp

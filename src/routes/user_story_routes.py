from flask import Blueprint, request, jsonify
from src.managers.user_story_manager import UserStoryManager
from src.schemas.user_story_schema import UserStorySchema, UserStorySchemas
from pydantic import ValidationError

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
        return jsonify(UserStorySchema.model_validate(user_story.to_dict()).model_dump()), 201

    @user_stories_bp.route('/user_stories', methods=['GET'])
    def get_user_stories():
        user_stories = usm.get_all_user_stories()
        return jsonify(UserStorySchemas([UserStorySchema.model_validate(us.to_dict()) for us in user_stories]).model_dump())

    @user_stories_bp.route('/user_stories/<int:user_story_id>', methods=['GET'])
    def get_user_story(user_story_id):
        user_story = usm.get_user_story(user_story_id)
        if not user_story:
            return jsonify({"error": "Historia de usuario no encontrada"}), 404
        return jsonify(UserStorySchema.model_validate(user_story.to_dict()).model_dump())

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
        return jsonify(UserStorySchema.model_validate(user_story.to_dict()).model_dump())

    @user_stories_bp.route('/user_stories/<int:user_story_id>', methods=['DELETE'])
    def delete_user_story(user_story_id):
        success = usm.delete_user_story(user_story_id)
        if not success:
            return jsonify({"error": "Historia de usuario no encontrada"}), 404
        return jsonify({"message": "Historia de usuario eliminada"})

    return user_stories_bp

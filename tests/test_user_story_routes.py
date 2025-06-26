import pytest
from flask import Flask
from src.routes.user_story_routes import create_user_stories_blueprint
from src.managers.user_story_manager import UserStoryManager
from unittest.mock import MagicMock
from datetime import datetime, timezone

from src.db import db  # Importa la instancia de SQLAlchemy

fake_data_get = {
        "id": 1,
        "project": "Proyecto Demo",
        "role": "Como usuario",
        "goal": "quiero poder registrarme",
        "reason": "para acceder a funcionalidades exclusivas",
        "description": "El usuario debe poder crear una cuenta con email y contraseña.",
        "priority": "alta",
        "story_points": 5,
        "effort_hours": 8,
        "created_at": datetime.now(timezone.utc)  # Campo obligatorio
    }

fake_data_post = {
        "project": "Proyecto Demo",
        "role": "Como usuario",
        "goal": "quiero poder registrarme",
        "reason": "para acceder a funcionalidades exclusivas",
        "description": "El usuario debe poder crear una cuenta con email y contraseña.",
        "priority": "alta",
        "story_points": 5,
        "effort_hours": 8
}

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Inicializa SQLAlchemy con la app
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos en memoria
    user_story_manager = MagicMock(spec=UserStoryManager)

    # Mock para get_all_user_stories con datos que incluyen to_dict
    mock_user_story = MagicMock()
    mock_user_story.to_dict.return_value = fake_data_get
    user_story_manager.get_all_user_stories.return_value = [fake_data_get]
    user_story_manager.get_user_story.return_value = fake_data_get
    user_story_manager.add_user_story.return_value = fake_data_post
    user_story_manager.update_user_story.return_value = fake_data_get
    app.register_blueprint(create_user_stories_blueprint(user_story_manager))
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user_story(client):
    data = fake_data_post

    response = client.post('/user_stories', json=data)
    assert response.status_code == 201

def test_get_user_stories(client):
    response = client.get('/user_stories')
    assert response.status_code == 200

def test_get_user_story(client):
    response = client.get('/user_stories/1')
    assert response.status_code in [200, 404]

def test_update_user_story(client):
    data = fake_data_post
    response = client.put('/user_stories/1', json=data)
    assert response.status_code in [200, 404]

def test_delete_user_story(client):
    response = client.delete('/user_stories/1')
    assert response.status_code in [200, 404]

def test_generate_user_story_from_prompt(client):
    data = {"prompt": "Como usuario quiero registrarme para acceder a funcionalidades exclusivas."}
    response = client.post('/user-stories', data=data)
    assert response.status_code in [200, 400]

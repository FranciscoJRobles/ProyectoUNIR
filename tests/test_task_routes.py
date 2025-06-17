import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from src.routes.task_routes import create_tasks_blueprint

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(create_tasks_blueprint(task_manager=MagicMock()))
    with app.test_client() as client:
        yield client

def get_fake_task_dict(id=1, **kwargs):
    defaults = {
        "id": id,
        "title": "Test tarea",
        "description": "Descripción de prueba",
        "priority": "alta",
        "effort_hours": 2,
        "status": "pendiente",
        "assigned_to": "Juan",
        "user_story_id": 1,
        "created_at": None
    }
    defaults.update(kwargs)
    return defaults

@patch('src.managers.task_manager.TaskManager.add_task')
def test_create_task(mock_add_task, client):
    fake_task = get_fake_task_dict()
    mock_add_task.return_value = MagicMock(**fake_task)
    data = fake_task.copy()
    del data["id"]
    del data["created_at"]
    response = client.post("/tasks", json=data)
    assert response.status_code == 201
    resp_json = response.get_json()
    assert resp_json["title"] == data["title"]
    assert resp_json["priority"] == data["priority"]

@patch('src.managers.task_manager.TaskManager.get_all_tasks')
def test_get_tasks(mock_get_all, client):
    mock_get_all.return_value = [MagicMock(**get_fake_task_dict(id=1)), MagicMock(**get_fake_task_dict(id=2, title="Otra tarea"))]
    response = client.get("/tasks")
    assert response.status_code == 200
    resp_json = response.get_json()
    assert isinstance(resp_json["TaskSchemasList"], list)
    assert len(resp_json["TaskSchemasList"]) == 2

@patch('src.managers.task_manager.TaskManager.get_task')
def test_get_task(mock_get_task, client):
    mock_get_task.return_value = MagicMock(**get_fake_task_dict(id=1))
    response = client.get("/tasks/1")
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json["id"] == 1

@patch('src.managers.task_manager.TaskManager.update_task')
def test_update_task(mock_update_task, client):
    fake_task = get_fake_task_dict(id=1, title="Tarea actualizada", priority="media")
    mock_update_task.return_value = MagicMock(**fake_task)
    update = fake_task.copy()
    response = client.put("/tasks/1", json=update)
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json["title"] == update["title"]
    assert resp_json["priority"] == update["priority"]

@patch('src.managers.task_manager.TaskManager.delete_task')
def test_delete_task(mock_delete_task, client):
    mock_delete_task.return_value = True
    response = client.delete("/tasks/1")
    assert response.status_code == 200

@patch('src.managers.task_manager.TaskManager.add_task')
def test_create_task_validation_error(mock_add_task, client):
    data = {"title": "Falta campos"}
    response = client.post("/tasks", json=data)
    assert response.status_code in (400, 422)

@patch('src.managers.task_manager.TaskManager.get_task')
def test_get_task_not_found(mock_get_task, client):
    mock_get_task.return_value = None
    response = client.get("/tasks/999")
    assert response.status_code == 404

@patch('src.managers.task_manager.TaskManager.update_task')
def test_update_task_not_found(mock_update_task, client):
    mock_update_task.return_value = None
    update = get_fake_task_dict(id=999, title="No existe", description="No existe", priority="media", effort_hours=1, status="pendiente", assigned_to="Nadie")
    response = client.put("/tasks/999", json=update)
    assert response.status_code == 404

@patch('src.managers.task_manager.TaskManager.delete_task')
def test_delete_task_not_found(mock_delete_task, client):
    mock_delete_task.return_value = False
    response = client.delete("/tasks/999")
    assert response.status_code == 404


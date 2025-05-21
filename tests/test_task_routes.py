import pytest
from flask import Flask
from src.routes.task_routes import create_tasks_blueprint
from src.managers.task_manager import TaskManager

@pytest.fixture
def client(tmp_path):
    test_data_file = tmp_path / "tasks_test.json"
    tm = TaskManager(data_file=str(test_data_file))
    app = Flask(__name__)
    app.register_blueprint(create_tasks_blueprint(task_manager=tm))
    with app.test_client() as client:
        yield client

def test_create_task(client):
    data = {
        "title": "Test tarea",
        "description": "Descripción de prueba",
        "priority": "alta",
        "effort_hours": 2,
        "status": "pendiente",
        "assigned_to": "Juan"
    }
    response = client.post("/tasks", json=data)
    assert response.status_code == 201
    resp_json = response.get_json()
    assert resp_json["title"] == data["title"]
    assert resp_json["priority"] == data["priority"]

def test_get_tasks(client):
    test_create_task(client)
    response = client.get("/tasks")
    assert response.status_code == 200
    resp_json = response.get_json()
    assert isinstance(resp_json, list)
    assert len(resp_json) >= 1

def test_get_task(client):
    test_create_task(client)
    response = client.get("/tasks/1")
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json["id"] == 1

def test_update_task(client):
    test_create_task(client)
    update = {
        "title": "Tarea actualizada",
        "description": "Nueva descripción",
        "priority": "media",
        "effort_hours": 3,
        "status": "en progreso",
        "assigned_to": "Ana"
    }
    response = client.put("/tasks/1", json=update)
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json["title"] == update["title"]
    assert resp_json["priority"] == update["priority"]

def test_delete_task(client):
    test_create_task(client)
    response = client.delete("/tasks/1")
    assert response.status_code == 200


def test_create_task_validation_error(client):
    data = {"title": "Falta campos"}
    response = client.post("/tasks", json=data)
    assert response.status_code == 400


def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task_not_found(client):
    update = {
        "title": "No existe",
        "description": "No existe",
        "priority": "media",
        "effort_hours": 1,
        "status": "pendiente",
        "assigned_to": "Nadie"
    }
    response = client.put("/tasks/999", json=update)
    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404


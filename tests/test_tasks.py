import unittest
from src.main import app
from src.utils import load_tasks, save_tasks
import os

class TaskApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Patch DATA_FILE for testing
        from src import config
        self.test_file = 'test_tasks.json'
        self.original_data_file = config.DATA_FILE
        config.DATA_FILE = self.test_file
        self.sample_tasks = [
            {'id': 1, 'title': 'Tarea 1', 'description': 'Desc 1', 'priority': 'media', 'effort_hours': 2, 'status': 'pendiente', 'assigned_to': 'Juan'},
            {'id': 2, 'title': 'Tarea 2', 'description': 'Desc 2', 'priority': 'alta', 'effort_hours': 3, 'status': 'en progreso', 'assigned_to': 'Ana'}
        ]
        save_tasks(self.sample_tasks)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        from src import config
        config.DATA_FILE = self.original_data_file

    def test_get_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.sample_tasks)

    def test_save_and_load_tasks(self):
        loaded = load_tasks()
        self.assertEqual(loaded, self.sample_tasks)

if __name__ == '__main__':
    unittest.main()

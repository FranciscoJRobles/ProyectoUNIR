from src.models.task import Task
from src.db import db

class TaskManager:
    def add_task(self, data):
        task = Task.from_dict(data)
        db.session.add(task)
        db.session.commit()
        return task

    def get_task(self, task_id):
        return Task.query.get(task_id)

    def get_all_tasks(self):
        return Task.query.all()

    def update_task(self, task_id, updates):
        task = Task.query.get(task_id)
        if not task:
            return None
        # Ignorar campos que no deben actualizarse
        updates = {k: v for k, v in updates.items() if k not in ('id', 'created_at')}
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)
        db.session.commit()
        return task

    def delete_task(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return False
        db.session.delete(task)
        db.session.commit()
        return True
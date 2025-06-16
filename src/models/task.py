from sqlalchemy import Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional
from src.db import db
from src.models.enums import PriorityEnum, StatusEnum

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(SqlEnum(PriorityEnum), nullable=False)
    effort_hours = db.Column(db.Float, nullable=False)
    status = db.Column(SqlEnum(StatusEnum), nullable=False)
    assigned_to = db.Column(db.String(255), nullable=False)
    user_story_id = db.Column(db.Integer, ForeignKey('user_stories.id'), nullable=True)
    user_story = relationship('UserStory', backref='tasks')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'effort_hours': self.effort_hours,
            'status': self.status.value,
            'assigned_to': self.assigned_to,
            'user_story_id': self.user_story_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data['title'],
            description=data['description'],
            priority=PriorityEnum(data['priority']),
            effort_hours=data['effort_hours'],
            status=StatusEnum(data['status']),
            assigned_to=data['assigned_to'],
            user_story_id=data.get('user_story_id')
        )
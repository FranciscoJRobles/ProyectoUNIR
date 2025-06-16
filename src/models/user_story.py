from sqlalchemy import Enum as SqlEnum
from sqlalchemy.sql import func
from src.db import db
from src.models.enums import PriorityEnum

class UserStory(db.Model):
    __tablename__ = 'user_stories'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    goal = db.Column(db.String(255), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(SqlEnum(PriorityEnum), nullable=False)
    story_points = db.Column(db.Integer, nullable=False)
    effort_hours = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'project': self.project,
            'role': self.role,
            'goal': self.goal,
            'reason': self.reason,
            'description': self.description,
            'priority': self.priority.value,
            'story_points': self.story_points,
            'effort_hours': self.effort_hours,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @staticmethod
    def from_dict(data):
        return UserStory(
            project=data['project'],
            role=data['role'],
            goal=data['goal'],
            reason=data['reason'],
            description=data['description'],
            priority=PriorityEnum(data['priority']),
            story_points=data['story_points'],
            effort_hours=data['effort_hours']
        )
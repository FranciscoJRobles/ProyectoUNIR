from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, RootModel
from src.models.user_story import PriorityEnum

class UserStorySchema(BaseModel):
    id: Optional[int] = Field(default=None, serialization_only=True)
    project: str
    role: str
    goal: str
    reason: str
    description: str
    priority: PriorityEnum
    story_points: int
    effort_hours: float
    created_at: Optional[datetime] = Field(default=None, serialization_only=True)

    @field_validator('priority')
    @classmethod
    def priority_must_be_valid(cls, v):
        allowed = [e.value for e in PriorityEnum]
        if v not in allowed:
            raise ValueError(f'priority debe ser uno de {allowed}')
        return v

    @field_validator('story_points')
    @classmethod
    def story_points_range(cls, v):
        if not (1 <= v <= 8):
            raise ValueError('story_points debe estar entre 1 y 8')
        return v

class UserStorySchemas(RootModel[List[UserStorySchema]]):
    pass

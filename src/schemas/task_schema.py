from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, RootModel
from src.models.task import PriorityEnum, StatusEnum

class TaskSchema(BaseModel):
    id: Optional[int] = Field(default=None, serialization_only=True)
    title: str
    description: str
    priority: PriorityEnum
    effort_hours: float
    status: StatusEnum
    assigned_to: str
    user_story_id: Optional[int] = None
    created_at: Optional[datetime] = Field(default=None, serialization_only=True)

    @field_validator('priority')
    @classmethod
    def priority_must_be_valid(cls, v):
        allowed = [e.value for e in PriorityEnum]
        if v not in allowed:
            raise ValueError(f'priority debe ser uno de {allowed}')
        return v

    @field_validator('status')
    @classmethod
    def status_must_be_valid(cls, v):
        allowed = [e.value for e in StatusEnum]
        if v not in allowed:
            raise ValueError(f'status debe ser uno de {allowed}')
        return v

class TaskSchemas(RootModel[List[TaskSchema]]):
    pass

from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional

class PriorityEnum(str, Enum):
    baja = 'baja'
    media = 'media'
    alta = 'alta'
    bloqueante = 'bloqueante'

class StatusEnum(str, Enum):
    pendiente = 'pendiente'
    en_progreso = 'en progreso'
    en_revision = 'en revisión'
    completada = 'completada'

@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: PriorityEnum
    effort_hours: float
    status: StatusEnum
    assigned_to: str

    def to_dict(self):
        d = asdict(self)
        d['priority'] = self.priority.value
        d['status'] = self.status.value
        return d

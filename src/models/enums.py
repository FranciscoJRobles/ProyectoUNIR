from enum import Enum

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

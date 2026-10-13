from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class AsistenciaXEstudiante(BaseModel):
    id: Optional[int] = None
    id_estudiante: int
    id_usuario: int
    id_motivo: int
    fecha: date
    hora_llegada: time
    minutos_tarde: int
    observaciones: str
    estado: Optional[bool] = True
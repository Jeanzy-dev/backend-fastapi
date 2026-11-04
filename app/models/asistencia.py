from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class AsistenciaXEstudiante(BaseModel):
    id: Optional[int] = None
    id_estudiante: int
    id_usuario: Optional[int] = None      # se toma del token (usuario que registra)
    id_motivo: int
    fecha: date
    hora_llegada: time
    minutos_tarde: Optional[int] = None   # si no llega, se calcula con primeraclasexgrupo
    observaciones: Optional[str] = None
    estado: Optional[bool] = True

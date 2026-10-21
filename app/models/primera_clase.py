from pydantic import BaseModel
from typing import Optional
from datetime import time

class PrimeraClase(BaseModel):
    id_clase_grupo: Optional[int] = None
    grado: int
    grupo: str
    jornada: str
    hora_inicio_timbre: time
    hora_cierre_porton: time
    tolerancia_minutos: Optional[int] = None
    estado: Optional[bool] = True
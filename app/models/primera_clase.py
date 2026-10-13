from pydantic import BaseModel
from datetime import time
from typing import Optional

class PrimeraClaseBase(BaseModel):
    grado: int
    grupo: str
    jornada: str
    hora_inicio_timbre: time
    hora_cierre_porton: time
    tolerancia_minutos: Optional[int] = 10

class PrimeraClaseCrear(PrimeraClaseBase):
    pass

class PrimeraClaseRespuesta(PrimeraClaseBase):
    id_clase_grupo: int
    estado: bool

    class Config:
        from_attributes = True
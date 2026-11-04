from pydantic import BaseModel
from typing import Optional

class Estudiante(BaseModel):
    id_estudiante: Optional[int] = None
    documento: str
    nombres: str
    apellidos: str
    grado: int
    grupo: str
    jornada: str
    id_curso: Optional[int] = None   # se resuelve solo a partir de grado/grupo/jornada
    estado: Optional[bool] = True

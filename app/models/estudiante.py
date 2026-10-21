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
    estado: Optional[bool] = True
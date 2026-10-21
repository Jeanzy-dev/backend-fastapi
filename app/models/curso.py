from pydantic import BaseModel
from typing import Optional

class Curso(BaseModel):
    id_curso: Optional[int] = None
    grado: int
    grupo: str
    jornada: str
    estado: Optional[bool] = True
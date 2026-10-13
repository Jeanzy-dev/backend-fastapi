from pydantic import BaseModel
from typing import Optional

class Coordinador(BaseModel):
    id_coordinador: Optional[int] = None
    id_usuario: int
    jornada_asignada: str
    telefono_oficina: str
    estado: Optional[bool] = True
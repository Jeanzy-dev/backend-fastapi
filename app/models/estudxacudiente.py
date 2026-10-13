from pydantic import BaseModel
from typing import Optional

class EstudXAcudiente(BaseModel):
    id: Optional[int] = None
    id_estudiante: int
    id_acudiente: int
    parentesco: str
    es_principal: bool
    estado: Optional[bool] = True
from pydantic import BaseModel
from typing import Optional

class MotivoTardanza(BaseModel):
    id_motivo: Optional[int] = None
    descripcion: str
    es_justificable: Optional[bool] = False
    estado: Optional[bool] = True
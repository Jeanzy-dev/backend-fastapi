from pydantic import BaseModel
from typing import Optional

class ModuloxRol(BaseModel):
    id: Optional[int] = None
    id_perfil: int
    id_modulo: int
    estado: Optional[bool] = True
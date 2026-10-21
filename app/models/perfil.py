from pydantic import BaseModel
from typing import Optional

class Perfil(BaseModel):
    id_perfil: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[bool] = True
from pydantic import BaseModel
from typing import Optional

class PerfilBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class PerfilCrear(PerfilBase):
    pass

class PerfilRespuesta(PerfilBase):
    id_perfil: int
    estado: bool

    class Config:
        from_attributes = True
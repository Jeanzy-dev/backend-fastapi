from pydantic import BaseModel
from typing import Optional

class ModuloBase(BaseModel):
    nombre: str
    ruta_url: str
    icono: Optional[str] = None

class ModuloCrear(ModuloBase):
    pass

class ModuloRespuesta(ModuloBase):
    id_modulo: int
    estado: bool

    class Config:
        from_attributes = True
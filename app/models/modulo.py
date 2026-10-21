from pydantic import BaseModel
from typing import Optional

class Modulo(BaseModel):
    id_modulo: Optional[int] = None
    nombre: str
    ruta_url: str
    icono: Optional[str] = None
    estado: Optional[bool] = True
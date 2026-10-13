from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    id_perfil: int
    nombre_completo: str
    correo: str
    password_hash: str
    estado: Optional[bool] = True
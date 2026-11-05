from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    id_perfil: int
    nombre_completo: str
    correo: str
    password: Optional[str] = None   # texto plano: el repositorio la encripta (obligatoria al crear)
    estado: Optional[bool] = True

from pydantic import BaseModel
from typing import Optional

class Acudiente(BaseModel):
    id_acudiente: Optional[int] = None
    documento: str
    nombres: str
    apellidos: str
    telefono: str
    correo: str
    estado: Optional[bool] = True
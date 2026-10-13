from pydantic import BaseModel
from typing import Optional

class RegistroNotificaciones(BaseModel):
    id_notificacion: Optional[int] = None
    id_estudiante: int
    total_tardanzas: int
    correo_destinatario: str
    asunto: str
    estado_envio: str
    estado: Optional[bool] = True
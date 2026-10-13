from pydantic import BaseModel

class MotivoBase(BaseModel):
    descripcion: str
    es_justificable: bool = False

class MotivoCrear(MotivoBase):
    pass

class MotivoRespuesta(MotivoBase):
    id_motivo: int
    estado: bool

    class Config:
        from_attributes = True
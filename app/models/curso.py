from pydantic import BaseModel

class CursoBase(BaseModel):
    grado: int
    grupo: str
    jornada: str

class CursoCrear(CursoBase):
    pass

class CursoRespuesta(CursoBase):
    id_curso: int
    estado: bool

    class Config:
        from_attributes = True
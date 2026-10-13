from pydantic import BaseModel

class EstudianteBase(BaseModel):
    documento: str
    nombres: str
    apellidos: str
    grado: int
    grupo: str
    jornada: str

class EstudianteCrear(EstudianteBase):
    pass

class EstudianteRespuesta(EstudianteBase):
    id_estudiante: int
    estado: bool

    class Config:
        from_attributes = True
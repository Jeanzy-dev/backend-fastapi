from pydantic import BaseModel, EmailStr

class AcudienteBase(BaseModel):
    documento: str
    nombres: str
    apellidos: str
    telefono: str
    correo: str

class AcudienteCrear(AcudienteBase):
    pass

class AcudienteRespuesta(AcudienteBase):
    id_acudiente: int
    estado: bool

    class Config:
        from_attributes = True
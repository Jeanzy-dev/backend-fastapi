from pydantic import BaseModel

class LoginData(BaseModel):
    correo: str
    password: str



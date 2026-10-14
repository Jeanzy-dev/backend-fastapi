from pydantic import BaseModel

class LoginData(BaseModel):
    correo: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    mensaje: str
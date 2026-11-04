from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    mensaje: str
    usuario: dict
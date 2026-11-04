from fastapi import APIRouter, Depends
from app.core.security import verificar_token
from app.models.auth import LoginData, TokenResponse
from app.repositories.auth_repo import AuthRepository

router = APIRouter(prefix="/api/auth", tags=["Autenticación y Login"])
repo = AuthRepository()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginData):
    return repo.autenticar_usuario(data)

@router.get("/me")
def sesion_actual(sesion: dict = Depends(verificar_token)):
    # Sirve al frontend para comprobar que el token sigue vigente
    return sesion

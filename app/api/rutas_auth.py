from fastapi import APIRouter
from app.models.auth import LoginData, TokenResponse
from app.repositories.auth import AuthRepository

router = APIRouter(prefix="/auth", tags=["Autenticación y Login"])
repo = AuthRepository()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginData):
    return repo.autenticar_usuario(data)
import os
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_si_falla_el_env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas: cubre la jornada de la coordinadora

esquema_bearer = HTTPBearer(auto_error=False)


# ---------- Contraseñas (bcrypt directo; passlib ya no funciona con bcrypt 4.1+) ----------
def encriptar_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        # El valor guardado no es un hash bcrypt válido (por ejemplo, texto plano)
        return False


# ---------- JWT ----------
def crear_token_acceso(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(credenciales: HTTPAuthorizationCredentials = Depends(esquema_bearer)):
    """Dependencia: protege las rutas. Devuelve los datos guardados en el token."""
    if credenciales is None:
        raise HTTPException(status_code=401, detail="Debe iniciar sesión")
    try:
        return jwt.decode(credenciales.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="La sesión expiró, ingrese de nuevo")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

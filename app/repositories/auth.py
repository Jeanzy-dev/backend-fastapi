from fastapi import HTTPException
from app.core.database import Database
from app.core.security import crear_token_acceso
from passlib.context import CryptContext
from app.models.auth import LoginData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthRepository:
    def __init__(self):
        self.db = Database()

    def autenticar_usuario(self, data: LoginData):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Usuario WHERE correo = %s;", (data.correo,))
        usuario = cursor.fetchone()
        conn.close()

        if not usuario:
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
        
        if not usuario['estado']:
            raise HTTPException(status_code=403, detail="Este usuario está inactivo o fue eliminado")
        
        if not pwd_context.verify(data.password, usuario['password_hash']):
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
        
        token_data = {"sub": str(usuario['id_usuario']), "correo": usuario['correo']}
        token = crear_token_acceso(data=token_data)
        
        return {
            "access_token": token, 
            "token_type": "bearer",
            "mensaje": "Login coronado, estás adentro"
        }
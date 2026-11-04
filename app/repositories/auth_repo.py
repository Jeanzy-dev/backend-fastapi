from fastapi import HTTPException
from app.core.database import Database
from app.core.security import crear_token_acceso, verificar_password
from app.models.auth import LoginData

class AuthRepository:
    def __init__(self):
        self.db = Database()

    def autenticar_usuario(self, data: LoginData):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.*, p.nombre AS perfil, p.estado AS perfil_activo
            FROM usuario u JOIN perfil p ON p.id_perfil = u.id_perfil
            WHERE LOWER(u.correo) = LOWER(%s);
        """, (data.correo.strip(),))
        usuario = cursor.fetchone()
        conn.close()

        if not usuario or not verificar_password(data.password, usuario['password_hash']):
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

        if not usuario['estado'] or not usuario['perfil_activo']:
            raise HTTPException(status_code=403, detail="Este usuario está inactivo")

        # El perfil viaja en el token para saber qué módulos puede ver
        token_data = {
            "sub": str(usuario['id_usuario']),
            "correo": usuario['correo'],
            "id_perfil": usuario['id_perfil'],
            "perfil": usuario['perfil']
        }
        token = crear_token_acceso(data=token_data)

        return {
            "access_token": token,
            "token_type": "bearer",
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id_usuario": usuario['id_usuario'],
                "nombre_completo": usuario['nombre_completo'],
                "correo": usuario['correo'],
                "id_perfil": usuario['id_perfil'],
                "perfil": usuario['perfil']
            }
        }

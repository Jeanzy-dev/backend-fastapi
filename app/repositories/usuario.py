from app.core.database import Database
from app.models.usuario import Usuario
from passlib.context import CryptContext

class UsuarioRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE estado = true ORDER BY id_usuario ASC;")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def obtener_por_id(self, id_usuario: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE id_usuario = %s AND estado = true;", (id_usuario,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def crear(self, usuario: Usuario):
        contrasena_hasheada = pwd_context.hash(usuario.password_hash)

        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Usuario (id_perfil, nombre_completo, correo, password_hash, estado, creado, actualizado) 
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id_usuario;
        """
        
        cursor.execute(query, (
            usuario.id_perfil, 
            usuario.nombre_completo, 
            usuario.correo, 
            contrasena_hasheada, 
            usuario.estado
        ))
        
        nuevo_id = cursor.fetchone()['id_usuario']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, id_usuario: int, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Usuario
            SET id_perfil = %s, nombre_completo = %s, correo = %s, password_hash = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id_usuario = %s AND estado = true
            RETURNING id_usuario;
        """
        cursor.execute(query, (usuario.id_perfil, usuario.nombre_completo, usuario.correo, usuario.password_hash, id_usuario))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, id_usuario: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Usuario SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_usuario = %s RETURNING id_usuario;", (id_usuario,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None
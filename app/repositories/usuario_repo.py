from app.core.database import Database
from app.core.security import encriptar_password
from app.models.usuario import Usuario

class UsuarioRepository:
    def __init__(self):
        self.db = Database()

    # Nunca se devuelve password_hash al frontend
    COLUMNAS = """u.id_usuario, u.id_perfil, u.nombre_completo, u.correo, u.estado,
                  u.creado, u.actualizado, p.nombre AS perfil"""

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT {self.COLUMNAS}
            FROM usuario u JOIN perfil p ON p.id_perfil = u.id_perfil
            WHERE u.estado = true ORDER BY u.nombre_completo;
        """)
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def obtener_por_id(self, id_usuario: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT {self.COLUMNAS}
            FROM usuario u JOIN perfil p ON p.id_perfil = u.id_perfil
            WHERE u.id_usuario = %s AND u.estado = true;
        """, (id_usuario,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def crear(self, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO usuario (id_perfil, nombre_completo, correo, password_hash)
            VALUES (%s, %s, %s, %s) RETURNING id_usuario;
        """
        cursor.execute(query, (usuario.id_perfil, usuario.nombre_completo, usuario.correo,
                               encriptar_password(usuario.password)))
        nuevo_id = cursor.fetchone()['id_usuario']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, id_usuario: int, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # La contraseña solo cambia si se envía una nueva (y se guarda encriptada)
        nuevo_hash = encriptar_password(usuario.password) if usuario.password else None
        query = """
            UPDATE usuario
            SET id_perfil = %s, nombre_completo = %s, correo = %s,
                password_hash = COALESCE(%s, password_hash), actualizado = CURRENT_TIMESTAMP
            WHERE id_usuario = %s AND estado = true
            RETURNING id_usuario;
        """
        cursor.execute(query, (usuario.id_perfil, usuario.nombre_completo, usuario.correo, nuevo_hash, id_usuario))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, id_usuario: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_usuario = %s AND estado = true RETURNING id_usuario;", (id_usuario,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

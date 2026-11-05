from app.core.database import Database
from app.models.perfil import Perfil

class PerfilRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM perfil WHERE estado = true ORDER BY nombre ASC;")
        perfiles = cursor.fetchall()
        conn.close()
        return perfiles

    def obtener_por_id(self, perfil_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM perfil WHERE id_perfil = %s AND estado = true;", (perfil_id,))
        perfil = cursor.fetchone()
        conn.close()
        return perfil

    def crear(self, perfil: Perfil):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO perfil (nombre, descripcion)
            VALUES (%s, %s) RETURNING id_perfil;
        """
        cursor.execute(query, (perfil.nombre, perfil.descripcion))
        nuevo_id = cursor.fetchone()['id_perfil']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, perfil_id: int, perfil: Perfil):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE perfil
            SET nombre = %s, descripcion = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id_perfil = %s AND estado = true
            RETURNING id_perfil;
        """
        cursor.execute(query, (perfil.nombre, perfil.descripcion, perfil_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, perfil_id: int):
        # Borrado lógico: no se borra la fila, se cambia el estado
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE perfil SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_perfil = %s AND estado = true RETURNING id_perfil;", (perfil_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

from app.core.database import Database
from app.models.perfil import Perfil

class PerfilRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM perfil ORDER BY id_perfil ASC;")
        perfiles = cursor.fetchall()
        conn.close()
        return perfiles

    def obtener_por_id(self, perfil_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM perfil WHERE id_perfil = %s;", (perfil_id,))
        perfil = cursor.fetchone()
        conn.close()
        return perfil

    def crear(self, perfil: Perfil):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO perfil (nombre, descripcion, estado)
            VALUES (%s, %s, %s) RETURNING id_perfil;
        """
        cursor.execute(query, (perfil.nombre, perfil.descripcion, perfil.estado))
        nuevo_id = cursor.fetchone()['id_perfil']
        conn.commit()
        conn.close()
        return nuevo_id

    def eliminar(self, perfil_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM perfil WHERE id_perfil = %s RETURNING id_perfil;", (perfil_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

    def actualizar(self, perfil_id: int, perfil: Perfil):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE perfil
            SET nombre = %s, descripcion = %s, estado = %s
            WHERE id_perfil = %s
            RETURNING id_perfil;
        """
        cursor.execute(query, (perfil.nombre, perfil.descripcion, perfil.estado, perfil_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None
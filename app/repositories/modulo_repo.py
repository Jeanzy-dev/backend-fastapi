from app.core.database import Database
from app.models.modulo import Modulo

class ModuloRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM modulos WHERE estado = true ORDER BY nombre ASC;")
        modulos = cursor.fetchall()
        conn.close()
        return modulos

    def obtener_por_id(self, modulo_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM modulos WHERE id_modulo = %s AND estado = true;", (modulo_id,))
        modulo = cursor.fetchone()
        conn.close()
        return modulo

    def crear(self, modulo: Modulo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO modulos (nombre, ruta_url, icono)
            VALUES (%s, %s, %s) RETURNING id_modulo;
        """
        cursor.execute(query, (modulo.nombre, modulo.ruta_url, modulo.icono))
        nuevo_id = cursor.fetchone()['id_modulo']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, modulo_id: int, modulo: Modulo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE modulos
            SET nombre = %s, ruta_url = %s, icono = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id_modulo = %s AND estado = true
            RETURNING id_modulo;
        """
        cursor.execute(query, (modulo.nombre, modulo.ruta_url, modulo.icono, modulo_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, modulo_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE modulos SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_modulo = %s AND estado = true RETURNING id_modulo;", (modulo_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

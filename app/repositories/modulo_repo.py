from app.core.database import Database
from app.models.modulo import Modulo

class ModuloRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Modulos ORDER BY id_modulo ASC;")
        modulos = cursor.fetchall()
        conn.close()
        return modulos

    def obtener_por_id(self, modulo_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Modulos WHERE id_modulo = %s;", (modulo_id,))
        modulo = cursor.fetchone()
        conn.close()
        return modulo

    def crear(self, modulo: Modulo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Modulos (nombre, ruta_url, icono, estado)
            VALUES (%s, %s, %s, %s) RETURNING id_modulo;
        """
        cursor.execute(query, (modulo.nombre, modulo.ruta_url, modulo.icono, modulo.estado))
        nuevo_id = cursor.fetchone()['id_modulo']
        conn.commit()
        conn.close()
        return nuevo_id

    def eliminar(self, modulo_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Modulos WHERE id_modulo = %s RETURNING id_modulo;", (modulo_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

    def actualizar(self, modulo_id: int, modulo: Modulo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Modulos
            SET nombre = %s, ruta_url = %s, icono = %s, estado = %s
            WHERE id_modulo = %s
            RETURNING id_modulo;
        """
        cursor.execute(query, (modulo.nombre, modulo.ruta_url, modulo.icono, modulo.estado, modulo_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None
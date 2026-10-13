from app.core.database import Database
from app.models.modulo import ModuloCrear

class ModuloRepository:
    def __init__(self):
        self.db = Database()

    # 1. Listar solo los activos
    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Modulos WHERE estado = TRUE ORDER BY id_modulo ASC;")
        modulos = cursor.fetchall()
        cursor.close()
        conn.close()
        return modulos

    # 2. Obtener por ID
    def obtener_por_id(self, id_modulo: int):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Modulos WHERE id_modulo = %s AND estado = TRUE;", (id_modulo,))
        modulo = cursor.fetchone()
        cursor.close()
        conn.close()
        return modulo

    # 3. Crear nuevo módulo
    def crear(self, modulo: ModuloCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Modulos (nombre, ruta_url, icono)
            VALUES (%s, %s, %s)
            RETURNING id_modulo;
        """
        cursor.execute(query, (modulo.nombre, modulo.ruta_url, modulo.icono))
        nuevo_id = cursor.fetchone()['id_modulo']
        conn.commit()
        cursor.close()
        conn.close()
        return nuevo_id

    # 4. Actualizar módulo
    def actualizar(self, id_modulo: int, modulo: ModuloCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Modulos
            SET nombre = %s, ruta_url = %s, icono = %s
            WHERE id_modulo = %s AND estado = TRUE
            RETURNING id_modulo;
        """
        cursor.execute(query, (modulo.nombre, modulo.ruta_url, modulo.icono, id_modulo))
        actualizado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return actualizado is not None

    # 5. Soft Delete (desactivar)
    def eliminar_logico(self, id_modulo: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Modulos
            SET estado = FALSE
            WHERE id_modulo = %s AND estado = TRUE
            RETURNING id_modulo;
        """
        cursor.execute(query, (id_modulo,))
        eliminado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return eliminado is not None
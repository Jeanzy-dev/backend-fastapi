from app.core.database import Database
from app.models.acudiente import Acudiente

class AcudienteRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM acudiente ORDER BY id_acudiente ASC;")
        acudientes = cursor.fetchall()
        conn.close()
        return acudientes

    def obtener_por_id(self, acudiente_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM acudiente WHERE id_acudiente = %s;", (acudiente_id,))
        acudiente = cursor.fetchone()
        conn.close()
        return acudiente

    def crear(self, acudiente: Acudiente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO acudiente (documento, nombres, apellidos, telefono, correo, estado)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_acudiente;
        """
        cursor.execute(query, (
            acudiente.documento, acudiente.nombres, acudiente.apellidos,
            acudiente.telefono, acudiente.correo, acudiente.estado
        ))
        nuevo_id = cursor.fetchone()['id_acudiente']
        conn.commit()
        conn.close()
        return nuevo_id

    def eliminar(self, acudiente_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM acudiente WHERE id_acudiente = %s RETURNING id_acudiente;", (acudiente_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

    def actualizar(self, acudiente_id: int, acudiente: Acudiente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE acudiente
            SET documento = %s, nombres = %s, apellidos = %s, telefono = %s, correo = %s, estado = %s
            WHERE id_acudiente = %s
            RETURNING id_acudiente;
        """
        cursor.execute(query, (
            acudiente.documento, acudiente.nombres, acudiente.apellidos,
            acudiente.telefono, acudiente.correo, acudiente.estado, acudiente_id
        ))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None
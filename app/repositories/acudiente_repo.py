from app.core.database import Database
from app.models.acudiente import AcudienteCrear

class AcudienteRepository:
    def __init__(self):
        self.db = Database()

    # 1. Listar solo activos
    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM acudiente WHERE estado = TRUE ORDER BY id_acudiente ASC;")
        acudientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return acudientes

    # 2. Obtener por ID
    def obtener_por_id(self, id_acudiente: int):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM acudiente WHERE id_acudiente = %s AND estado = TRUE;", (id_acudiente,))
        acudiente = cursor.fetchone()
        cursor.close()
        conn.close()
        return acudiente

    # 3. Crear acudiente
    def crear(self, acudiente: AcudienteCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO acudiente (documento, nombres, apellidos, telefono, correo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_acudiente;
        """
        cursor.execute(query, (
            acudiente.documento,
            acudiente.nombres,
            acudiente.apellidos,
            acudiente.telefono,
            acudiente.correo
        ))
        nuevo_id = cursor.fetchone()['id_acudiente']
        conn.commit()
        cursor.close()
        conn.close()
        return nuevo_id

    # 4. Actualizar acudiente
    def actualizar(self, id_acudiente: int, acudiente: AcudienteCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE acudiente
            SET documento = %s, nombres = %s, apellidos = %s, telefono = %s, correo = %s
            WHERE id_acudiente = %s AND estado = TRUE
            RETURNING id_acudiente;
        """
        cursor.execute(query, (
            acudiente.documento,
            acudiente.nombres,
            acudiente.apellidos,
            acudiente.telefono,
            acudiente.correo,
            id_acudiente
        ))
        actualizado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return actualizado is not None

    # 5. Soft Delete
    def eliminar_logico(self, id_acudiente: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE acudiente
            SET estado = FALSE
            WHERE id_acudiente = %s AND estado = TRUE
            RETURNING id_acudiente;
        """
        cursor.execute(query, (id_acudiente,))
        eliminado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return eliminado is not None
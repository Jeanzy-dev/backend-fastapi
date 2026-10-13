from app.core.database import Database
from app.models.estudxacudiente import EstudXAcudiente

class EstudXAcudienteRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudXacudiente WHERE estado = true ORDER BY id ASC;")
        registros = cursor.fetchall()
        conn.close()
        return registros

    def obtener_por_id(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudXacudiente WHERE id = %s AND estado = true;", (id_registro,))
        registro = cursor.fetchone()
        conn.close()
        return registro

    def crear(self, registro: EstudXAcudiente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO estudXacudiente (id_estudiante, id_acudiente, parentesco, es_principal, estado, creado, actualizado) 
            VALUES (%s, %s, %s, %s, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id;
        """
        cursor.execute(query, (registro.id_estudiante, registro.id_acudiente, registro.parentesco, registro.es_principal))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, id_registro: int, registro: EstudXAcudiente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE estudXacudiente
            SET id_estudiante = %s, id_acudiente = %s, parentesco = %s, es_principal = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id = %s AND estado = true
            RETURNING id;
        """
        cursor.execute(query, (registro.id_estudiante, registro.id_acudiente, registro.parentesco, registro.es_principal, id_registro))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE estudXacudiente SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id = %s RETURNING id;", (id_registro,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None
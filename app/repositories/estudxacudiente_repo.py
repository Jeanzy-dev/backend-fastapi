from app.core.database import Database
from app.models.estudxacudiente import EstudXAcudiente

class EstudXAcudienteRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # JOIN para devolver nombres: el frontend no debe mostrar IDs
        cursor.execute("""
            SELECT ea.*,
                   e.nombres || ' ' || e.apellidos AS estudiante,
                   e.grado, e.grupo,
                   a.nombres || ' ' || a.apellidos AS acudiente,
                   a.telefono, a.correo
            FROM estudxacudiente ea
            JOIN estudiantexcurso e ON e.id_estudiante = ea.id_estudiante
            JOIN acudiente a ON a.id_acudiente = ea.id_acudiente
            WHERE ea.estado = true AND e.estado = true AND a.estado = true
            ORDER BY e.apellidos, e.nombres;
        """)
        registros = cursor.fetchall()
        conn.close()
        return registros

    def obtener_por_id(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudxacudiente WHERE id = %s AND estado = true;", (id_registro,))
        registro = cursor.fetchone()
        conn.close()
        return registro

    def crear(self, registro: EstudXAcudiente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Si este acudiente queda como principal, los demás del estudiante dejan de serlo
        if registro.es_principal:
            cursor.execute("UPDATE estudxacudiente SET es_principal = false, actualizado = CURRENT_TIMESTAMP WHERE id_estudiante = %s AND estado = true;", (registro.id_estudiante,))
        query = """
            INSERT INTO estudxacudiente (id_estudiante, id_acudiente, parentesco, es_principal)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """
        cursor.execute(query, (registro.id_estudiante, registro.id_acudiente, registro.parentesco, registro.es_principal))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, id_registro: int, registro: EstudXAcudiente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        if registro.es_principal:
            cursor.execute("UPDATE estudxacudiente SET es_principal = false, actualizado = CURRENT_TIMESTAMP WHERE id_estudiante = %s AND id <> %s AND estado = true;", (registro.id_estudiante, id_registro))
        query = """
            UPDATE estudxacudiente
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
        cursor.execute("UPDATE estudxacudiente SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id = %s AND estado = true RETURNING id;", (id_registro,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

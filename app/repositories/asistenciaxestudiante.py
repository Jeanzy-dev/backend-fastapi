from app.core.database import Database
from app.models.asistenciaxestud import AsistenciaXEstudiante

class AsistenciaXEstudRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM asistenciaXestudiante WHERE estado = true ORDER BY id ASC;")
        registros = cursor.fetchall()
        conn.close()
        return registros

    def obtener_por_id(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM asistenciaXestudiante WHERE id = %s AND estado = true;", (id_registro,))
        registro = cursor.fetchone()
        conn.close()
        return registro

    def crear(self, registro: AsistenciaXEstudiante):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO asistenciaXestudiante (id_estudiante, id_usuario, id_motivo, fecha, hora_llegada, minutos_tarde, observaciones, estado, creado, actualizado) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id;
        """
        cursor.execute(query, (registro.id_estudiante, registro.id_usuario, registro.id_motivo, registro.fecha, registro.hora_llegada, registro.minutos_tarde, registro.observaciones))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, id_registro: int, registro: AsistenciaXEstudiante):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE asistenciaXestudiante
            SET id_estudiante = %s, id_usuario = %s, id_motivo = %s, fecha = %s, hora_llegada = %s, minutos_tarde = %s, observaciones = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id = %s AND estado = true
            RETURNING id;
        """
        cursor.execute(query, (registro.id_estudiante, registro.id_usuario, registro.id_motivo, registro.fecha, registro.hora_llegada, registro.minutos_tarde, registro.observaciones, id_registro))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE asistenciaXestudiante SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id = %s RETURNING id;", (id_registro,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None
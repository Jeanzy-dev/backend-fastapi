from app.core.database import Database
from app.models.registronotificacion import RegistroNotificaciones

class RegistroNotificacionRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Registro_notificaciones WHERE estado = true ORDER BY id_notificacion ASC;")
        registros = cursor.fetchall()
        conn.close()
        return registros

    def obtener_por_id(self, id_notificacion: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Registro_notificaciones WHERE id_notificacion = %s AND estado = true;", (id_notificacion,))
        registro = cursor.fetchone()
        conn.close()
        return registro

    def crear(self, registro: RegistroNotificaciones):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Registro_notificaciones (id_estudiante, total_tardanzas, correo_destinatario, asunto, estado_envio, estado, creado, actualizado) 
            VALUES (%s, %s, %s, %s, %s, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id_notificacion;
        """
        cursor.execute(query, (registro.id_estudiante, registro.total_tardanzas, registro.correo_destinatario, registro.asunto, registro.estado_envio))
        nuevo_id = cursor.fetchone()['id_notificacion']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, id_notificacion: int, registro: RegistroNotificaciones):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Registro_notificaciones
            SET id_estudiante = %s, total_tardanzas = %s, correo_destinatario = %s, asunto = %s, estado_envio = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id_notificacion = %s AND estado = true
            RETURNING id_notificacion;
        """
        cursor.execute(query, (registro.id_estudiante, registro.total_tardanzas, registro.correo_destinatario, registro.asunto, registro.estado_envio, id_notificacion))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, id_notificacion: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Registro_notificaciones SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_notificacion = %s RETURNING id_notificacion;", (id_notificacion,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None
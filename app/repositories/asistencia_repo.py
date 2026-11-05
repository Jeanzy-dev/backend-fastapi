import os
from app.core.database import Database
from app.models.asistencia import AsistenciaXEstudiante

# Cada cuántas llegadas tarde se genera una alerta al acudiente (3, 6, 9...)
TARDANZAS_PARA_ALERTA = int(os.getenv("TARDANZAS_ALERTA", "3"))

class AsistenciaXEstudRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self, desde=None, hasta=None, id_estudiante=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # JOIN con estudiante, motivo y usuario para devolver nombres en lugar de IDs
        query = """
            SELECT a.*,
                   e.documento, e.nombres || ' ' || e.apellidos AS estudiante,
                   e.grado, e.grupo, e.jornada,
                   m.descripcion AS motivo, m.es_justificable,
                   u.nombre_completo AS registrado_por
            FROM asistenciaxestudiante a
            JOIN estudiantexcurso e ON e.id_estudiante = a.id_estudiante
            JOIN motivo_tardanza m ON m.id_motivo = a.id_motivo
            LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
            WHERE a.estado = true
              AND (%s::date IS NULL OR a.fecha >= %s::date)
              AND (%s::date IS NULL OR a.fecha <= %s::date)
              AND (%s::int IS NULL OR a.id_estudiante = %s::int)
            ORDER BY a.fecha DESC, a.hora_llegada DESC;
        """
        cursor.execute(query, (desde, desde, hasta, hasta, id_estudiante, id_estudiante))
        registros = cursor.fetchall()
        conn.close()
        return registros

    def obtener_por_id(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM asistenciaxestudiante WHERE id = %s AND estado = true;", (id_registro,))
        registro = cursor.fetchone()
        conn.close()
        return registro

    def _calcular_minutos_tarde(self, cursor, id_estudiante, hora_llegada):
        """Minutos entre el timbre de la primera clase del grupo y la hora de llegada."""
        cursor.execute("""
            SELECT GREATEST(0, EXTRACT(EPOCH FROM (%s::time - p.hora_inicio_timbre)) / 60)::int AS minutos
            FROM estudiantexcurso e
            JOIN primeraclasexgrupo p
              ON p.grado = e.grado AND p.grupo = e.grupo AND p.jornada = e.jornada AND p.estado = true
            WHERE e.id_estudiante = %s
            LIMIT 1;
        """, (hora_llegada, id_estudiante))
        fila = cursor.fetchone()
        return fila['minutos'] if fila else 0

    def _generar_alerta_si_aplica(self, cursor, id_estudiante):
        """Si el estudiante completa 3, 6, 9... tardanzas, deja una notificación PENDIENTE
        para el acudiente principal (el servicio de correos la envía después)."""
        cursor.execute("SELECT COUNT(*) AS total FROM asistenciaxestudiante WHERE id_estudiante = %s AND estado = true;", (id_estudiante,))
        total = cursor.fetchone()['total']
        if total == 0 or total % TARDANZAS_PARA_ALERTA != 0:
            return None
        cursor.execute("""
            SELECT a.correo, e.nombres || ' ' || e.apellidos AS estudiante
            FROM estudxacudiente ea
            JOIN acudiente a ON a.id_acudiente = ea.id_acudiente AND a.estado = true
            JOIN estudiantexcurso e ON e.id_estudiante = ea.id_estudiante
            WHERE ea.id_estudiante = %s AND ea.estado = true
            ORDER BY ea.es_principal DESC NULLS LAST, ea.id ASC
            LIMIT 1;
        """, (id_estudiante,))
        acudiente = cursor.fetchone()
        if not acudiente:
            return {"total_tardanzas": total, "notificacion_creada": False,
                    "motivo": "El estudiante no tiene acudiente registrado"}
        asunto = f"Alerta de llegadas tarde: {acudiente['estudiante']} ({total} tardanzas)"
        cursor.execute("""
            INSERT INTO registro_notificaciones (id_estudiante, total_tardanzas, correo_destinatario, asunto, estado_envio)
            VALUES (%s, %s, %s, %s, 'PENDIENTE') RETURNING id_notificacion;
        """, (id_estudiante, total, acudiente['correo'], asunto))
        return {"total_tardanzas": total, "notificacion_creada": True, "correo": acudiente['correo']}

    def crear(self, registro: AsistenciaXEstudiante):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        minutos = registro.minutos_tarde
        if minutos is None:
            minutos = self._calcular_minutos_tarde(cursor, registro.id_estudiante, registro.hora_llegada)
        query = """
            INSERT INTO asistenciaxestudiante (id_estudiante, id_usuario, id_motivo, fecha, hora_llegada, minutos_tarde, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        cursor.execute(query, (registro.id_estudiante, registro.id_usuario, registro.id_motivo, registro.fecha,
                               registro.hora_llegada, minutos, registro.observaciones))
        nuevo_id = cursor.fetchone()['id']
        alerta = self._generar_alerta_si_aplica(cursor, registro.id_estudiante)
        conn.commit()
        conn.close()
        return nuevo_id, minutos, alerta

    def actualizar(self, id_registro: int, registro: AsistenciaXEstudiante):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        minutos = registro.minutos_tarde
        if minutos is None:
            minutos = self._calcular_minutos_tarde(cursor, registro.id_estudiante, registro.hora_llegada)
        query = """
            UPDATE asistenciaxestudiante
            SET id_estudiante = %s, id_motivo = %s, fecha = %s, hora_llegada = %s, minutos_tarde = %s,
                observaciones = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id = %s AND estado = true
            RETURNING id;
        """
        cursor.execute(query, (registro.id_estudiante, registro.id_motivo, registro.fecha, registro.hora_llegada,
                               minutos, registro.observaciones, id_registro))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE asistenciaxestudiante SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id = %s AND estado = true RETURNING id;", (id_registro,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

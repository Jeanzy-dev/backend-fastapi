from app.core.database import Database

class ReporteRepository:
    """Consultas de solo lectura para tableros (coordinadora y rector)."""
    def __init__(self):
        self.db = Database()

    def resumen(self, desde, hasta):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        rango = (desde, hasta)

        cursor.execute("""
            SELECT COUNT(*) AS total_tardanzas,
                   COUNT(DISTINCT a.id_estudiante) AS estudiantes_distintos,
                   COALESCE(ROUND(AVG(a.minutos_tarde), 1), 0) AS promedio_minutos,
                   COUNT(*) FILTER (WHERE m.es_justificable) AS justificadas
            FROM asistenciaxestudiante a
            JOIN motivo_tardanza m ON m.id_motivo = a.id_motivo
            WHERE a.estado = true AND a.fecha BETWEEN %s AND %s;
        """, rango)
        totales = cursor.fetchone()

        cursor.execute("""
            SELECT a.fecha, COUNT(*) AS total
            FROM asistenciaxestudiante a
            WHERE a.estado = true AND a.fecha BETWEEN %s AND %s
            GROUP BY a.fecha ORDER BY a.fecha;
        """, rango)
        por_dia = cursor.fetchall()

        cursor.execute("""
            SELECT e.grado || '°' || e.grupo || ' ' || e.jornada AS curso, COUNT(*) AS total
            FROM asistenciaxestudiante a
            JOIN estudiantexcurso e ON e.id_estudiante = a.id_estudiante
            WHERE a.estado = true AND a.fecha BETWEEN %s AND %s
            GROUP BY e.grado, e.grupo, e.jornada ORDER BY total DESC;
        """, rango)
        por_curso = cursor.fetchall()

        cursor.execute("""
            SELECT m.descripcion AS motivo, COUNT(*) AS total
            FROM asistenciaxestudiante a
            JOIN motivo_tardanza m ON m.id_motivo = a.id_motivo
            WHERE a.estado = true AND a.fecha BETWEEN %s AND %s
            GROUP BY m.descripcion ORDER BY total DESC;
        """, rango)
        por_motivo = cursor.fetchall()

        cursor.execute("""
            SELECT e.nombres || ' ' || e.apellidos AS estudiante,
                   e.grado || '°' || e.grupo AS curso, COUNT(*) AS total
            FROM asistenciaxestudiante a
            JOIN estudiantexcurso e ON e.id_estudiante = a.id_estudiante
            WHERE a.estado = true AND a.fecha BETWEEN %s AND %s
            GROUP BY e.id_estudiante, e.nombres, e.apellidos, e.grado, e.grupo
            ORDER BY total DESC LIMIT 10;
        """, rango)
        top_estudiantes = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS pendientes FROM registro_notificaciones WHERE estado = true AND estado_envio = 'PENDIENTE';")
        pendientes = cursor.fetchone()['pendientes']

        conn.close()
        return {
            "desde": desde, "hasta": hasta,
            "totales": totales,
            "notificaciones_pendientes": pendientes,
            "por_dia": por_dia,
            "por_curso": por_curso,
            "por_motivo": por_motivo,
            "top_estudiantes": top_estudiantes
        }

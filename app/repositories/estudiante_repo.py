from app.core.database import Database
from app.models.estudiante import Estudiante

class EstudianteRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Se agrega el total de tardanzas para que la coordinadora lo vea al buscar
        cursor.execute("""
            SELECT e.*,
                   (SELECT COUNT(*) FROM asistenciaxestudiante a
                     WHERE a.id_estudiante = e.id_estudiante AND a.estado = true) AS total_tardanzas
            FROM estudiantexcurso e
            WHERE e.estado = true
            ORDER BY e.apellidos, e.nombres;
        """)
        estudiantes = cursor.fetchall()
        conn.close()
        return estudiantes

    def obtener_por_id(self, estudiante_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudiantexcurso WHERE id_estudiante = %s AND estado = true;", (estudiante_id,))
        estudiante = cursor.fetchone()
        conn.close()
        return estudiante

    def crear(self, estudiante: Estudiante):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # id_curso se busca automáticamente con grado, grupo y jornada
        query = """
            INSERT INTO estudiantexcurso (documento, nombres, apellidos, grado, grupo, jornada, id_curso)
            VALUES (%s, %s, %s, %s, %s, %s,
                    (SELECT id_curso FROM cursos WHERE grado = %s AND grupo = %s AND jornada = %s LIMIT 1))
            RETURNING id_estudiante;
        """
        cursor.execute(query, (
            estudiante.documento, estudiante.nombres, estudiante.apellidos,
            estudiante.grado, estudiante.grupo, estudiante.jornada,
            estudiante.grado, estudiante.grupo, estudiante.jornada
        ))
        nuevo_id = cursor.fetchone()['id_estudiante']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, estudiante_id: int, estudiante: Estudiante):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE estudiantexcurso
            SET documento = %s, nombres = %s, apellidos = %s, grado = %s, grupo = %s, jornada = %s,
                id_curso = (SELECT id_curso FROM cursos WHERE grado = %s AND grupo = %s AND jornada = %s LIMIT 1),
                actualizado = CURRENT_TIMESTAMP
            WHERE id_estudiante = %s AND estado = true
            RETURNING id_estudiante;
        """
        cursor.execute(query, (
            estudiante.documento, estudiante.nombres, estudiante.apellidos,
            estudiante.grado, estudiante.grupo, estudiante.jornada,
            estudiante.grado, estudiante.grupo, estudiante.jornada, estudiante_id
        ))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, estudiante_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE estudiantexcurso SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_estudiante = %s AND estado = true RETURNING id_estudiante;", (estudiante_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

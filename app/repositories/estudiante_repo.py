from app.core.database import Database
from app.models.estudiante import Estudiante

class EstudianteRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudiantexcurso ORDER BY id_estudiante ASC;")
        estudiantes = cursor.fetchall()
        conn.close()
        return estudiantes

    def obtener_por_id(self, estudiante_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudiantexcurso WHERE id_estudiante = %s;", (estudiante_id,))
        estudiante = cursor.fetchone()
        conn.close()
        return estudiante

    def crear(self, estudiante: Estudiante):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO estudiantexcurso (documento, nombres, apellidos, grado, grupo, jornada, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_estudiante;
        """
        cursor.execute(query, (
            estudiante.documento, estudiante.nombres, estudiante.apellidos,
            estudiante.grado, estudiante.grupo, estudiante.jornada, estudiante.estado
        ))
        nuevo_id = cursor.fetchone()['id_estudiante']
        conn.commit()
        conn.close()
        return nuevo_id

    def eliminar(self, estudiante_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estudiantexcurso WHERE id_estudiante = %s RETURNING id_estudiante;", (estudiante_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

    def actualizar(self, estudiante_id: int, estudiante: Estudiante):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE estudiantexcurso
            SET documento = %s, nombres = %s, apellidos = %s, grado = %s, grupo = %s, jornada = %s, estado = %s
            WHERE id_estudiante = %s
            RETURNING id_estudiante;
        """
        cursor.execute(query, (
            estudiante.documento, estudiante.nombres, estudiante.apellidos,
            estudiante.grado, estudiante.grupo, estudiante.jornada, estudiante.estado, estudiante_id
        ))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None
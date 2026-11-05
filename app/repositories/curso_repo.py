from app.core.database import Database
from app.models.curso import Curso

class CursoRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos WHERE estado = true ORDER BY grado, grupo, jornada;")
        cursos = cursor.fetchall()
        conn.close()
        return cursos

    def obtener_por_id(self, curso_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos WHERE id_curso = %s AND estado = true;", (curso_id,))
        curso = cursor.fetchone()
        conn.close()
        return curso

    def crear(self, curso: Curso):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO cursos (grado, grupo, jornada)
            VALUES (%s, %s, %s) RETURNING id_curso;
        """
        cursor.execute(query, (curso.grado, curso.grupo, curso.jornada))
        nuevo_id = cursor.fetchone()['id_curso']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, curso_id: int, curso: Curso):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE cursos
            SET grado = %s, grupo = %s, jornada = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id_curso = %s AND estado = true
            RETURNING id_curso;
        """
        cursor.execute(query, (curso.grado, curso.grupo, curso.jornada, curso_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, curso_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cursos SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_curso = %s AND estado = true RETURNING id_curso;", (curso_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

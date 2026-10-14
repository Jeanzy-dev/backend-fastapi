from app.core.database import Database
from app.models.curso import CursoCrear

class CursoRepository:
    def __init__(self):
        self.db = Database()

    # 1. Listar cursos activos
    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos WHERE estado = TRUE ORDER BY grado ASC, grupo ASC;")
        cursos = cursor.fetchall()
        cursor.close()
        conn.close()
        return cursos

    # 2. Obtener curso por ID
    def obtener_por_id(self, id_curso: int):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos WHERE id_curso = %s AND estado = TRUE;", (id_curso,))
        curso = cursor.fetchone()
        cursor.close()
        conn.close()
        return curso

    # 3. Crear nuevo curso
    def crear(self, curso: CursoCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO cursos (grado, grupo, jornada)
            VALUES (%s, %s, %s)
            RETURNING id_curso;
        """
        cursor.execute(query, (curso.grado, curso.grupo, curso.jornada))
        nuevo_id = cursor.fetchone()['id_curso']
        conn.commit()
        cursor.close()
        conn.close()
        return nuevo_id

    # 4. Actualizar curso
    def actualizar(self, id_curso: int, curso: CursoCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE cursos
            SET grado = %s, grupo = %s, jornada = %s
            WHERE id_curso = %s AND estado = TRUE
            RETURNING id_curso;
        """
        cursor.execute(query, (curso.grado, curso.grupo, curso.jornada, id_curso))
        actualizado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return actualizado is not None

    # 5. Soft Delete
    def eliminar_logico(self, id_curso: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE cursos
            SET estado = FALSE
            WHERE id_curso = %s AND estado = TRUE
            RETURNING id_curso;
        """
        cursor.execute(query, (id_curso,))
        eliminado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return eliminado is not None
from app.core.database import Database
from app.models.estudiante import EstudianteCrear

class EstudianteRepository:
    def __init__(self):
        self.db = Database()

    # 1. Listar solo activos
    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudiantexcurso WHERE estado = TRUE ORDER BY id_estudiante ASC;")
        estudiantes = cursor.fetchall()
        cursor.close()
        conn.close()
        return estudiantes

    # 2. Obtener por ID
    def obtener_por_id(self, id_estudiante: int):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudiantexcurso WHERE id_estudiante = %s AND estado = TRUE;", (id_estudiante,))
        estudiante = cursor.fetchone()
        cursor.close()
        conn.close()
        return estudiante

    # 3. Crear estudiante
    def crear(self, estudiante: EstudianteCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO estudiantexcurso (documento, nombres, apellidos, grado, grupo, jornada)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_estudiante;
        """
        cursor.execute(query, (
            estudiante.documento,
            estudiante.nombres,
            estudiante.apellidos,
            estudiante.grado,
            estudiante.grupo,
            estudiante.jornada
        ))
        nuevo_id = cursor.fetchone()['id_estudiante']
        conn.commit()
        cursor.close()
        conn.close()
        return nuevo_id

    # 4. Actualizar estudiante
    def actualizar(self, id_estudiante: int, estudiante: EstudianteCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE estudiantexcurso
            SET documento = %s, nombres = %s, apellidos = %s, grado = %s, grupo = %s, jornada = %s
            WHERE id_estudiante = %s AND estado = TRUE
            RETURNING id_estudiante;
        """
        cursor.execute(query, (
            estudiante.documento,
            estudiante.nombres,
            estudiante.apellidos,
            estudiante.grado,
            estudiante.grupo,
            estudiante.jornada,
            id_estudiante
        ))
        actualizado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return actualizado is not None

    # 5. Soft Delete
    def eliminar_logico(self, id_estudiante: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE estudiantexcurso
            SET estado = FALSE
            WHERE id_estudiante = %s AND estado = TRUE
            RETURNING id_estudiante;
        """
        cursor.execute(query, (id_estudiante,))
        eliminado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return eliminado is not None
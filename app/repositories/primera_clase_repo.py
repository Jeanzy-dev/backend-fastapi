from app.core.database import Database
from app.models.primera_clase import PrimeraClase

class PrimeraClaseRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM primeraclasexgrupo WHERE estado = true ORDER BY grado, grupo, jornada;")
        clases = cursor.fetchall()
        conn.close()
        return clases

    def obtener_por_id(self, clase_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM primeraclasexgrupo WHERE id_clase_grupo = %s AND estado = true;", (clase_id,))
        clase = cursor.fetchone()
        conn.close()
        return clase

    def crear(self, clase: PrimeraClase):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO primeraclasexgrupo (grado, grupo, jornada, hora_inicio_timbre, hora_cierre_porton, tolerancia_minutos, id_curso)
            VALUES (%s, %s, %s, %s, %s, %s,
                    (SELECT id_curso FROM cursos WHERE grado = %s AND grupo = %s AND jornada = %s LIMIT 1))
            RETURNING id_clase_grupo;
        """
        cursor.execute(query, (
            clase.grado, clase.grupo, clase.jornada,
            clase.hora_inicio_timbre, clase.hora_cierre_porton, clase.tolerancia_minutos,
            clase.grado, clase.grupo, clase.jornada
        ))
        nuevo_id = cursor.fetchone()['id_clase_grupo']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, clase_id: int, clase: PrimeraClase):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE primeraclasexgrupo
            SET grado = %s, grupo = %s, jornada = %s, hora_inicio_timbre = %s, hora_cierre_porton = %s,
                tolerancia_minutos = %s,
                id_curso = (SELECT id_curso FROM cursos WHERE grado = %s AND grupo = %s AND jornada = %s LIMIT 1),
                actualizado = CURRENT_TIMESTAMP
            WHERE id_clase_grupo = %s AND estado = true
            RETURNING id_clase_grupo;
        """
        cursor.execute(query, (
            clase.grado, clase.grupo, clase.jornada, clase.hora_inicio_timbre,
            clase.hora_cierre_porton, clase.tolerancia_minutos,
            clase.grado, clase.grupo, clase.jornada, clase_id
        ))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, clase_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE primeraclasexgrupo SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_clase_grupo = %s AND estado = true RETURNING id_clase_grupo;", (clase_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

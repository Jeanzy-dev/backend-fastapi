from app.core.database import Database
from app.models.primera_clase import PrimeraClase

class PrimeraClaseRepository:
    def __init__(self):
     self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM primeraClaseXGrupo ORDER BY id_clase_grupo ASC;")
        clases = cursor.fetchall()
        conn.close()
        return clases

    def obtener_por_id(self, clase_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM primeraClaseXGrupo WHERE id_clase_grupo = %s;", (clase_id,))
        clase = cursor.fetchone()
        conn.close()
        return clase

    def crear(self, clase: PrimeraClase):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO primeraClaseXGrupo (grado, grupo, jornada, hora_inicio_timbre, hora_cierre_porton, tolerancia_minutos, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_clase_grupo;
        """
        cursor.execute(query, (
            clase.grado, clase.grupo, clase.jornada, 
            clase.hora_inicio_timbre, clase.hora_cierre_porton, 
            clase.tolerancia_minutos, clase.estado
        ))
        nuevo_id = cursor.fetchone()['id_clase_grupo']
        conn.commit()
        conn.close()
        return nuevo_id

    def eliminar(self, clase_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM primeraClaseXGrupo WHERE id_clase_grupo = %s RETURNING id_clase_grupo;", (clase_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

    def actualizar(self, clase_id: int, clase: PrimeraClase):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE primeraClaseXGrupo
            SET grado = %s, grupo = %s, jornada = %s, hora_inicio_timbre = %s, hora_cierre_porton = %s, tolerancia_minutos = %s, estado = %s
            WHERE id_clase_grupo = %s
            RETURNING id_clase_grupo;
        """
        cursor.execute(query, (
            clase.grado, clase.grupo, clase.jornada, clase.hora_inicio_timbre,
            clase.hora_cierre_porton, clase.tolerancia_minutos, clase.estado, clase_id
        ))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None
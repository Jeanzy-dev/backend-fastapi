from app.core.database import Database
from app.models.primera_clase import PrimeraClaseCrear

class PrimeraClaseRepository:
    def __init__(self):
        self.db = Database()

    # 1. Listar solo activos
    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM primeraClaseXGrupo WHERE estado = TRUE ORDER BY id_clase_grupo ASC;")
        horarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return horarios

    # 2. Obtener por ID
    def obtener_por_id(self, id_clase_grupo: int):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM primeraClaseXGrupo WHERE id_clase_grupo = %s AND estado = TRUE;", (id_clase_grupo,))
        horario = cursor.fetchone()
        cursor.close()
        conn.close()
        return horario

    # 3. Crear horario por grupo
    def crear(self, horario: PrimeraClaseCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO primeraClaseXGrupo (grado, grupo, jornada, hora_inicio_timbre, hora_cierre_porton, tolerancia_minutos)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_clase_grupo;
        """
        cursor.execute(query, (
            horario.grado,
            horario.grupo,
            horario.jornada,
            horario.hora_inicio_timbre,
            horario.hora_cierre_porton,
            horario.tolerancia_minutos
        ))
        nuevo_id = cursor.fetchone()['id_clase_grupo']
        conn.commit()
        cursor.close()
        conn.close()
        return nuevo_id

    # 4. Actualizar horario
    def actualizar(self, id_clase_grupo: int, horario: PrimeraClaseCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE primeraClaseXGrupo
            SET grado = %s, grupo = %s, jornada = %s, hora_inicio_timbre = %s, hora_cierre_porton = %s, tolerancia_minutos = %s
            WHERE id_clase_grupo = %s AND estado = TRUE
            RETURNING id_clase_grupo;
        """
        cursor.execute(query, (
            horario.grado,
            horario.grupo,
            horario.jornada,
            horario.hora_inicio_timbre,
            horario.hora_cierre_porton,
            horario.tolerancia_minutos,
            id_clase_grupo
        ))
        actualizado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return actualizado is not None


    def eliminar_logico(self, id_clase_grupo: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE primeraClaseXGrupo
            SET estado = FALSE
            WHERE id_clase_grupo = %s AND estado = TRUE
            RETURNING id_clase_grupo;
        """
        cursor.execute(query, (id_clase_grupo,))
        eliminado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return eliminado is not None
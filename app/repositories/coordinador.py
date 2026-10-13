from app.core.database import Database
from app.models.coordinador import Coordinador

class CoordinadorRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordinador WHERE estado = true ORDER BY id_coordinador ASC;")
        registros = cursor.fetchall()
        conn.close()
        return registros

    def obtener_por_id(self, id_coordinador: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordinador WHERE id_coordinador = %s AND estado = true;", (id_coordinador,))
        registro = cursor.fetchone()
        conn.close()
        return registro

    def crear(self, registro: Coordinador):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO coordinador (id_usuario, jornada_asignada, telefono_oficina, estado, creado, actualizado) 
            VALUES (%s, %s, %s, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id_coordinador;
        """
        cursor.execute(query, (registro.id_usuario, registro.jornada_asignada, registro.telefono_oficina))
        nuevo_id = cursor.fetchone()['id_coordinador']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, id_coordinador: int, registro: Coordinador):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE coordinador
            SET id_usuario = %s, jornada_asignada = %s, telefono_oficina = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id_coordinador = %s AND estado = true
            RETURNING id_coordinador;
        """
        cursor.execute(query, (registro.id_usuario, registro.jornada_asignada, registro.telefono_oficina, id_coordinador))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, id_coordinador: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE coordinador SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_coordinador = %s RETURNING id_coordinador;", (id_coordinador,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None
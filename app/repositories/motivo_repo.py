from app.core.database import Database
from app.models.motivo import MotivoTardanza

class MotivoRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motivo_tardanza WHERE estado = true ORDER BY descripcion ASC;")
        motivos = cursor.fetchall()
        conn.close()
        return motivos

    def obtener_por_id(self, motivo_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motivo_tardanza WHERE id_motivo = %s AND estado = true;", (motivo_id,))
        motivo = cursor.fetchone()
        conn.close()
        return motivo

    def crear(self, motivo: MotivoTardanza):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO motivo_tardanza (descripcion, es_justificable)
            VALUES (%s, %s) RETURNING id_motivo;
        """
        cursor.execute(query, (motivo.descripcion, motivo.es_justificable))
        nuevo_id = cursor.fetchone()['id_motivo']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, motivo_id: int, motivo: MotivoTardanza):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE motivo_tardanza
            SET descripcion = %s, es_justificable = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id_motivo = %s AND estado = true
            RETURNING id_motivo;
        """
        cursor.execute(query, (motivo.descripcion, motivo.es_justificable, motivo_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, motivo_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE motivo_tardanza SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id_motivo = %s AND estado = true RETURNING id_motivo;", (motivo_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None

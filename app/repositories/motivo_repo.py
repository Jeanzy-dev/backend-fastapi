from app.core.database import Database
from app.models.motivo import MotivoCrear

class MotivoRepository:
    def __init__(self):
        self.db = Database()

    # 1. Listar solo activos
    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motivo_tardanza WHERE estado = TRUE ORDER BY id_motivo ASC;")
        motivos = cursor.fetchall()
        cursor.close()
        conn.close()
        return motivos

    # 2. Obtener por ID
    def obtener_por_id(self, id_motivo: int):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motivo_tardanza WHERE id_motivo = %s AND estado = TRUE;", (id_motivo,))
        motivo = cursor.fetchone()
        cursor.close()
        conn.close()
        return motivo

    # 3. Crear motivo
    def crear(self, motivo: MotivoCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO motivo_tardanza (descripcion, es_justificable)
            VALUES (%s, %s)
            RETURNING id_motivo;
        """
        cursor.execute(query, (motivo.descripcion, motivo.es_justificable))
        nuevo_id = cursor.fetchone()['id_motivo']
        conn.commit()
        cursor.close()
        conn.close()
        return nuevo_id

    # 4. Actualizar motivo
    def actualizar(self, id_motivo: int, motivo: MotivoCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE motivo_tardanza
            SET descripcion = %s, es_justificable = %s
            WHERE id_motivo = %s AND estado = TRUE
            RETURNING id_motivo;
        """
        cursor.execute(query, (motivo.descripcion, motivo.es_justificable, id_motivo))
        actualizado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return actualizado is not None

    # 5. Soft Delete
    def eliminar_logico(self, id_motivo: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE motivo_tardanza
            SET estado = FALSE
            WHERE id_motivo = %s AND estado = TRUE
            RETURNING id_motivo;
        """
        cursor.execute(query, (id_motivo,))
        eliminado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return eliminado is not None
from app.core.database import Database
from app.models.perfil import PerfilCrear

class PerfilRepository:
    def __init__(self):
        self.db = Database()

    # 1. Listar solo los activos (Soft Delete)
    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM perfil WHERE estado = TRUE ORDER BY id_perfil ASC;")
        perfiles = cursor.fetchall()
        cursor.close()
        conn.close()
        return perfiles

    # 2. Obtener por ID
    def obtener_por_id(self, id_perfil: int):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM perfil WHERE id_perfil = %s AND estado = TRUE;", (id_perfil,))
        perfil = cursor.fetchone()
        cursor.close()
        conn.close()
        return perfil

    # 3. Crear nuevo perfil
    def crear(self, perfil: PerfilCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO perfil (nombre, descripcion)
            VALUES (%s, %s)
            RETURNING id_perfil;
        """
        cursor.execute(query, (perfil.nombre, perfil.descripcion))
        nuevo_id = cursor.fetchone()['id_perfil']
        conn.commit()
        cursor.close()
        conn.close()
        return nuevo_id

    # 4. Actualizar
    def actualizar(self, id_perfil: int, perfil: PerfilCrear):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE perfil
            SET nombre = %s, descripcion = %s
            WHERE id_perfil = %s AND estado = TRUE
            RETURNING id_perfil;
        """
        cursor.execute(query, (perfil.nombre, perfil.descripcion, id_perfil))
        actualizado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return actualizado is not None

    # 5. ELIMINACIÓN LÓGICA (Soft Delete: cambia estado a FALSE)
    def eliminar_logico(self, id_perfil: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE perfil
            SET estado = FALSE
            WHERE id_perfil = %s AND estado = TRUE
            RETURNING id_perfil;
        """
        cursor.execute(query, (id_perfil,))
        eliminado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return eliminado is not None
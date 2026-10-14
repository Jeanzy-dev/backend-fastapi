from app.core.database import Database
from app.models.moduloxrol import ModuloxRol

class ModuloxRolRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM moduloxrol WHERE estado = true ORDER BY id ASC;")
        registros = cursor.fetchall()
        conn.close()
        return registros

    def obtener_por_id(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM moduloxrol WHERE id = %s AND estado = true;", (id_registro,))
        registro = cursor.fetchone()
        conn.close()
        return registro

    def crear(self, registro: ModuloxRol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO moduloxrol (id_perfil, id_modulo, estado, creado, actualizado) 
            VALUES (%s, %s, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id;
        """
        cursor.execute(query, (registro.id_perfil, registro.id_modulo))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, id_registro: int, registro: ModuloxRol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE moduloxrol
            SET id_perfil = %s, id_modulo = %s, actualizado = CURRENT_TIMESTAMP
            WHERE id = %s AND estado = true
            RETURNING id;
        """
        cursor.execute(query, (registro.id_perfil, registro.id_modulo, id_registro))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, id_registro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE moduloxrol SET estado = false, actualizado = CURRENT_TIMESTAMP WHERE id = %s RETURNING id;", (id_registro,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None
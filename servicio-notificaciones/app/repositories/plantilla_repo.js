const db = require('../core/database');

class PlantillaRepository {
    async obtenerTodos() {
        const conn = await db.getConnection();
        try {
            const [rows] = await conn.execute('SELECT * FROM plantillas_notificacion ORDER BY id_plantilla ASC;');
            return rows;
        } finally {
            conn.release();
        }
    }

    async obtenerPorId(id_plantilla) {
        const conn = await db.getConnection();
        try {
            const [rows] = await conn.execute('SELECT * FROM plantillas_notificacion WHERE id_plantilla = ?;', [id_plantilla]);
            return rows[0] || null;
        } finally {
            conn.release();
        }
    }

    async crear(plantilla) {
        const conn = await db.getConnection();
        try {
            const query = `
                INSERT INTO plantillas_notificacion (codigo_plantilla, asunto, cuerpo_html, estado)
                VALUES (?, ?, ?, ?);
            `;
            const [res] = await conn.execute(query, [plantilla.codigo_plantilla, plantilla.asunto, plantilla.cuerpo_html, plantilla.estado]);
            return res.insertId;
        } finally {
            conn.release();
        }
    }

    async actualizar(id_plantilla, plantilla) {
        const conn = await db.getConnection();
        try {
            const query = `
                UPDATE plantillas_notificacion
                SET codigo_plantilla = ?, asunto = ?, cuerpo_html = ?, estado = ?
                WHERE id_plantilla = ?;
            `;
            const [res] = await conn.execute(query, [plantilla.codigo_plantilla, plantilla.asunto, plantilla.cuerpo_html, plantilla.estado, id_plantilla]);
            return res.affectedRows > 0;
        } finally {
            conn.release();
        }
    }

    async eliminar(id_plantilla) {
        const conn = await db.getConnection();
        try {
            const [res] = await conn.execute('DELETE FROM plantillas_notificacion WHERE id_plantilla = ?;', [id_plantilla]);
            return res.affectedRows > 0;
        } finally {
            conn.release();
        }
    }
}

module.exports = new PlantillaRepository();
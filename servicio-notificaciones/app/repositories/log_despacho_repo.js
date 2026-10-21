const db = require('../core/database');

class LogDespachoRepository {
    async obtenerTodos() {
        const conn = await db.getConnection();
        try {
            const [rows] = await conn.execute('SELECT * FROM logs_despacho_correo ORDER BY id_log DESC;');
            return rows;
        } finally {
            conn.release();
        }
    }

    async obtenerPorId(id_log) {
        const conn = await db.getConnection();
        try {
            const [rows] = await conn.execute('SELECT * FROM logs_despacho_correo WHERE id_log = ?;', [id_log]);
            return rows[0] || null;
        } finally {
            conn.release();
        }
    }

    async crear(log) {
        const conn = await db.getConnection();
        try {
            const query = `
                INSERT INTO logs_despacho_correo (id_envio, proveedor_smtp, id_mensaje_servidor, intentos, detalle_respuesta, estado)
                VALUES (?, ?, ?, ?, ?, ?);
            `;
            const [res] = await conn.execute(query, [
                log.id_envio, log.proveedor_smtp, log.id_mensaje_servidor,
                log.intentos, log.detalle_respuesta, log.estado
            ]);
            return res.insertId;
        } finally {
            conn.release();
        }
    }

    async eliminar(id_log) {
        const conn = await db.getConnection();
        try {
            const [res] = await conn.execute('DELETE FROM logs_despacho_correo WHERE id_log = ?;', [id_log]);
            return res.affectedRows > 0;
        } finally {
            conn.release();
        }
    }
}

module.exports = new LogDespachoRepository();
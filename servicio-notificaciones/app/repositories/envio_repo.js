const db = require('../core/database');

class EnvioRepository {
    async obtenerTodos() {
        const conn = await db.getConnection();
        try {
            const [rows] = await conn.execute('SELECT * FROM envios_alerta ORDER BY id_envio DESC;');
            return rows;
        } finally {
            conn.release();
        }
    }

    async obtenerPorId(id_envio) {
        const conn = await db.getConnection();
        try {
            const [rows] = await conn.execute('SELECT * FROM envios_alerta WHERE id_envio = ?;', [id_envio]);
            return rows[0] || null;
        } finally {
            conn.release();
        }
    }

    async crear(envio) {
        const conn = await db.getConnection();
        try {
            const query = `
                INSERT INTO envios_alerta (id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            `;
            const [res] = await conn.execute(query, [
                envio.id_plantilla, envio.documento_estudiante, envio.nombre_estudiante,
                envio.correo_destinatario, envio.total_tardanzas, envio.codigo_seguimiento,
                envio.estado_despacho, envio.estado
            ]);
            return res.insertId;
        } finally {
            conn.release();
        }
    }

    async actualizar(id_envio, envio) {
        const conn = await db.getConnection();
        try {
            const query = `
                UPDATE envios_alerta
                SET id_plantilla = ?, documento_estudiante = ?, nombre_estudiante = ?, correo_destinatario = ?, total_tardanzas = ?, codigo_seguimiento = ?, estado_despacho = ?, estado = ?
                WHERE id_envio = ?;
            `;
            const [res] = await conn.execute(query, [
                envio.id_plantilla, envio.documento_estudiante, envio.nombre_estudiante,
                envio.correo_destinatario, envio.total_tardanzas, envio.codigo_seguimiento,
                envio.estado_despacho, envio.estado, id_envio
            ]);
            return res.affectedRows > 0;
        } finally {
            conn.release();
        }
    }

    async eliminar(id_envio) {
        const conn = await db.getConnection();
        try {
            const [res] = await conn.execute('DELETE FROM envios_alerta WHERE id_envio = ?;', [id_envio]);
            return res.affectedRows > 0;
        } finally {
            conn.release();
        }
    }
}

module.exports = new EnvioRepository();
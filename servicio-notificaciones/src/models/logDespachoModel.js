const db = require('../config/dbConfig');

class logDespachoModel {

    getLogs(callback) {
        const sql = "select * from logs_despacho_correo";
        db.query(sql, callback);
    }

    getLogById(id, callback) {
        const sql = "select * from logs_despacho_correo where id_log = ?";
        db.query(sql, [id], callback);
    }

    postLog(id_envio, proveedor_smtp, id_mensaje_servidor, intentos, detalle_respuesta, estado, callback) {
        const sql = 'insert into logs_despacho_correo(id_envio, proveedor_smtp, id_mensaje_servidor, intentos, detalle_respuesta, estado) values (?, ?, ?, ?, ?, ?)';
        db.query(sql, [id_envio, proveedor_smtp || 'Gmail SMTP', id_mensaje_servidor, intentos || 1, detalle_respuesta, estado || 1], (err, result) => {
            if (err) return callback(err, null);
            callback(null, result.insertId);
        });
    }

    deleteLog(id, callback) {
        const sql = 'delete from logs_despacho_correo where id_log = ?';
        db.query(sql, [id], callback);
    }

}

module.exports = new logDespachoModel();
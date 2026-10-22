const db = require('../config/dbConfig');

class envioModel {

    getEnvios(callback) {
        const sql = "select * from envios_alerta";
        db.query(sql, callback);
    }

    getEnvioById(id, callback) {
        const sql = "select * from envios_alerta where id_envio = ?";
        db.query(sql, [id], callback);
    }

    postEnvio(id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado, callback) {
        const sql = 'insert into envios_alerta(id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado) values (?, ?, ?, ?, ?, ?, ?, ?)';
        db.query(sql, [id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho || 'PENDIENTE', estado || 1], (err, result) => {
            if (err) return callback(err, null);
            callback(null, result.insertId);
        });
    }

    putEnvio(id, id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado, callback) {
        const sql = 'update envios_alerta set id_plantilla = ?, documento_estudiante = ?, nombre_estudiante = ?, correo_destinatario = ?, total_tardanzas = ?, codigo_seguimiento = ?, estado_despacho = ?, estado = ? where id_envio = ?';
        db.query(sql, [id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado, id], callback);
    }

    deleteEnvio(id, callback) {
        const sql = 'delete from envios_alerta where id_envio = ?';
        db.query(sql, [id], callback);
    }

}

module.exports = new envioModel();
const db = require('../config/dbConfig');

class plantillaModel {

    getPlantillas(callback) {
        const sql = "select * from plantillas_notificacion";
        db.query(sql, callback);
    }

    getPlantillaById(id, callback) {
        const sql = "select * from plantillas_notificacion where id_plantilla = ?";
        db.query(sql, [id], callback);
    }

    postPlantilla(codigo_plantilla, asunto, cuerpo_html, estado, callback) {
        const sql = 'insert into plantillas_notificacion(codigo_plantilla, asunto, cuerpo_html, estado) values (?, ?, ?, ?)';
        db.query(sql, [codigo_plantilla, asunto, cuerpo_html, estado || 1], (err, result) => {
            if (err) return callback(err, null);
            callback(null, result.insertId);
        });
    }

    putPlantilla(id, codigo_plantilla, asunto, cuerpo_html, estado, callback) {
        const sql = 'update plantillas_notificacion set codigo_plantilla = ?, asunto = ?, cuerpo_html = ?, estado = ? where id_plantilla = ?';
        db.query(sql, [codigo_plantilla, asunto, cuerpo_html, estado, id], callback);
    }

    deletePlantilla(id, callback) {
        const sql = 'delete from plantillas_notificacion where id_plantilla = ?';
        db.query(sql, [id], callback);
    }

}

module.exports = new plantillaModel();
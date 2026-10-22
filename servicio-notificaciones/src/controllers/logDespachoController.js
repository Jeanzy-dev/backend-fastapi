const logDespachoModel = require('../models/logDespachoModel');

module.exports = {

    getLogs: (req, res) => {
        logDespachoModel.getLogs((err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            res.status(200).json({ data: result });
        });
    },

    getLogById: (req, res) => {
        const { id } = req.params;
        logDespachoModel.getLogById(id, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            if (result.length === 0) return res.status(404).json({ message: 'Log no encontrado' });
            res.status(200).json({ data: result });
        });
    },

    postLog: (req, res) => {
        const { id_envio, proveedor_smtp, id_mensaje_servidor, intentos, detalle_respuesta, estado } = req.body;
        logDespachoModel.postLog(id_envio, proveedor_smtp, id_mensaje_servidor, intentos, detalle_respuesta, estado, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            res.status(201).json({ message: 'Log de despacho creado correctamente', data: { idInsertado: result } });
        });
    },

    deleteLog: (req, res) => {
        const { id } = req.params;
        logDespachoModel.deleteLog(id, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ message: 'Log No Encontrado' });
            res.status(200).json({ message: 'Log eliminado correctamente' });
        });
    }

};
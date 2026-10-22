const envioModel = require('../models/envioModel');

module.exports = {

    getEnvios: (req, res) => {
        envioModel.getEnvios((err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            res.status(200).json({ data: result });
        });
    },

    getEnvioById: (req, res) => {
        const { id } = req.params;
        envioModel.getEnvioById(id, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            if (result.length === 0) return res.status(404).json({ message: 'Envio no encontrado' });
            res.status(200).json({ data: result });
        });
    },

    postEnvio: (req, res) => {
        const { id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado } = req.body;
        envioModel.postEnvio(id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            res.status(201).json({ message: 'Envio creado correctamente', data: { idInsertado: result } });
        });
    },

    putEnvio: (req, res) => {
        const { id } = req.params;
        const { id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado } = req.body;
        envioModel.putEnvio(id, id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho, estado, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ message: 'Envio No Encontrado' });
            res.status(200).json({ message: 'Envio actualizado correctamente' });
        });
    },

    deleteEnvio: (req, res) => {
        const { id } = req.params;
        envioModel.deleteEnvio(id, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ message: 'Envio No Encontrado' });
            res.status(200).json({ message: 'Envio eliminado correctamente' });
        });
    }

};
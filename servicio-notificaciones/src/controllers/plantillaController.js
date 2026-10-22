const plantillaModel = require('../models/plantillaModel');

module.exports = {

    getPlantillas: (req, res) => {
        plantillaModel.getPlantillas((err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            res.status(200).json({ data: result });
        });
    },

    getPlantillaById: (req, res) => {
        const { id } = req.params;
        plantillaModel.getPlantillaById(id, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            if (result.length === 0) return res.status(404).json({ message: 'Plantilla no encontrada' });
            res.status(200).json({ data: result });
        });
    },

    postPlantilla: (req, res) => {
        const { codigo_plantilla, asunto, cuerpo_html, estado } = req.body;
        plantillaModel.postPlantilla(codigo_plantilla, asunto, cuerpo_html, estado, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            res.status(201).json({ message: 'Plantilla creada correctamente', data: { idInsertado: result } });
        });
    },

    putPlantilla: (req, res) => {
        const { id } = req.params;
        const { codigo_plantilla, asunto, cuerpo_html, estado } = req.body;
        plantillaModel.putPlantilla(id, codigo_plantilla, asunto, cuerpo_html, estado, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ message: 'Plantilla No Encontrada' });
            res.status(200).json({ message: 'Plantilla actualizada correctamente' });
        });
    },

    deletePlantilla: (req, res) => {
        const { id } = req.params;
        plantillaModel.deletePlantilla(id, (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            if (result.affectedRows === 0) return res.status(404).json({ message: 'Plantilla No Encontrada' });
            res.status(200).json({ message: 'Plantilla eliminada correctamente' });
        });
    }

};
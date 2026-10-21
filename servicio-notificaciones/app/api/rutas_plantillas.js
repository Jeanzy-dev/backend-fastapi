const express = require('express');
const router = express.Router();
const repo = require('../repositories/plantilla_repo');
const PlantillaNotificacion = require('../models/plantilla');

router.get('/', async (req, res) => {
    try {
        const plantillas = await repo.obtenerTodos();
        res.json(plantillas);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.get('/:plantilla_id', async (req, res) => {
    try {
        const plantilla = await repo.obtenerPorId(req.params.plantilla_id);
        if (!plantilla) return res.status(404).json({ detail: "Plantilla no encontrada" });
        res.json(plantilla);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.post('/', async (req, res) => {
    try {
        const plantilla = new PlantillaNotificacion(req.body);
        const nuevoId = await repo.crear(plantilla);
        res.status(201).json({ mensaje: "Plantilla registrada exitosamente", id: nuevoId });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.put('/:plantilla_id', async (req, res) => {
    try {
        const plantilla = new PlantillaNotificacion(req.body);
        const exito = await repo.actualizar(req.params.plantilla_id, plantilla);
        if (!exito) return res.status(404).json({ detail: "Plantilla no encontrada" });
        res.json({ mensaje: "Plantilla actualizada correctamente" });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.delete('/:plantilla_id', async (req, res) => {
    try {
        const exito = await repo.eliminar(req.params.plantilla_id);
        if (!exito) return res.status(404).json({ detail: "Plantilla no encontrada" });
        res.json({ mensaje: "Plantilla eliminada correctamente" });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
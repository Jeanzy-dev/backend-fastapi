const express = require('express');
const router = express.Router();
const repo = require('../repositories/log_despacho_repo');
const LogDespachoCorreo = require('../models/log_despacho');

router.get('/', async (req, res) => {
    try {
        const logs = await repo.obtenerTodos();
        res.json(logs);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.get('/:log_id', async (req, res) => {
    try {
        const log = await repo.obtenerPorId(req.params.log_id);
        if (!log) return res.status(404).json({ detail: "Log no encontrado" });
        res.json(log);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.post('/', async (req, res) => {
    try {
        const log = new LogDespachoCorreo(req.body);
        const nuevoId = await repo.crear(log);
        res.status(201).json({ mensaje: "Log de despacho registrado exitosamente", id: nuevoId });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.delete('/:log_id', async (req, res) => {
    try {
        const exito = await repo.eliminar(req.params.log_id);
        if (!exito) return res.status(404).json({ detail: "Log no encontrado" });
        res.json({ mensaje: "Log eliminado correctamente" });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
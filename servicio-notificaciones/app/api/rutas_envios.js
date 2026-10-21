const express = require('express');
const router = express.Router();
const repo = require('../repositories/envio_repo');
const EnvioAlerta = require('../models/envio');

router.get('/', async (req, res) => {
    try {
        const envios = await repo.obtenerTodos();
        res.json(envios);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.get('/:envio_id', async (req, res) => {
    try {
        const envio = await repo.obtenerPorId(req.params.envio_id);
        if (!envio) return res.status(404).json({ detail: "Envío no encontrado" });
        res.json(envio);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.post('/', async (req, res) => {
    try {
        const envio = new EnvioAlerta(req.body);
        const nuevoId = await repo.crear(envio);
        res.status(201).json({ mensaje: "Envío registrado exitosamente", id: nuevoId });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.put('/:envio_id', async (req, res) => {
    try {
        const envio = new EnvioAlerta(req.body);
        const exito = await repo.actualizar(req.params.envio_id, envio);
        if (!exito) return res.status(404).json({ detail: "Envío no encontrado" });
        res.json({ mensaje: "Envío actualizado correctamente" });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

router.delete('/:envio_id', async (req, res) => {
    try {
        const exito = await repo.eliminar(req.params.envio_id);
        if (!exito) return res.status(404).json({ detail: "Envío no encontrado" });
        res.json({ mensaje: "Envío eliminado correctamente" });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
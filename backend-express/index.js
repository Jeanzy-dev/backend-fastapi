const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

const pool = mysql.createPool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 4000,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME || 'test',
    ssl: { rejectUnauthorized: false },
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

app.get('/', (req, res) => {
    res.json({
        status: 'ok',
        mensaje: 'API Auxiliar de Notificaciones (Node.js + Express + MySQL) activa y funcional'
    });
});


app.get('/api/plantillas', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM plantillas_notificacion WHERE estado = 1 ORDER BY id_plantilla ASC');
        res.json(rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/plantillas/:id', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM plantillas_notificacion WHERE id_plantilla = ? AND estado = 1', [req.params.id]);
        if (rows.length === 0) return res.status(404).json({ mensaje: 'Plantilla no encontrada o inactiva' });
        res.json(rows[0]);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/plantillas', async (req, res) => {
    const { codigo_plantilla, asunto, cuerpo_html } = req.body;
    try {
        const [result] = await pool.query(
            'INSERT INTO plantillas_notificacion (codigo_plantilla, asunto, cuerpo_html) VALUES (?, ?, ?)',
            [codigo_plantilla, asunto, cuerpo_html]
        );
        res.status(201).json({ mensaje: 'Plantilla creada con éxito', id_plantilla: result.insertId });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.put('/api/plantillas/:id', async (req, res) => {
    const { codigo_plantilla, asunto, cuerpo_html } = req.body;
    try {
        const [result] = await pool.query(
            'UPDATE plantillas_notificacion SET codigo_plantilla = ?, asunto = ?, cuerpo_html = ? WHERE id_plantilla = ? AND estado = 1',
            [codigo_plantilla, asunto, cuerpo_html, req.params.id]
        );
        if (result.affectedRows === 0) return res.status(404).json({ mensaje: 'Plantilla no encontrada o inactiva' });
        res.json({ mensaje: 'Plantilla actualizada con éxito' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.delete('/api/plantillas/:id', async (req, res) => {
    try {
        const [result] = await pool.query(
            'UPDATE plantillas_notificacion SET estado = 0 WHERE id_plantilla = ? AND estado = 1',
            [req.params.id]
        );
        if (result.affectedRows === 0) return res.status(404).json({ mensaje: 'Plantilla no encontrada o ya inactiva' });
        res.json({ mensaje: 'Plantilla desactivada exitosamente (Soft Delete)' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.get('/api/envios', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM envios_alerta WHERE estado = 1 ORDER BY id_envio DESC');
        res.json(rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/envios', async (req, res) => {
    const { id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento } = req.body;
    try {
        const [result] = await pool.query(
            `INSERT INTO envios_alerta 
            (id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento, estado_despacho) 
            VALUES (?, ?, ?, ?, ?, ?, 'ENVIADO')`,
            [id_plantilla, documento_estudiante, nombre_estudiante, correo_destinatario, total_tardanzas, codigo_seguimiento]
        );
        res.status(201).json({ mensaje: 'Orden de alerta registrada', id_envio: result.insertId });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.get('/api/logs', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM logs_despacho_correo WHERE estado = 1 ORDER BY id_log DESC');
        res.json(rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Servidor Express corriendo en http://localhost:${PORT}`);
});
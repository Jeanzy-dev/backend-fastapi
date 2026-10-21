const express = require('express');
const app = express();
require('dotenv').config();

app.use(express.json());

const rutasPlantillas = require('./app/api/rutas_plantillas');
const rutasEnvios = require('./app/api/rutas_envios');
const rutasLogs = require('./app/api/rutas_logs');

app.use('/plantillas', rutasPlantillas);
app.use('/envios', rutasEnvios);
app.use('/logs', rutasLogs);

app.get('/', (req, res) => {
    res.json({ mensaje: "Servicio de notificaciones en Express y MySQL activo y funcional" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor de notificaciones iniciado en http://localhost:${PORT}`);
});
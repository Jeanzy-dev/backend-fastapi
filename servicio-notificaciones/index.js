const express = require('express');
const bodyParser = require('body-parser');

const plantillaRoutes = require('./src/routes/plantillaRoutes');
const envioRoutes = require('./src/routes/envioRoutes');
const logDespachoRoutes = require('./src/routes/logDespachoRoutes');

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

app.use('/api/plantillas', plantillaRoutes);
app.use('/api/envios', envioRoutes);
app.use('/api/logs', logDespachoRoutes);

app.listen(port, () => {
    console.log("Servidor iniciado en http://localhost:" + port);
});
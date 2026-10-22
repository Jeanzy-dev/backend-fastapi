const express = require('express');
const router = express.Router();
const envioController = require('../controllers/envioController');

router.get('/getEnvios', envioController.getEnvios);
router.get('/getEnvioById/:id', envioController.getEnvioById);
router.post('/postEnvio', envioController.postEnvio);
router.put('/putEnvio/:id', envioController.putEnvio);
router.delete('/deleteEnvio/:id', envioController.deleteEnvio);

module.exports = router;
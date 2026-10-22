const express = require('express');
const router = express.Router();
const logDespachoController = require('../controllers/logDespachoController');

router.get('/getLogs', logDespachoController.getLogs);
router.get('/getLogById/:id', logDespachoController.getLogById);
router.post('/postLog', logDespachoController.postLog);
router.delete('/deleteLog/:id', logDespachoController.deleteLog);

module.exports = router;
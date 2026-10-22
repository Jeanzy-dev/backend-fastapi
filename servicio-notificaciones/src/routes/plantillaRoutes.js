const express = require('express');
const router = express.Router();
const plantillaController = require('../controllers/plantillaController');

router.get('/getPlantillas', plantillaController.getPlantillas);
router.get('/getPlantillaById/:id', plantillaController.getPlantillaById);
router.post('/postPlantilla', plantillaController.postPlantilla);
router.put('/putPlantilla/:id', plantillaController.putPlantilla);
router.delete('/deletePlantilla/:id', plantillaController.deletePlantilla);

module.exports = router;
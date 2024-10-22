const express = require('express');
const sensorController = require('../controllers/sensorController');
const router = express.Router();

// Get all sensors
router.get('/', sensorController.getAllSensors);

// Add sensor
router.post('/', sensorController.addSensor);

// Get specific sensor by ID
router.get('/:sensorId', sensorController.getSensorById);

// Update sensor by ID
router.put('/:sensorId', sensorController.updateSensor);

// Delete sensor by ID
router.delete('/:sensorId', sensorController.deleteSensor);

module.exports = router;
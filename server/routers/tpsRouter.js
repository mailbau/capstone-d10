const express = require('express');
const tpsController = require('../controllers/tpsController');
const router = express.Router();

// Get all users
router.get('/', tpsController.getAllTPS);

// Add user
router.post('/register', tpsController.addTPS);

// Get specific TPS by ID
router.get('/:tpsId', tpsController.getTPSById);

// Update TPS by ID
router.put('/:tpsId', tpsController.updateTPS);

// Delete TPS by ID
router.delete('/:tpsId', tpsController.deleteTPS);

module.exports = router;
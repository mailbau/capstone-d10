const express = require('express');
const pathController = require('../controllers/pathController');
const router = express.Router();

// Get all routes
router.get('/', pathController.getAllPaths);

// Add route
router.post('/register', pathController.addPath);

// Get specific route by ID
router.get('/:pathId', pathController.getPathById);

// Update route by ID
router.put('/:pathId', pathController.updatePath);

// Delete route by ID
router.delete('/:pathId', pathController.deletePath);

module.exports = router;
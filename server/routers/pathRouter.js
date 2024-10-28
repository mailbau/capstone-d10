const express = require('express');
const pathController = require('../controllers/pathController');
const router = express.Router();

// Get all paths
router.get('/', pathController.getAllPaths);

// Add path
router.post('/register', pathController.addPath);

// Get specific path by ID
router.get('/:pathId', pathController.getPathById);

// Update path by ID
router.put('/:pathId', pathController.updatePath);

// Delete path by ID
router.delete('/:pathId', pathController.deletePath);

module.exports = router;
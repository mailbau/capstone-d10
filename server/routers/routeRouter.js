const express = require('express');
const routeController = require('../controllers/routeController');
const router = express.Router();

// Get all routes
router.get('/', routeController.getAllRoutes);

// Add route
router.post('/register', routeController.addRoute);

// Get specific route by ID
router.get('/:routeId', routeController.getRouteById);

// Update route by ID
router.put('/:routeId', routeController.updateRoute);

// Delete route by ID
router.delete('/:routeId', routeController.deleteRoute);

module.exports = router;
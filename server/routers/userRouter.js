const express = require('express');
const userController = require('../controllers/userController');
const router = express.Router();

// Get all users
router.get('/', userController.getAllUsers);

// Add user
router.post('/register', userController.addUser);

module.exports = router;
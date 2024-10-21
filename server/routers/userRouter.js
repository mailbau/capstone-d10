const express = require('express');
const userController = require('../controllers/userController');
const router = express.Router();

// Get all users
router.get('/', userController.getAllUsers);

// Add user
router.post('/register', userController.addUser);

// Get specific user by ID
router.get('/:userId', userController.getUserById);

// Update user by ID
router.put('/:userId', userController.updateUser);

// Delete user by ID
router.delete('/:userId', userController.deleteUser);

module.exports = router;
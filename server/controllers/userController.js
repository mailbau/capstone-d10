const db = require('../config/firebase');
const bcrypt = require('bcrypt');

const userController = {

    // Get all users
    getAllUsers: async (req, res) => {
        try {
            const usersSnapshot = await db.ref('/users').get();
            const users = usersSnapshot.val() || {}; // Return empty object if no users
            res.status(200).json(users);
        } catch (error) {
            console.error('Error getting all users', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Get user by ID
    getUserById: async (req, res) => {
        try {
            const userId = req.params.userId;

            if (!userId || typeof userId !== 'string') {
                return res.status(400).json({ error: 'Invalid user ID' });
            }

            const userSnapshot = await db.ref(`/users/${userId}`).get();

            if (!userSnapshot.exists()) {
                return res.status(404).json({ message: 'User not found' });
            }

            const user = userSnapshot.val();
            res.status(200).json(user);
        } catch (error) {
            console.error('Error getting user by ID', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Add user
    addUser: async (req, res) => {
        try {
            const { first_name, last_name, user_email, user_password } = req.body;

            // Check if user already exists
            const existingUserSnapshot = await db.ref('/users').orderByChild('user_email').equalTo(user_email).get();
            if (existingUserSnapshot.exists()) {
                return res.status(409).json({ message: 'User already exists' });
            }

            // Hash the password
            const hashedPassword = await bcrypt.hash(user_password, 10);

            // Create a new user object
            const newUser = {
                first_name,
                last_name,
                user_email,
                user_password: hashedPassword
            };

            // Save the user to Firebase
            const newUserRef = await db.ref('/users').push(newUser);
            res.status(201).json({ message: 'User registered successfully', user: { ...newUser, id: newUserRef.key } });
        } catch (error) {
            console.error('Error registering user', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Update user by ID
    updateUser: async (req, res) => {
        try {
            const userId = req.params.userId; // Ensure userId is properly extracted

            if (!userId || typeof userId !== 'string') {
                return res.status(400).json({ error: 'Invalid user ID' });
            }

            const { first_name, last_name, user_email, user_password } = req.body;

            // Check if user exists
            const userSnapshot = await db.ref(`/users/${userId}`).get();
            if (!userSnapshot.exists()) {
                return res.status(404).json({ message: 'User not found' });
            }

            // Hash the password if it's being updated
            let updatedPassword = user_password;
            if (user_password) {
                updatedPassword = await bcrypt.hash(user_password, 10);
            }

            // Update user data
            const updatedUser = {
                first_name,
                last_name,
                user_email,
                user_password: updatedPassword
            };

            await db.ref(`/users/${userId}`).update(updatedUser);
            res.status(200).json({ message: 'User updated successfully', updatedUser });
        } catch (error) {
            console.error('Error updating user', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Delete user by ID
    deleteUser: async (req, res) => {
        try {
            const userId = req.params.userId; // Ensure userId is properly extracted

            if (!userId || typeof userId !== 'string') {
                return res.status(400).json({ error: 'Invalid user ID' });
            }

            // Check if user exists
            const userSnapshot = await db.ref(`/users/${userId}`).get();
            if (!userSnapshot.exists()) {
                return res.status(404).json({ message: 'User not found' });
            }

            await db.ref(`/users/${userId}`).remove();
            res.status(200).json({ message: 'User deleted successfully' });
        } catch (error) {
            console.error('Error deleting user', error);
            res.status(500).json({ error: error.message });
        }
    }

};

module.exports = userController;
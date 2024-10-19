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

};

module.exports = userController;
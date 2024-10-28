const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const db = require('../config/firebase');

const loginUser = async (req, res) => {
    const { email, password } = req.body;
    // console.log('req.body', req.body);

    try {
        const snapshot = await db.ref('/users').orderByChild('user_email').equalTo(email).once('value');
        if (!snapshot.exists()) {
            return res.status(401).json({ message: 'Invalid email or password' });
        }

        const userId = Object.keys(snapshot.val())[0];
        const userData = snapshot.val()[userId];

        // Compare the entered password with the hashed password in the database
        const isPasswordValid = await bcrypt.compare(password, userData.user_password);
        if (!isPasswordValid) {
            return res.status(401).json({ message: 'Invalid email or password' });
        }

        // Generate JWT token if password is valid
        const token = jwt.sign({ userId, email }, process.env.JWT_SECRET, { expiresIn: '1h' });
        res.json({ token });
    } catch (error) {
        console.error('Error logging in user', error);
        res.status(500).json({ message: 'An error occurred during login', error });
    }
};

module.exports = { loginUser };
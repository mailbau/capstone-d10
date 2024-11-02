const express = require('express');
const cors = require('cors');
const listEndpoints = require('express-list-endpoints');
require('dotenv').config();
const db = require('./config/firebase');

const userRouter = require('./routers/userRouter');
const tpsRouter = require('./routers/tpsRouter');
const pathRouter = require('./routers/pathRouter');
const sensorRouter = require('./routers/sensorRouter');
const authRouter = require('./routers/authRouter');
const tpsStatusRouter = require('./routers/tpsStatusRouter');

const app = express();

// Test the connection to Firebase
db.ref('/').get().then(() => {
    console.log('Connected to Firebase');
}).catch((error) => {
    console.error('Error connecting to Firebase', error);
});

// Enable CORS
app.use(cors());

// Use JSON parsing middleware
app.use(express.json());

// Use the auth router
app.use('/auth', authRouter);

// Protected routes
app.use('/user', userRouter);
app.use('/tps', tpsRouter);
app.use('/path', pathRouter);
app.use('/sensor', sensorRouter);
app.use('/tpsstatus', tpsStatusRouter);

// Set the port from environment variables or use 8080
const PORT = process.env.PORT || 8080;

// Start the server
const server = app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(listEndpoints(app));
});

module.exports = server;

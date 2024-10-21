const express = require('express');
const cors = require('cors');
const listEndpoints = require('express-list-endpoints');
require('dotenv').config();

const userRouter = require('./routers/userRouter');
const tpsRouter = require('./routers/tpsRouter');
const routeRouter = require('./routers/routeRouter');

const app = express();

// Enable CORS
app.use(cors());

// Use JSON parsing middleware
app.use(express.json());

// Routes
app.use('/user', userRouter);
app.use('/tps', tpsRouter);
app.use('/route', routeRouter);

// Set the port from environment variables or use 8080
const PORT = process.env.PORT || 8080;

// Start the server
const server = app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(listEndpoints(app));
});

module.exports = server;

const db = require('../config/firebase');

const sensorController = {
    // Get all sensors
    getAllSensors: async (req, res) => {
        try {
            const sensorsSnapshot = await db.ref('/sensors').get();
            const sensors = sensorsSnapshot.val() || {}; // Return empty object if no sensors found
            res.status(200).json(sensors);
        } catch (error) {
            console.error('Error getting all sensors', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Add a new sensor
    addSensor: async (req, res) => {
        try {
            const { sensorName, tpsId } = req.body;

            // Check if sensor already exists for the same TPS
            const existingSensorSnapshot = await db.ref('/sensors').orderByChild('tpsId').equalTo(tpsId).get();
            if (existingSensorSnapshot.exists()) {
                return res.status(409).json({ message: 'Sensor already exists for this TPS' });
            }

            // Create a new sensor object
            const newSensor = {
                sensorName,
                tpsId,
                createdAt: new Date().toISOString() // Record creation time
            };

            // Save the new sensor to Firebase
            const newSensorRef = await db.ref('/sensors').push(newSensor);
            res.status(201).json({ message: 'Sensor added successfully', sensor: { ...newSensor, id: newSensorRef.key } });
        } catch (error) {
            console.error('Error adding sensor', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Get sensor by ID
    getSensorById: async (req, res) => {
        try {
            const sensorId = req.params.sensorId;

            if (!sensorId || typeof sensorId !== 'string') {
                return res.status(400).json({ error: 'Invalid sensor ID' });
            }

            const sensorSnapshot = await db.ref(`/sensors/${sensorId}`).get();

            if (!sensorSnapshot.exists()) {
                return res.status(404).json({ message: 'Sensor not found' });
            }

            const sensor = sensorSnapshot.val();
            res.status(200).json(sensor);
        } catch (error) {
            console.error('Error getting sensor by ID', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Update sensor by ID
    updateSensor: async (req, res) => {
        try {
            const sensorId = req.params.sensorId;

            if (!sensorId || typeof sensorId !== 'string') {
                return res.status(400).json({ error: 'Invalid sensor ID' });
            }

            const { sensorName, tpsId } = req.body;

            // Check if sensor exists
            const sensorSnapshot = await db.ref(`/sensors/${sensorId}`).get();
            if (!sensorSnapshot.exists()) {
                return res.status(404).json({ message: 'Sensor not found' });
            }

            // Update sensor data
            const updatedSensor = {
                sensorName,
                tpsId,
                updatedAt: new Date().toISOString() // Record update time
            };

            await db.ref(`/sensors/${sensorId}`).update(updatedSensor);
            res.status(200).json({ message: 'Sensor updated successfully', updatedSensor });
        } catch (error) {
            console.error('Error updating sensor', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Delete sensor by ID
    deleteSensor: async (req, res) => {
        try {
            const sensorId = req.params.sensorId;

            if (!sensorId || typeof sensorId !== 'string') {
                return res.status(400).json({ error: 'Invalid sensor ID' });
            }

            // Check if sensor exists
            const sensorSnapshot = await db.ref(`/sensors/${sensorId}`).get();
            if (!sensorSnapshot.exists()) {
                return res.status(404).json({ message: 'Sensor not found' });
            }

            await db.ref(`/sensors/${sensorId}`).remove();
            res.status(200).json({ message: 'Sensor deleted successfully' });
        } catch (error) {
            console.error('Error deleting sensor', error);
            res.status(500).json({ error: error.message });
        }
    }
};

module.exports = sensorController;

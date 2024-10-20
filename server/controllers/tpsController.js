const db = require('../config/firebase');
const { v4: uuidv4 } = require('uuid'); // To generate unique tpsId

const tpsController = {

    // Get all TPS locations
    getAllTPS: async (req, res) => {
        try {
            const tpsSnapshot = await db.ref('/tps').get();
            const tps = tpsSnapshot.val() || {}; // Return empty object if no TPS records found
            res.status(200).json(tps);
        } catch (error) {
            console.error('Error getting all TPS', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Add new TPS
    addTPS: async (req, res) => {
        try {
            const { name, address, latitude, longitude, gmapsLink } = req.body;

            // Create a new TPS object
            const newTPS = {
                tpsId: uuidv4(),  // Generate a unique tpsId
                name,
                address,
                latitude,
                longitude,
                gmapsLink
            };

            // Save the new TPS to Firebase
            const newTPSRef = await db.ref('/tps').push(newTPS);
            res.status(201).json({ message: 'TPS added successfully', tps: { ...newTPS, id: newTPSRef.key } });
        } catch (error) {
            console.error('Error adding TPS', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Get a specific TPS by tpsId
    getTPSById: async (req, res) => {
        try {
            const { tpsId } = req.params;
            const tpsSnapshot = await db.ref(`/tps/${tpsId}`).get();
            const tps = tpsSnapshot.val();

            if (!tps) {
                return res.status(404).json({ message: `TPS with ID ${tpsId} not found` });
            }

            res.status(200).json(tps);
        } catch (error) {
            console.error('Error getting TPS by ID', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Update an existing TPS by tpsId
    updateTPS: async (req, res) => {
        try {
            const { tpsId } = req.params;
            const { name, address, latitude, longitude, gmapsLink } = req.body;

            // Updated TPS data
            const updatedTPS = {
                name,
                address,
                latitude,
                longitude,
                gmapsLink
            };

            // Update TPS in Firebase
            await db.ref(`/tps/${tpsId}`).update(updatedTPS);
            res.status(200).json({ message: `TPS with ID ${tpsId} updated successfully`, updatedTPS });
        } catch (error) {
            console.error('Error updating TPS', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Delete a TPS by tpsId
    deleteTPS: async (req, res) => {
        try {
            const { tpsId } = req.params;

            // Delete TPS from Firebase
            await db.ref(`/tps/${tpsId}`).remove();

            res.status(200).json({ message: `TPS with ID ${tpsId} deleted successfully` });
        } catch (error) {
            console.error('Error deleting TPS', error);
            res.status(500).json({ error: error.message });
        }
    },
};

module.exports = tpsController;

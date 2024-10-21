const db = require('../config/firebase');

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

    // Get TPS by Firebase ID
    getTPSById: async (req, res) => {
        try {
            const { tpsId } = req.params;
            const tpsSnapshot = await db.ref(`/tps/${tpsId}`).get();

            if (!tpsSnapshot.exists()) {
                return res.status(404).json({ message: 'TPS not found' });
            }

            const tps = tpsSnapshot.val();
            res.status(200).json(tps);
        } catch (error) {
            console.error('Error getting TPS by ID', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Update TPS by Firebase ID
    updateTPS: async (req, res) => {
        try {
            const { tpsId } = req.params;
            const { name, address, latitude, longitude, gmapsLink } = req.body;

            // Check if TPS exists
            const tpsSnapshot = await db.ref(`/tps/${tpsId}`).get();
            if (!tpsSnapshot.exists()) {
                return res.status(404).json({ message: 'TPS not found' });
            }

            // Update TPS with new data
            const updatedTPS = {
                name,
                address,
                latitude,
                longitude,
                gmapsLink
            };

            await db.ref(`/tps/${tpsId}`).update(updatedTPS);
            res.status(200).json({ message: 'TPS updated successfully', tps: updatedTPS });
        } catch (error) {
            console.error('Error updating TPS', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Delete TPS by Firebase ID
    deleteTPS: async (req, res) => {
        try {
            const { tpsId } = req.params;

            // Check if TPS exists
            const tpsSnapshot = await db.ref(`/tps/${tpsId}`).get();
            if (!tpsSnapshot.exists()) {
                return res.status(404).json({ message: 'TPS not found' });
            }

            // Delete the TPS
            await db.ref(`/tps/${tpsId}`).remove();
            res.status(200).json({ message: 'TPS deleted successfully' });
        } catch (error) {
            console.error('Error deleting TPS', error);
            res.status(500).json({ error: error.message });
        }
    }
};

module.exports = tpsController;

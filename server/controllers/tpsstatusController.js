const db = require('../config/firebase');

const tpsStatusController = {

    // Get all TPS statuses
    getAllTPSStatus: async (req, res) => {
        try {
            const tpsStatusSnapshot = await db.ref('/tpsstatus').get();
            const tpsStatus = tpsStatusSnapshot.val() || {}; // Return empty object if no TPS statuses found
            res.status(200).json(tpsStatus);
        } catch (error) {
            console.error('Error getting all TPS statuses', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Add new TPS status
    addTPSStatus: async (req, res) => {
        try {
            const { tpsId, status } = req.body;

            // Check if TPS already exists
            const existingTPSSnapshot = await db.ref('/tps').child(tpsId).get();
            if (!existingTPSSnapshot.exists()) {
                return res.status(404).json({ message: 'TPS not found' });
            }

            // Create a new TPS status object
            const newTPSStatus = {
                tpsId,
                status,
                timestamp: new Date().toISOString()
            };

            // Save the new TPS status to Firebase
            const newTPSStatusRef = await db.ref('/tpsstatus').push(newTPSStatus);
            res.status(201).json({ message: 'TPS status added successfully', tpsStatus: { ...newTPSStatus, id: newTPSStatusRef.key } });
        } catch (error) {
            console.error('Error adding TPS status', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Get TPS status by ID
    getTPSStatusById: async (req, res) => {
        try {
            const tpsStatusId = req.params.tpsStatusId;

            if (!tpsStatusId || typeof tpsStatusId !== 'string') {
                return res.status(400).json({ error: 'Invalid TPS status ID' });
            }

            const tpsStatusSnapshot = await db.ref(`/tpsstatus/${tpsStatusId}`).get();

            if (!tpsStatusSnapshot.exists()) {
                return res.status(404).json({ message: 'TPS status not found' });
            }

            const tpsStatus = tpsStatusSnapshot.val();
            res.status(200).json(tpsStatus);
        } catch (error) {
            console.error('Error getting TPS status by ID', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Update TPS status by ID
    updateTPSStatus: async (req, res) => {
        try {
            const tpsStatusId = req.params.tpsStatusId;
            const { tpsId, status } = req.body;

            // Check if TPS status exists
            const tpsStatusSnapshot = await db.ref(`/tpsstatus/${tpsStatusId}`).get();
            if (!tpsStatusSnapshot.exists()) {
                return res.status(404).json({ message: 'TPS status not found' });
            }

            // Update the TPS status
            await db.ref(`/tpsstatus/${tpsStatusId}`).update({ tpsId, status, timestamp: new Date().toISOString() });
            res.status(200).json({ message: 'TPS status updated successfully' });
        } catch (error) {
            console.error('Error updating TPS status', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Delete TPS status by ID
    deleteTPSStatus: async (req, res) => {
        try {
            const tpsStatusId = req.params.tpsStatusId;

            // Check if TPS status exists
            const tpsStatusSnapshot = await db.ref(`/tpsstatus/${tpsStatusId}`).get();
            if (!tpsStatusSnapshot.exists()) {
                return res.status(404).json({ message: 'TPS status not found' });
            }

            // Delete the TPS status
            await db.ref(`/tpsstatus/${tpsStatusId}`).remove();
            res.status(200).json({ message: 'TPS status deleted successfully' });
        } catch (error) {
            console.error('Error deleting TPS status', error);
            res.status(500).json({ error: error.message });
        }
    }
};

module.exports = tpsStatusController;
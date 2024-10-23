const db = require('../config/firebase');

const pathController = {

    // Get all paths
    getAllPaths: async (req, res) => {
        try {
            const pathsSnapshot = await db.ref('/paths').get();
            const paths = pathsSnapshot.val() || {}; // Return empty object if no paths found
            res.status(200).json(paths);
        } catch (error) {
            console.error('Error getting all paths', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Add new path
    addPath: async (req, res) => {
        try {
            const { initialTPS, endTPS, distance } = req.body;

            // Check if both initialTPS and endTPS exist in the TPS collection
            const initialTPSSnapshot = await db.ref(`/tps/${initialTPS}`).get();
            const endTPSSnapshot = await db.ref(`/tps/${endTPS}`).get();

            if (!initialTPSSnapshot.exists() || !endTPSSnapshot.exists()) {
                return res.status(404).json({ message: 'One or both TPS locations do not exist' });
            }

            // Create a new path object
            const newPath = {
                initialTPS,  // Foreign key to initial TPS
                endTPS,      // Foreign key to end TPS
                distance     // Distance between the TPS locations
            };

            // Save the new path to Firebase
            const newPathRef = await db.ref('/paths').push(newPath);
            res.status(201).json({ message: 'Path added successfully', path: { ...newPath, pathId: newPathRef.key } });
        } catch (error) {
            console.error('Error adding path', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Get path by ID
    getPathById: async (req, res) => {
        try {
            const pathId = req.params.pathId;

            if (!pathId || typeof pathId !== 'string') {
                return res.status(400).json({ error: 'Invalid path ID' });
            }

            const pathsnapshot = await db.ref(`/paths/${pathId}`).get();

            if (!pathsnapshot.exists()) {
                return res.status(404).json({ message: 'Path not found' });
            }

            const path = pathsnapshot.val();
            res.status(200).json(path);
        } catch (error) {
            console.error('Error getting path by ID', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Update path by ID
    updatePath: async (req, res) => {
        try {
            const pathId = req.params.pathId;

            if (!pathId || typeof pathId !== 'string') {
                return res.status(400).json({ error: 'Invalid path ID' });
            }
            const { initialTPS, endTPS, distance } = req.body;

            // Check if path exists
            const pathsnapshot = await db.ref(`/paths/${pathId}`).get();
            if (!pathsnapshot.exists()) {
                return res.status(404).json({ message: 'path not found' });
            }

            // Update the path with new data
            const updatedPath = {
                initialTPS,
                endTPS,
                distance
            };

            await db.ref(`/paths/${pathId}`).update(updatedPath);
            res.status(200).json({ message: 'Path updated successfully', path: updatedPath });
        } catch (error) {
            console.error('Error updating path', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Delete path
    deletePath: async (req, res) => {
        try {
            const pathId = req.params.pathId;

            if (!pathId || typeof pathId !== 'string') {
                return res.status(400).json({ error: 'Invalid path ID' });
            }

            // Check if path exists
            const pathsnapshot = await db.ref(`/paths/${pathId}`).get();
            if (!pathsnapshot.exists()) {
                return res.status(404).json({ message: 'Path not found' });
            }

            // Delete the path
            await db.ref(`/paths/${pathId}`).remove();
            res.status(200).json({ message: 'Path deleted successfully' });
        } catch (error) {
            console.error('Error deleting path', error);
            res.status(500).json({ error: error.message });
        }
    }
};

module.exports = pathController;

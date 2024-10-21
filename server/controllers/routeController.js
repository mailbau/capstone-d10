const db = require('../config/firebase');

const routeController = {

    // Get all routes
    getAllRoutes: async (req, res) => {
        try {
            const routesSnapshot = await db.ref('/routes').get();
            const routes = routesSnapshot.val() || {}; // Return empty object if no routes found
            res.status(200).json(routes);
        } catch (error) {
            console.error('Error getting all routes', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Add new route
    addRoute: async (req, res) => {
        try {
            const { initialTPS, endTPS, distance } = req.body;

            // Check if both initialTPS and endTPS exist in the TPS collection
            const initialTPSSnapshot = await db.ref(`/tps/${initialTPS}`).get();
            const endTPSSnapshot = await db.ref(`/tps/${endTPS}`).get();

            if (!initialTPSSnapshot.exists() || !endTPSSnapshot.exists()) {
                return res.status(404).json({ message: 'One or both TPS locations do not exist' });
            }

            // Create a new route object
            const newRoute = {
                initialTPS,  // Foreign key to initial TPS
                endTPS,      // Foreign key to end TPS
                distance     // Distance between the TPS locations
            };

            // Save the new route to Firebase
            const newRouteRef = await db.ref('/routes').push(newRoute);
            res.status(201).json({ message: 'Route added successfully', route: { ...newRoute, routeId: newRouteRef.key } });
        } catch (error) {
            console.error('Error adding route', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Get route by ID
    getRouteById: async (req, res) => {
        try {
            const { routeId } = req.params;
            const routeSnapshot = await db.ref(`/routes/${routeId}`).get();

            if (!routeSnapshot.exists()) {
                return res.status(404).json({ message: 'Route not found' });
            }

            const route = routeSnapshot.val();
            res.status(200).json(route);
        } catch (error) {
            console.error('Error getting route by ID', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Update route
    updateRoute: async (req, res) => {
        try {
            const { routeId } = req.params;
            const { initialTPS, endTPS, distance } = req.body;

            // Check if route exists
            const routeSnapshot = await db.ref(`/routes/${routeId}`).get();
            if (!routeSnapshot.exists()) {
                return res.status(404).json({ message: 'Route not found' });
            }

            // Update the route with new data
            const updatedRoute = {
                initialTPS,
                endTPS,
                distance
            };

            await db.ref(`/routes/${routeId}`).update(updatedRoute);
            res.status(200).json({ message: 'Route updated successfully', route: updatedRoute });
        } catch (error) {
            console.error('Error updating route', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Delete route
    deleteRoute: async (req, res) => {
        try {
            const { routeId } = req.params;

            // Check if route exists
            const routeSnapshot = await db.ref(`/routes/${routeId}`).get();
            if (!routeSnapshot.exists()) {
                return res.status(404).json({ message: 'Route not found' });
            }

            // Delete the route
            await db.ref(`/routes/${routeId}`).remove();
            res.status(200).json({ message: 'Route deleted successfully' });
        } catch (error) {
            console.error('Error deleting route', error);
            res.status(500).json({ error: error.message });
        }
    }
};

module.exports = routeController;

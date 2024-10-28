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

    // Add a new route
    addRoute: async (req, res) => {
        try {
            const { pathList, totalCapacity } = req.body;

            // Calculate the total distance from the provided paths
            const totalDistance = pathList.reduce((sum, path) => sum + (path.distance || 0), 0);

            // Create a new route object
            const newRoute = {
                pathList,
                totalCapacity,
                totalDistance
            };

            // Save the new route to Firebase
            const newRouteRef = await db.ref('/routes').push(newRoute);
            res.status(201).json({ message: 'Route added successfully', route: { ...newRoute, id: newRouteRef.key } });
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

    // Update route by ID
    updateRoute: async (req, res) => {
        try {
            const { routeId } = req.params;
            const { pathList, totalCapacity } = req.body;

            // Check if route exists
            const routeSnapshot = await db.ref(`/routes/${routeId}`).get();
            if (!routeSnapshot.exists()) {
                return res.status(404).json({ message: 'Route not found' });
            }

            // Calculate the total distance from the updated path list
            const totalDistance = pathList.reduce((sum, path) => sum + (path.distance || 0), 0);

            // Update route data
            const updatedRoute = {
                pathList,
                totalCapacity,
                totalDistance
            };

            await db.ref(`/routes/${routeId}`).update(updatedRoute);
            res.status(200).json({ message: 'Route updated successfully', updatedRoute });
        } catch (error) {
            console.error('Error updating route', error);
            res.status(500).json({ error: error.message });
        }
    },

    // Delete route by ID
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

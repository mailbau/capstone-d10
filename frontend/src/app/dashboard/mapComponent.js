import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const MapComponent = () => {
    const mapRef = useRef(null);

    useEffect(() => {
        const initializeMap = async () => {
            const fetchRouteData = async () => {
                try {
                    // Fetch the latest route data
                    // const routeResponse = await fetch('http://localhost:8080/route/latest');
                    const routeResponse = await fetch('https://capstoned10.duckdns.org//route/latest');
                    const routeData = await routeResponse.json();

                    console.log("Route API Response:", routeData);

                    // Extract the route information from the response
                    const latestRouteKey = Object.keys(routeData)[0];
                    const latestRoute = routeData[latestRouteKey];

                    if (!latestRoute || !latestRoute.route) {
                        console.warn("No route data found in the latest route.");
                        return null;
                    }

                    return latestRoute;
                } catch (error) {
                    console.error("Error fetching route data:", error);
                    return null;
                }
            };

            const routeData = await fetchRouteData();

            if (!routeData) {
                console.error("Failed to load route data.");
                return;
            }

            // Initialize the map with a default view
            const map = L.map(mapRef.current).setView([-7.7051764, 110.3605896], 12);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);

            const waypoints = [];
            routeData.route.forEach((segment, index) => {
                const startCoordinates = segment.start.coordinates;
                const endCoordinates = segment.end.coordinates;

                // Add start coordinates as a waypoint if it's the first segment
                if (index === 0) {
                    waypoints.push(
                        L.latLng(parseFloat(startCoordinates[0]), parseFloat(startCoordinates[1]))
                    );
                    L.marker(startCoordinates)
                        .addTo(map)
                        .bindPopup(`<strong>Starting Point: ${segment.start.name}</strong>`)
                        .openPopup();
                }

                // Add end coordinates as a waypoint
                waypoints.push(
                    L.latLng(parseFloat(endCoordinates[0]), parseFloat(endCoordinates[1]))
                );

                // Label each destination sequentially
                const destinationLabel = `Destination ${index + 2}`;
                L.marker(endCoordinates)
                    .addTo(map)
                    .bindPopup(`<strong>${destinationLabel}: ${segment.end.name}</strong>`)
                    .openPopup();

                // Label the final destination explicitly
                if (index === routeData.route.length - 1) {
                    L.marker(endCoordinates)
                        .addTo(map)
                        .bindPopup(`<strong>Final Destination: ${segment.end.name}</strong>`);
                }
            });

            // Add the route to the map using Leaflet Routing Machine
            L.Routing.control({
                waypoints: waypoints,
                show: false,
                lineOptions: {
                    styles: [{ color: 'red', opacity: 0.6, weight: 4 }]
                },
                createMarker: function () { return null; } // Remove default markers if you already added custom ones
            }).addTo(map);
        };

        initializeMap();
    }, []);

    return <div ref={mapRef} style={{ width: '100%', height: '100%' }} />;
};

export default MapComponent;
from flask import Blueprint, request, jsonify
from firebase_admin import db
from itertools import permutations
import requests
import numpy as np
import networkx as nx
import heapq

route_controller = Blueprint('route_controller', __name__)

# Firebase id for garage and destination
GARAGE_ID = "-OAbvaj7i0rvIdbk8KIb"
DESTINATION_ID = "-OAkudzPCsvVxg3nVb4R"

# Helper function to fetch data from endpoints
def fetch_tps_data():
    response = requests.get("http://localhost:8080/tps")
    return response.json()

def fetch_tps_status():
    response = requests.get("http://localhost:8080/tpsstatus")
    return response.json()

def fetch_paths():
    response = requests.get("http://localhost:8080/path")
    return response.json()

# A* route optimization to visit all nodes (bins)
def calculate_optimal_route(tps_data, tps_status, paths_data):
    G = nx.Graph()

    # Build the graph with provided path data
    for path_id, path in paths_data.items():
        G.add_edge(path['initialTPS'], path['endTPS'], weight=path['distance'])

    # Define mandatory stops: all bins except Garage and Destination
    mandatory_stops = [node for node in tps_data.keys() if node not in {GARAGE_ID, DESTINATION_ID}]
    best_route = None
    best_distance = float('inf')

    # Iterate through all permutations of mandatory stops
    for perm in permutations(mandatory_stops):
        current_route = [GARAGE_ID] + list(perm) + [DESTINATION_ID]
        current_distance = 0
        current_load = 0
        valid_route = True

        # Calculate the total distance for this route
        for i in range(len(current_route) - 1):
            start, end = current_route[i], current_route[i + 1]

            # Add load if the node is a bin
            if start in tps_status:
                current_load += int(tps_data[start]['capacity'] * tps_status[start]['status'])

            # Check capacity constraint
            if current_load > 10:  # Vehicle capacity
                valid_route = False
                break

            # Calculate path length
            if G.has_edge(start, end):
                current_distance += G[start][end]['weight']
            else:
                valid_route = False
                break

        # Update the best route if the current one is valid and shorter
        if valid_route and current_distance < best_distance:
            best_route = current_route
            best_distance = current_distance

    # Prepare output format
    if best_route is None:
        return None, None  # No valid route found

    optimal_path_list = []
    for i in range(len(best_route) - 1):
        initial, end = best_route[i], best_route[i + 1]
        # Find the path ID that connects these two nodes
        for path_id, path in paths_data.items():
            if path['initialTPS'] == initial and path['endTPS'] == end:
                optimal_path_list.append({
                    "pathId": path_id,
                    "initialTPS": initial,
                    "endTPS": end,
                    "distance": path['distance'],
                    "pathName": path['pathName']
                })
                break

    # Calculate total capacity used based on best route
    total_capacity = sum(tps_data[node]['capacity'] for node in best_route if node in tps_data)

    return optimal_path_list, best_distance, total_capacity

# Calculate and save the optimal route
@route_controller.route('/calculate_route', methods=['POST'])
def calculate_route():
    try:
        # Fetch data from other endpoints
        tps_data = fetch_tps_data()
        tps_status = fetch_tps_status()
        paths_data = fetch_paths()

        # Calculate optimal route
        optimal_path_list, best_distance, total_capacity = calculate_optimal_route(tps_data, tps_status, paths_data)
        
        if optimal_path_list is None:
            return jsonify({"error": "No valid route found"}), 404

        # Create a new route object
        new_route = {
            "pathList": optimal_path_list,
            "totalCapacity": total_capacity,
            "totalDistance": best_distance
        }

        # Save the new route to Firebase
        new_route_ref = db.reference('/routes').push(new_route)
        return jsonify({
            "message": "Optimal route calculated and added successfully",
            "route": {**new_route, "id": new_route_ref.key}
        }), 201

    except Exception as error:
        print("Error calculating optimal route:", error)
        return jsonify({"error": str(error)}), 500


# Get all routes
@route_controller.route('/routes', methods=['GET'])
def get_all_routes():
    try:
        routes_snapshot = db.reference('/routes').get()
        routes = routes_snapshot or {}  # Return empty dictionary if no routes found
        return jsonify(routes), 200
    except Exception as error:
        print('Error getting all routes:', error)
        return jsonify({'error': str(error)}), 500

# Add a new route
@route_controller.route('/routes', methods=['POST'])
def add_route():
    try:
        data = request.get_json()
        path_list = data.get('pathList', [])
        total_capacity = data.get('totalCapacity', 0)

        # Calculate the total distance from the provided paths
        total_distance = sum(path.get('distance', 0) for path in path_list)

        # Create a new route object
        new_route = {
            'pathList': path_list,
            'totalCapacity': total_capacity,
            'totalDistance': total_distance
        }

        # Save the new route to Firebase
        new_route_ref = db.reference('/routes').push(new_route)
        return jsonify({'message': 'Route added successfully', 'route': {**new_route, 'id': new_route_ref.key}}), 201
    except Exception as error:
        print('Error adding route:', error)
        return jsonify({'error': str(error)}), 500

# Get route by ID
@route_controller.route('/routes/<route_id>', methods=['GET'])
def get_route_by_id(route_id):
    try:
        route_snapshot = db.reference(f'/routes/{route_id}').get()

        if not route_snapshot:
            return jsonify({'message': 'Route not found'}), 404

        return jsonify(route_snapshot), 200
    except Exception as error:
        print('Error getting route by ID:', error)
        return jsonify({'error': str(error)}), 500

# Update route by ID
@route_controller.route('/routes/<route_id>', methods=['PUT'])
def update_route(route_id):
    try:
        data = request.get_json()
        path_list = data.get('pathList', [])
        total_capacity = data.get('totalCapacity', 0)

        # Check if route exists
        route_snapshot = db.reference(f'/routes/{route_id}').get()
        if not route_snapshot:
            return jsonify({'message': 'Route not found'}), 404

        # Calculate the total distance from the updated path list
        total_distance = sum(path.get('distance', 0) for path in path_list)

        # Update route data
        updated_route = {
            'pathList': path_list,
            'totalCapacity': total_capacity,
            'totalDistance': total_distance
        }

        db.reference(f'/routes/{route_id}').update(updated_route)
        return jsonify({'message': 'Route updated successfully', 'updatedRoute': updated_route}), 200
    except Exception as error:
        print('Error updating route:', error)
        return jsonify({'error': str(error)}), 500

# Delete route by ID
@route_controller.route('/routes/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    try:
        # Check if route exists
        route_snapshot = db.reference(f'/routes/{route_id}').get()
        if not route_snapshot:
            return jsonify({'message': 'Route not found'}), 404

        # Delete the route
        db.reference(f'/routes/{route_id}').delete()
        return jsonify({'message': 'Route deleted successfully'}), 200
    except Exception as error:
        print('Error deleting route:', error)
        return jsonify({'error': str(error)}), 500

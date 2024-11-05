from flask import Blueprint, request, jsonify
from firebase_admin import db
from itertools import permutations
import requests
import numpy as np
import networkx as nx
import heapq

from app.algorithm.astar import AStarAlgorithm

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


def convert_to_dict_format(tps_data, tps_status_data, path_data):
    # Extracting point data
    point_dict = []
    tps_id_to_point_id = {}
    point_id = 0
    for tps_id, tps_info in tps_data.items():
        # Find demand/status value for the tps_id or default to 0.0
        status_entry = next((status for status in tps_status_data.values() if status['tpsId'] == tps_id), None)
        demand_value = status_entry['status'] if status_entry else 0.0
        
        point_dict.append({
            "point": point_id, 
            "name": tps_info["name"], 
            "coordinates": (float(tps_info["latitude"]), float(tps_info["longitude"])), 
            "demand": demand_value
        })
        tps_id_to_point_id[tps_id] = point_id
        point_id += 1
    
    # Extracting path data
    path_dict = []
    for path_id_str, path_info in path_data.items():
        start_id = tps_id_to_point_id[path_info["initialTPS"]]
        end_id = tps_id_to_point_id[path_info["endTPS"]]
        path_dict.append({
            "path_id": path_id_str, 
            "start_id": start_id, 
            "end_id": end_id, 
            "distance": path_info["distance"]
        })
    
    return point_dict, path_dict


# Calculate and save the optimal route
@route_controller.route('/calculate_route', methods=['POST'])
def calculate_route():
    try:
        # Fetch data from other endpoints
        tps_data = fetch_tps_data()
        tps_status = fetch_tps_status()
        paths_data = fetch_paths()

        # Calculate optimal route
        point_dict, path_dict = convert_to_dict_format(tps_data, tps_status, paths_data)
        max_capacity = 11.0
        weights = (0.4, 0.4, 0.2)
        start_point = "Dinas Lingkungan Hidup"
        end_point = "Dinas Lingkungan Hidup"
        a_star = AStarAlgorithm(point_dict, path_dict, max_capacity, weights, end_point)
        
        optimal_path = a_star(start_point)
        
        if optimal_path is None:
            return jsonify({"error": "No valid route found"}), 404

        # Save the new route to Firebase
        new_route_ref = db.reference('/routes').push(optimal_path)
        return jsonify({
            "message": "Optimal route calculated and added successfully",
            "route": {**optimal_path, "id": new_route_ref.key}
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

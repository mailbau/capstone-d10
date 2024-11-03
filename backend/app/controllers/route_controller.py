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

# A* route optimization with capacity-based unloading added to path list
def calculate_optimal_route(tps_data, tps_status, paths_data, vehicle_capacity=8):
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
        current_route = [GARAGE_ID]
        path_list = []
        current_distance = 0
        current_load = 0
        unvisited_nodes = list(perm)  # Initialize unvisited nodes queue

        while unvisited_nodes:
            node = unvisited_nodes.pop(0)  # Visit next node in the queue

            if node in tps_status:
                # Calculate the load from this node
                added_load = int(tps_data[node]['capacity'] * tps_status[node]['status'])
                current_load += added_load

            # Check if the vehicle has reached or exceeded capacity
            if current_load >= vehicle_capacity:
                # Detour to the destination to unload
                last_node = current_route[-1]  # Node before going to the destination
                path_to_dest = nx.shortest_path(G, source=last_node, target=DESTINATION_ID, weight='weight')
                
                # Add segments in the route to the destination
                for i in range(len(path_to_dest) - 1):
                    initial, end = path_to_dest[i], path_to_dest[i + 1]
                    distance = G[initial][end]['weight']
                    path_id = next((pid for pid, pdata in paths_data.items() if pdata['initialTPS'] == initial and pdata['endTPS'] == end), None)
                    path_list.append({
                        "pathId": path_id,
                        "initialTPS": initial,
                        "endTPS": end,
                        "distance": distance,
                        "pathName": paths_data[path_id]['pathName'] if path_id else "Unknown"
                    })
                    current_distance += distance

                # Reset load and update current route
                current_load = 0  # Unload completely at destination
                current_route.append(DESTINATION_ID)

                # After unloading, determine next node to visit
                if unvisited_nodes:
                    # Shortest path from destination to the next unvisited node
                    next_node = unvisited_nodes[0]
                    path_from_dest = nx.shortest_path(G, source=DESTINATION_ID, target=next_node, weight='weight')

                    # Add segments from destination to next node
                    for i in range(len(path_from_dest) - 1):
                        initial, end = path_from_dest[i], path_from_dest[i + 1]
                        distance = G[initial][end]['weight']
                        path_id = next((pid for pid, pdata in paths_data.items() if pdata['initialTPS'] == initial and pdata['endTPS'] == end), None)
                        path_list.append({
                            "pathId": path_id,
                            "initialTPS": initial,
                            "endTPS": end,
                            "distance": distance,
                            "pathName": paths_data[path_id]['pathName'] if path_id else "Unknown"
                        })
                        current_distance += distance

                    # Update current route to include the path from destination to the next node
                    current_route.extend(path_from_dest[1:])  # Skip adding destination itself twice
                continue  # Skip to next node in the while loop

            # If under capacity, add node to route normally
            if current_route[-1] != node:  
                current_route.append(node)

        # Finally, add the destination to complete the route
        current_route.append(DESTINATION_ID)

        # Calculate paths and distances for the completed route
        for i in range(len(current_route) - 1):
            initial, end = current_route[i], current_route[i + 1]
            if G.has_edge(initial, end):
                distance = G[initial][end]['weight']
                path_id = next((pid for pid, pdata in paths_data.items() if pdata['initialTPS'] == initial and pdata['endTPS'] == end), None)
                path_list.append({
                    "pathId": path_id,
                    "initialTPS": initial,
                    "endTPS": end,
                    "distance": distance,
                    "pathName": paths_data[path_id]['pathName'] if path_id else "Unknown"
                })
                current_distance += distance
            else:
                path_list = None
                break

        # Update best route if the current one is valid and shorter
        if path_list and current_distance < best_distance:
            best_route = current_route
            best_distance = current_distance

    if best_route is None:
        return None, None, None

    total_capacity = sum(tps_data[node]['capacity'] for node in best_route if node in tps_data)
    return path_list, best_distance, total_capacity


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

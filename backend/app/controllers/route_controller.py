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
    # response = requests.get("http://localhost:8080/tps")
    response = requests.get("https://capstoned10.duckdns.org/tps")
    return response.json()

def fetch_tps_status():
    # response = requests.get("http://localhost:8080/tpsstatus")
    response = requests.get("https://capstoned10.duckdns.org/tpsstatus")
    return response.json()

def fetch_paths():
    # response = requests.get("http://localhost:8080/path")
    response = requests.get("https://capstoned10.duckdns.org/path")
    return response.json()

def fetch_dummy_tps_status():
    # response = requests.get("http://localhost:8080/tpsstatus/dummy")
    response = requests.get("https://capstoned10.duckdns.org/tpsstatus/dummy")
    return response.json()

def convert_to_dict_format(tps_data, tps_status_data, path_data):
    # Extracting point data
    point_dict = []
    tps_id_to_point_id = {}
    point_id = 0
    
    for tps_id, tps_info in tps_data.items():
        # For real data, find status entry by matching tpsId
        status_entry = next((status for status in tps_status_data.values() if status['tpsId'] == tps_id), None)
        demand_value = status_entry['status'] if status_entry else 0.0

        # Add point details
        point_dict.append({
            "point": point_id, 
            "name": tps_info["name"], 
            "coordinates": (float(tps_info["latitude"]), float(tps_info["longitude"])), 
            "demand": demand_value * tps_info["capacity"]
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


def calculate_final_route(start_point, final_end_point, max_capacity, weights):
    # Fetch data from other endpoints
    tps_data = fetch_tps_data()
    tps_status = fetch_tps_status()
    paths_data = fetch_paths()

    # Initialize
    point_dict, path_dict = convert_to_dict_format(tps_data, tps_status, paths_data)
    final_route = []
    unvisited_points = {point['point'] for point in point_dict}  # Track unvisited nodes

    current_start = start_point
    route_num = 1
    total_objective_value = 0
    total_distance = 0
    end_point = None
    updated_max_capacity = max_capacity

    original_a_star = AStarAlgorithm(point_dict, path_dict, updated_max_capacity, weights, end_point)
    while updated_max_capacity > 0:
        a_star = AStarAlgorithm(point_dict, path_dict, updated_max_capacity, weights, end_point)
        optimal_path = a_star(current_start)
        # print("optimal_path", optimal_path)

        if not optimal_path or not optimal_path["path_list"]:
            break  # Stop if no further path is returned

        # Filter path to include only unvisited nodes and update their demand to 0
        filtered_path = [
            point for point in optimal_path["path_list"] if point in unvisited_points
        ]
        
        for point in filtered_path:
            unvisited_points.discard(point)  # Mark as visited
            next((p for p in point_dict if p['point'] == point), {})['demand'] = 0  # Set occupancy to 0

        # Append the filtered path to final_route and update cumulative stats
        final_route.extend(filtered_path)
        # print(optimal_path["path"])
        total_objective_value += optimal_path["objective_value"]
        total_distance += optimal_path["total_distance"]
        updated_max_capacity = optimal_path["unused_capacity"]  # Update capacity for next trip

        # Prepare for the next loop
        current_start = optimal_path["path"][-1]["end"]["name"]  # Set previous destination as the new starting point
        route_num += 1

    # Generate path data for the final combined route
    final_path_data, additional_distance = original_a_star.generate_path_data(final_route, final_end_point)  # Generate data for the entire combined route
    total_objective_value = original_a_star.calculate_objective_value(final_route)  # Calculate objective value for the entire
    return {
        "route": final_path_data,
        "path_list": final_route,
        "total_objective_value": total_objective_value,
        "total_distance": total_distance + additional_distance
    }

    # final_route = []

    # # Find the ID of the end_point
    # end_point_id = next((point['point'] for point in point_dict if point['name'] == end_point), None)

    # # Initialize unvisited points, excluding points with 0% status and the end point
    # unvisited_points = {
    #     point['point'] for point in point_dict
    #     if point['point'] != end_point_id and point_dict[point['point']]['demand'] > 0
    # }
    # print("Unvisited points (excluding 0% status and end point):", unvisited_points)
    
    # current_capacity = 0
    # current_start = start_point
    # total_objective_value = 0
    # total_distance = 0

    # while unvisited_points:
    #     print(f"Current start point: {current_start}")
    #     # Find the optimal path using A* Algorithm
    #     a_star = AStarAlgorithm(point_dict, path_dict, max_capacity, weights, end_point)
    #     optimal_path = a_star(current_start)
    #     print("Optimal path found:", optimal_path)

    #     if not optimal_path or not optimal_path["path_list"]:
    #         print("No valid path found, breaking out of loop.")
    #         break  # Stop if no further path is returned

    #     # Filter path to include only unvisited nodes and check for capacity
    #     filtered_path = []
    #     for point in optimal_path["path_list"]:
    #         print(f"Checking point: {point}")
            
    #         # Skip the end point during route selection
    #         if point == end_point_id:
    #             print(f"Skipping end point: {end_point_id}")
    #             continue  # Skip end point unless capacity exceeds

    #         if point in unvisited_points:
    #             # Debug: print the point's demand
    #             point_demand = point_dict[point]["demand"]
    #             print(f"Point {point} demand: {point_demand}, current capacity: {current_capacity}")
                
    #             # Check if visiting this point would exceed capacity
    #             if current_capacity + point_demand > max_capacity:
    #                 print(f"Capacity exceeded by {point}. Unloading at {end_point_id}...")
    #                 final_route.append(end_point_id)  # Unload at end point
    #                 current_capacity = 0  # Reset capacity after unloading
    #                 break  # Exit loop to start the next trip

    #             # Add the point if it doesn't exceed capacity
    #             print(f"Visiting point {point}, updating capacity...")
    #             filtered_path.append(point)
    #             current_capacity += point_demand  # Add demand to capacity
    #             print(f"Updated current capacity: {current_capacity}")
    #             unvisited_points.discard(point)  # Remove from unvisited points
    #             point_dict[point]["demand"] = 0  # Set demand to 0 as it's been visited
    #         else:
    #             print(f"Cannot visit point {point}: already visited or exceeds capacity.")

    #     print(f"Filtered path: {filtered_path}")

    #     # Add the filtered path to the final route and update total stats
    #     final_route.extend(filtered_path)
    #     total_objective_value += optimal_path["objective_value"]
    #     total_distance += optimal_path["total_distance"]

    #     # Set the current start point for the next loop
    #     if current_capacity == 0:
    #         current_start = end_point_id  # Unload and reset to the end point
    #     else:
    #         current_start = filtered_path[-1]  # Continue from the last valid point
    #     print(f"New start point: {current_start}")

    # # At the end, if all nodes have been visited, return to end_point
    # if current_capacity > 0:
    #     print(f"Returning to end point: {end_point}")
    #     final_route.append(end_point_id)

    # print("Final route:", final_route)

    # # Generate path data for the final combined route
    # final_path_data = a_star.generate_path_data(final_route)
    # print("Final path data generated:")

    # return {
    #     "route": final_path_data,
    #     "path_list": final_route,
    #     "total_objective_value": total_objective_value,
    #     "total_distance": total_distance
    # }
    # # except Exception as e:
    # #     print("Error during route calculation:", str(e))
    # #     raise  # Re-raise the exception for further logging by outer layers

# Calculate final route logic
def calculate_final_route_dummy(start_point, end_point, max_capacity, weights):
    try:
        print("Fetching TPS data...")
        # Fetch data from other endpoints
        tps_data = fetch_tps_data()
        print("TPS data fetched:")
        
        print("Fetching dummy TPS status...")
        dummy_tps_status = fetch_dummy_tps_status()
        print("Dummy TPS status fetched:")
        
        print("Fetching paths data...")
        paths_data = fetch_paths()
        print("Paths data fetched:")

        tps_ids = [
            "-OAS440Ha7EjF_f2MTwm", "-OAS440tFje7vRLUVQUf", "-OAS441ZAN7E0u1No34N",
            "-OAS442SU8h3E1yMe2Mh", "-OAS4430aL4reZbpSh0n", "-OAS443ap0dJTlq7UzAI",
            "-OAS4449SiRLtCXJk3B7", "-OAS444fRJ-t7ZUZDVWU", "-OAS445FOs-bHdQf7GnI"
        ]

        # Convert dummy data to real format by assigning IDs and converting percentages to status
        print("Converting dummy data to real format...")
        tps_status = {
            tps_id: {
                "status": float(dummy_tps_status[f"tps_{i+1}"]["percentage"]) / 100,
                "timestamp": "2024-11-02T03:10:59.855Z",  # Dummy timestamp for all entries
                "tpsId": tps_id
            }
            for i, tps_id in enumerate(tps_ids) if f"tps_{i+1}" in dummy_tps_status
        }
        print("Converted TPS status:")

        # Initialize
        print("Initializing route calculation...")
        point_dict, path_dict = convert_to_dict_format(tps_data, tps_status, paths_data)
        print("Point dictionary:", point_dict)

        final_route = []

        # Find the ID of the end_point
        end_point_id = next((point['point'] for point in point_dict if point['name'] == end_point), None)

        # Initialize unvisited points, excluding points with 0% status and the end point
        unvisited_points = {
            point['point'] for point in point_dict
            if point['point'] != end_point_id and point_dict[point['point']]['demand'] > 0
        }
        print("Unvisited points (excluding 0% status and end point):", unvisited_points)
        
        current_capacity = 0
        current_start = start_point
        total_objective_value = 0
        total_distance = 0

        while unvisited_points:
            print(f"Current start point: {current_start}")
            # Find the optimal path using A* Algorithm
            a_star = AStarAlgorithm(point_dict, path_dict, max_capacity, weights, end_point)
            optimal_path = a_star(current_start)
            print("Optimal path found:", optimal_path)

            if not optimal_path or not optimal_path["path_list"]:
                print("No valid path found, breaking out of loop.")
                break  # Stop if no further path is returned

            # Filter path to include only unvisited nodes and check for capacity
            filtered_path = []
            for point in optimal_path["path_list"]:
                print(f"Checking point: {point}")
                
                # Skip the end point during route selection
                if point == end_point_id:
                    print(f"Skipping end point: {end_point_id}")
                    continue  # Skip end point unless capacity exceeds

                if point in unvisited_points:
                    # Debug: print the point's demand
                    point_demand = point_dict[point]["demand"]
                    print(f"Point {point} demand: {point_demand}, current capacity: {current_capacity}")
                    
                    # Check if visiting this point would exceed capacity
                    if current_capacity + point_demand > max_capacity:
                        print(f"Capacity exceeded by {point}. Unloading at {end_point_id}...")
                        final_route.append(end_point_id)  # Unload at end point
                        current_capacity = 0  # Reset capacity after unloading
                        break  # Exit loop to start the next trip

                    # Add the point if it doesn't exceed capacity
                    print(f"Visiting point {point}, updating capacity...")
                    filtered_path.append(point)
                    current_capacity += point_demand  # Add demand to capacity
                    print(f"Updated current capacity: {current_capacity}")
                    unvisited_points.discard(point)  # Remove from unvisited points
                    point_dict[point]["demand"] = 0  # Set demand to 0 as it's been visited
                else:
                    print(f"Cannot visit point {point}: already visited or exceeds capacity.")

            print(f"Filtered path: {filtered_path}")

            # Add the filtered path to the final route and update total stats
            final_route.extend(filtered_path)
            total_objective_value += optimal_path["objective_value"]
            total_distance += optimal_path["total_distance"]

            # Set the current start point for the next loop
            if current_capacity == 0:
                current_start = end_point_id  # Unload and reset to the end point
            else:
                current_start = filtered_path[-1]  # Continue from the last valid point
            print(f"New start point: {current_start}")

        # At the end, if all nodes have been visited, return to end_point
        if current_capacity > 0:
            print(f"Returning to end point: {end_point}")
            final_route.append(end_point_id)

        print("Final route:", final_route)

        # Generate path data for the final combined route
        final_path_data = a_star.generate_path_data(final_route)
        print("Final path data generated:")

        return {
            "route": final_path_data,
            "path_list": final_route,
            "total_objective_value": total_objective_value,
            "total_distance": total_distance
        }
    except Exception as e:
        print("Error during route calculation:", str(e))
        raise  # Re-raise the exception for further logging by outer layers

# Calculate the final optimal route
@route_controller.route('/calculate_route', methods=['POST'])
def calculate_route():
    try:
        # Initial parameters
        max_capacity = 20.0
        weights = (0.35, 0.35, 0.3)
        start_point = "Dinas Lingkungan Hidup"  # Defined starting point (garage)
        end_point = "TPST SENDANGSARI"  # Defined destination

        # Calculate the final combined optimal route
        final_route = calculate_final_route(start_point, end_point, max_capacity, weights)

        if not final_route["path_list"]:
            return jsonify({"error": "No valid route found"}), 404

        # Save the final combined route to Firebase
        new_route_ref = db.reference('/routes').push(final_route)
        
        return jsonify({
            "message": "Final optimal route calculated and added successfully",
            "route": {**final_route, "id": new_route_ref.key}
        }), 201

    except Exception as error:
        print("Error calculating final route:", error)
        return jsonify({"error": str(error)}), 500

# Calculate the final optimal route with dummy data
@route_controller.route('/calculate_route/dummy', methods=['POST'])
def calculate_dummy():
    try:
        # Initial parameters
        max_capacity = 10.0
        weights = (0.35, 0.35, 0.3)
        start_point = "Dinas Lingkungan Hidup"  # Defined starting point (garage)
        end_point = "TPST SENDANGSARI"  # Defined destination

        # Calculate the final combined optimal route
        final_route = calculate_final_route_dummy(start_point, end_point, max_capacity, weights)

        if not final_route["path_list"]:
            return jsonify({"error": "No valid route found"}), 404

        # Save the final combined route to Firebase
        new_route_ref = db.reference('/routes').push(final_route)
        
        return jsonify({
            "message": "Final optimal route calculated and added successfully",
            "route": {**final_route, "id": new_route_ref.key}
        }), 201

    except Exception as error:
        print("Error calculating final route:", error)
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

# Get the latest route
@route_controller.route('/routes/latest', methods=['GET'])
def get_latest_route():
    try:
        # Fetch all routes in the routes folder
        routes_snapshot = db.reference('/routes').get()
        routes = routes_snapshot or {}  # Use an empty dictionary if no routes found

        # Find the latest route based on key sorting (Firebase keys are in chronological order)
        latest_route_key = max(routes.keys()) if routes else None
        latest_route = routes[latest_route_key] if latest_route_key else {}

        return jsonify({latest_route_key: latest_route}), 200
    except Exception as error:
        print('Error getting latest route:', error)
        return jsonify({'error': str(error)}), 500

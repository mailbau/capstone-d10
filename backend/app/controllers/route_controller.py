from flask import Blueprint, request, jsonify
from firebase_admin import db

route_controller = Blueprint('route_controller', __name__)

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

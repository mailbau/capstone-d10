from flask import Blueprint, request, jsonify
from firebase_admin import db

path_controller = Blueprint('path_controller', __name__)

# Get all paths
@path_controller.route('/paths', methods=['GET'])
def get_all_paths():
    try:
        paths_snapshot = db.reference('/paths').get()
        paths = paths_snapshot or {}  # Return empty dictionary if no paths found
        return jsonify(paths), 200
    except Exception as error:
        print('Error getting all paths:', error)
        return jsonify({'error': str(error)}), 500

# Add new path
@path_controller.route('/paths', methods=['POST'])
def add_path():
    try:
        data = request.get_json()
        path_name = data.get('pathName')
        initial_tps = data.get('initialTPS')
        end_tps = data.get('endTPS')
        distance = data.get('distance')

        # Check if both initialTPS and endTPS exist in the TPS collection
        initial_tps_snapshot = db.reference(f'/tps/{initial_tps}').get()
        end_tps_snapshot = db.reference(f'/tps/{end_tps}').get()

        if not initial_tps_snapshot or not end_tps_snapshot:
            return jsonify({'message': 'One or both TPS locations do not exist'}), 404

        # Create a new path object
        new_path = {
            'pathName': path_name,
            'initialTPS': initial_tps,
            'endTPS': end_tps,
            'distance': distance
        }

        # Save the new path to Firebase
        new_path_ref = db.reference('/paths').push(new_path)
        return jsonify({'message': 'Path added successfully', 'path': {**new_path, 'pathId': new_path_ref.key}}), 201
    except Exception as error:
        print('Error adding path:', error)
        return jsonify({'error': str(error)}), 500

# Get path by ID
@path_controller.route('/paths/<path_id>', methods=['GET'])
def get_path_by_id(path_id):
    try:
        if not path_id or not isinstance(path_id, str):
            return jsonify({'error': 'Invalid path ID'}), 400

        path_snapshot = db.reference(f'/paths/{path_id}').get()

        if not path_snapshot:
            return jsonify({'message': 'Path not found'}), 404

        return jsonify(path_snapshot), 200
    except Exception as error:
        print('Error getting path by ID:', error)
        return jsonify({'error': str(error)}), 500

# Update path by ID
@path_controller.route('/paths/<path_id>', methods=['PUT'])
def update_path(path_id):
    try:
        if not path_id or not isinstance(path_id, str):
            return jsonify({'error': 'Invalid path ID'}), 400

        data = request.get_json()
        initial_tps = data.get('initialTPS')
        end_tps = data.get('endTPS')
        distance = data.get('distance')

        # Check if path exists
        path_snapshot = db.reference(f'/paths/{path_id}').get()
        if not path_snapshot:
            return jsonify({'message': 'Path not found'}), 404

        # Update the path with new data
        updated_path = {
            'initialTPS': initial_tps,
            'endTPS': end_tps,
            'distance': distance
        }

        db.reference(f'/paths/{path_id}').update(updated_path)
        return jsonify({'message': 'Path updated successfully', 'path': updated_path}), 200
    except Exception as error:
        print('Error updating path:', error)
        return jsonify({'error': str(error)}), 500

# Delete path by ID
@path_controller.route('/paths/<path_id>', methods=['DELETE'])
def delete_path(path_id):
    try:
        if not path_id or not isinstance(path_id, str):
            return jsonify({'error': 'Invalid path ID'}), 400

        # Check if path exists
        path_snapshot = db.reference(f'/paths/{path_id}').get()
        if not path_snapshot:
            return jsonify({'message': 'Path not found'}), 404

        # Delete the path
        db.reference(f'/paths/{path_id}').delete()
        return jsonify({'message': 'Path deleted successfully'}), 200
    except Exception as error:
        print('Error deleting path:', error)
        return jsonify({'error': str(error)}), 500

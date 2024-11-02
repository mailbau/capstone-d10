from flask import Blueprint, request, jsonify
from firebase_admin import db

tps_controller = Blueprint('tps_controller', __name__)

# Get all TPS locations
@tps_controller.route('/tps', methods=['GET'])
def get_all_tps():
    try:
        tps_ref = db.reference('/tps')
        tps_snapshot = tps_ref.get()
        tps = tps_snapshot or {}  # Return empty dictionary if no TPS records found
        return jsonify(tps), 200
    except Exception as error:
        print('Error getting all TPS:', error)
        return jsonify({'error': str(error)}), 500

# Add new TPS
@tps_controller.route('/tps', methods=['POST'])
def add_tps():
    try:
        data = request.json
        new_tps = {
            'name': data.get('name'),
            'address': data.get('address'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'gmapsLink': data.get('gmapsLink'),
            'capacity': data.get('capacity')
        }

        new_tps_ref = db.reference('/tps').push(new_tps)
        return jsonify({'message': 'TPS added successfully', 'tps': {**new_tps, 'id': new_tps_ref.key}}), 201
    except Exception as error:
        print('Error adding TPS:', error)
        return jsonify({'error': str(error)}), 500

# Get TPS by Firebase ID
@tps_controller.route('/tps/<tps_id>', methods=['GET'])
def get_tps_by_id(tps_id):
    try:
        tps_ref = db.reference(f'/tps/{tps_id}')
        tps_snapshot = tps_ref.get()

        if tps_snapshot is None:
            return jsonify({'message': 'TPS not found'}), 404

        return jsonify(tps_snapshot), 200
    except Exception as error:
        print('Error getting TPS by ID:', error)
        return jsonify({'error': str(error)}), 500

# Update TPS by Firebase ID
@tps_controller.route('/tps/<tps_id>', methods=['PUT'])
def update_tps(tps_id):
    try:
        data = request.json
        tps_ref = db.reference(f'/tps/{tps_id}')
        tps_snapshot = tps_ref.get()

        if tps_snapshot is None:
            return jsonify({'message': 'TPS not found'}), 404

        updated_tps = {
            'name': data.get('name'),
            'address': data.get('address'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'gmapsLink': data.get('gmapsLink'),
            'capacity': data.get('capacity')
        }

        tps_ref.update(updated_tps)
        return jsonify({'message': 'TPS updated successfully', 'tps': updated_tps}), 200
    except Exception as error:
        print('Error updating TPS:', error)
        return jsonify({'error': str(error)}), 500

# Delete TPS by Firebase ID
@tps_controller.route('/tps/<tps_id>', methods=['DELETE'])
def delete_tps(tps_id):
    try:
        tps_ref = db.reference(f'/tps/{tps_id}')
        tps_snapshot = tps_ref.get()

        if tps_snapshot is None:
            return jsonify({'message': 'TPS not found'}), 404

        tps_ref.delete()
        return jsonify({'message': 'TPS deleted successfully'}), 200
    except Exception as error:
        print('Error deleting TPS:', error)
        return jsonify({'error': str(error)}), 500

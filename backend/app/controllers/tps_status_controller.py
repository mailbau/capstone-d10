from flask import Blueprint, request, jsonify
from firebase_admin import db
from datetime import datetime

tps_status_controller = Blueprint('tps_status_controller', __name__)

# Get all TPS statuses
@tps_status_controller.route('/tpsstatus', methods=['GET'])
def get_all_tps_status():
    try:
        tps_status_snapshot = db.reference('/tpsstatus').get()
        tps_status = tps_status_snapshot or {}  # Return empty dictionary if no TPS statuses found
        return jsonify(tps_status), 200
    except Exception as error:
        print('Error getting all TPS statuses:', error)
        return jsonify({'error': str(error)}), 500

# Add new TPS status
@tps_status_controller.route('/tpsstatus', methods=['POST'])
def add_tps_status():
    try:
        data = request.get_json()
        tps_id = data.get('tpsId')
        status = data.get('status')

        # Check if TPS exists
        existing_tps_snapshot = db.reference('/tps').child(tps_id).get()
        if not existing_tps_snapshot:
            return jsonify({'message': 'TPS not found'}), 404

        # Create a new TPS status object
        new_tps_status = {
            'tpsId': tps_id,
            'status': status,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Save the new TPS status to Firebase
        new_tps_status_ref = db.reference('/tpsstatus').push(new_tps_status)
        return jsonify({'message': 'TPS status added successfully', 'tpsStatus': {**new_tps_status, 'id': new_tps_status_ref.key}}), 201
    except Exception as error:
        print('Error adding TPS status:', error)
        return jsonify({'error': str(error)}), 500

# Get TPS status by ID
@tps_status_controller.route('/tpsstatus/<tps_status_id>', methods=['GET'])
def get_tps_status_by_id(tps_status_id):
    try:
        if not tps_status_id or not isinstance(tps_status_id, str):
            return jsonify({'error': 'Invalid TPS status ID'}), 400

        tps_status_snapshot = db.reference(f'/tpsstatus/{tps_status_id}').get()

        if not tps_status_snapshot:
            return jsonify({'message': 'TPS status not found'}), 404

        return jsonify(tps_status_snapshot), 200
    except Exception as error:
        print('Error getting TPS status by ID:', error)
        return jsonify({'error': str(error)}), 500

# Update TPS status by ID
@tps_status_controller.route('/tpsstatus/<tps_status_id>', methods=['PUT'])
def update_tps_status(tps_status_id):
    try:
        data = request.get_json()
        tps_id = data.get('tpsId')
        status = data.get('status')

        # Check if TPS status exists
        tps_status_snapshot = db.reference(f'/tpsstatus/{tps_status_id}').get()
        if not tps_status_snapshot:
            return jsonify({'message': 'TPS status not found'}), 404

        # Update the TPS status
        updated_tps_status = {
            'tpsId': tps_id,
            'status': status,
            'timestamp': datetime.utcnow().isoformat()
        }

        db.reference(f'/tpsstatus/{tps_status_id}').update(updated_tps_status)
        return jsonify({'message': 'TPS status updated successfully'}), 200
    except Exception as error:
        print('Error updating TPS status:', error)
        return jsonify({'error': str(error)}), 500

# Delete TPS status by ID
@tps_status_controller.route('/tpsstatus/<tps_status_id>', methods=['DELETE'])
def delete_tps_status(tps_status_id):
    try:
        # Check if TPS status exists
        tps_status_snapshot = db.reference(f'/tpsstatus/{tps_status_id}').get()
        if not tps_status_snapshot:
            return jsonify({'message': 'TPS status not found'}), 404

        # Delete the TPS status
        db.reference(f'/tpsstatus/{tps_status_id}').delete()
        return jsonify({'message': 'TPS status deleted successfully'}), 200
    except Exception as error:
        print('Error deleting TPS status:', error)
        return jsonify({'error': str(error)}), 500

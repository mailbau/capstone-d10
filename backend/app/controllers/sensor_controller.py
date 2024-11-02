from flask import Blueprint, request, jsonify
from firebase_admin import db
from datetime import datetime

sensor_controller = Blueprint('sensor_controller', __name__)

# Get all sensors
@sensor_controller.route('/sensors', methods=['GET'])
def get_all_sensors():
    try:
        sensors_snapshot = db.reference('/sensors').get()
        sensors = sensors_snapshot or {}  # Return empty dictionary if no sensors found
        return jsonify(sensors), 200
    except Exception as error:
        print('Error getting all sensors:', error)
        return jsonify({'error': str(error)}), 500

# Add a new sensor
@sensor_controller.route('/sensors', methods=['POST'])
def add_sensor():
    try:
        data = request.get_json()
        sensor_name = data.get('sensorName')
        tps_id = data.get('tpsId')

        # Check if sensor already exists for the same TPS
        existing_sensor_snapshot = db.reference('/sensors').order_by_child('tpsId').equal_to(tps_id).get()
        if existing_sensor_snapshot:
            return jsonify({'message': 'Sensor already exists for this TPS'}), 409

        # Create a new sensor object
        new_sensor = {
            'sensorName': sensor_name,
            'tpsId': tps_id,
            'createdAt': datetime.utcnow().isoformat()  # Record creation time
        }

        # Save the new sensor to Firebase
        new_sensor_ref = db.reference('/sensors').push(new_sensor)
        return jsonify({'message': 'Sensor added successfully', 'sensor': {**new_sensor, 'id': new_sensor_ref.key}}), 201
    except Exception as error:
        print('Error adding sensor:', error)
        return jsonify({'error': str(error)}), 500

# Get sensor by ID
@sensor_controller.route('/sensors/<sensor_id>', methods=['GET'])
def get_sensor_by_id(sensor_id):
    try:
        if not sensor_id or not isinstance(sensor_id, str):
            return jsonify({'error': 'Invalid sensor ID'}), 400

        sensor_snapshot = db.reference(f'/sensors/{sensor_id}').get()

        if not sensor_snapshot:
            return jsonify({'message': 'Sensor not found'}), 404

        return jsonify(sensor_snapshot), 200
    except Exception as error:
        print('Error getting sensor by ID:', error)
        return jsonify({'error': str(error)}), 500

# Update sensor by ID
@sensor_controller.route('/sensors/<sensor_id>', methods=['PUT'])
def update_sensor(sensor_id):
    try:
        if not sensor_id or not isinstance(sensor_id, str):
            return jsonify({'error': 'Invalid sensor ID'}), 400

        data = request.get_json()
        sensor_name = data.get('sensorName')
        tps_id = data.get('tpsId')

        # Check if sensor exists
        sensor_snapshot = db.reference(f'/sensors/{sensor_id}').get()
        if not sensor_snapshot:
            return jsonify({'message': 'Sensor not found'}), 404

        # Update sensor data
        updated_sensor = {
            'sensorName': sensor_name,
            'tpsId': tps_id,
            'updatedAt': datetime.utcnow().isoformat()  # Record update time
        }

        db.reference(f'/sensors/{sensor_id}').update(updated_sensor)
        return jsonify({'message': 'Sensor updated successfully', 'updatedSensor': updated_sensor}), 200
    except Exception as error:
        print('Error updating sensor:', error)
        return jsonify({'error': str(error)}), 500

# Delete sensor by ID
@sensor_controller.route('/sensors/<sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    try:
        if not sensor_id or not isinstance(sensor_id, str):
            return jsonify({'error': 'Invalid sensor ID'}), 400

        # Check if sensor exists
        sensor_snapshot = db.reference(f'/sensors/{sensor_id}').get()
        if not sensor_snapshot:
            return jsonify({'message': 'Sensor not found'}), 404

        db.reference(f'/sensors/{sensor_id}').delete()
        return jsonify({'message': 'Sensor deleted successfully'}), 200
    except Exception as error:
        print('Error deleting sensor:', error)
        return jsonify({'error': str(error)}), 500

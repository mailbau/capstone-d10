from flask import Blueprint
from app.controllers.sensor_controller import get_all_sensors, add_sensor, get_sensor_by_id, update_sensor, delete_sensor

# Create a Blueprint for sensor routes
sensor_routes = Blueprint('sensor_routes', __name__)

# Get all sensors
sensor_routes.route('/', methods=['GET'])(get_all_sensors)

# Add sensor
sensor_routes.route('/', methods=['POST'])(add_sensor)

# Get specific sensor by ID
sensor_routes.route('/<string:sensor_id>', methods=['GET'])(get_sensor_by_id)

# Update sensor by ID
sensor_routes.route('/<string:sensor_id>', methods=['PUT'])(update_sensor)

# Delete sensor by ID
sensor_routes.route('/<string:sensor_id>', methods=['DELETE'])(delete_sensor)
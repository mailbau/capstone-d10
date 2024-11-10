from flask import Blueprint
from app.controllers.tps_status_controller import get_all_tps_status, add_tps_status, get_tps_status_by_id, update_tps_status, delete_tps_status, get_dummy_tps_status

# Create a Blueprint for TPS status routes
tps_status_routes = Blueprint('tps_status_routes', __name__)

# Get all TPS statuses
tps_status_routes.route('/', methods=['GET'])(get_all_tps_status)

# Add TPS status
tps_status_routes.route('/', methods=['POST'])(add_tps_status)

# Get specific TPS status by ID
tps_status_routes.route('/<string:tps_status_id>', methods=['GET'])(get_tps_status_by_id)

# Update TPS status by ID
tps_status_routes.route('/<string:tps_status_id>', methods=['PUT'])(update_tps_status)

# Delete TPS status by ID
tps_status_routes.route('/<string:tps_status_id>', methods=['DELETE'])(delete_tps_status)

# Get dummy TPS status
tps_status_routes.route('/dummy', methods=['GET'])(get_dummy_tps_status)
from flask import Blueprint
from app.controllers.tps_controller import get_all_tps, add_tps, get_tps_by_id, update_tps, delete_tps

# Create a Blueprint for TPS routes
tps_routes = Blueprint('tps_routes', __name__)

# Get all TPS locations
tps_routes.route('/', methods=['GET'])(get_all_tps)

# Add TPS location
tps_routes.route('/', methods=['POST'])(add_tps)

# Get specific TPS location by ID
tps_routes.route('/<string:tps_id>', methods=['GET'])(get_tps_by_id)

# Update TPS location by ID
tps_routes.route('/<string:tps_id>', methods=['PUT'])(update_tps)

# Delete TPS location by ID
tps_routes.route('/<string:tps_id>', methods=['DELETE'])(delete_tps)
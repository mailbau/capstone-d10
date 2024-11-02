from flask import Blueprint
from app.controllers.route_controller import get_all_routes, add_route, get_route_by_id, update_route, delete_route

# Create a Blueprint for route routes
route_routes = Blueprint('route_routes', __name__)

# Get all routes
route_routes.route('/', methods=['GET'])(get_all_routes)

# Add route
route_routes.route('/', methods=['POST'])(add_route)

# Get specific route by ID
route_routes.route('/<string:route_id>', methods=['GET'])(get_route_by_id)

# Update route by ID
route_routes.route('/<string:route_id>', methods=['PUT'])(update_route)

# Delete route by ID
route_routes.route('/<string:route_id>', methods=['DELETE'])(delete_route)
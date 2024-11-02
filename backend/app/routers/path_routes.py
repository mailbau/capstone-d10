from flask import Blueprint
from app.controllers.path_controller import get_all_paths, add_path, get_path_by_id, update_path, delete_path

# Create a Blueprint for path routes
path_routes = Blueprint('path_routes', __name__)

# Get all paths
path_routes.route('/', methods=['GET'])(get_all_paths)

# Add path
path_routes.route('/', methods=['POST'])(add_path)

# Get specific path by ID
path_routes.route('/<string:path_id>', methods=['GET'])(get_path_by_id)

# Update path by ID
path_routes.route('/<string:path_id>', methods=['PUT'])(update_path)

# Delete path by ID
path_routes.route('/<string:path_id>', methods=['DELETE'])(delete_path)
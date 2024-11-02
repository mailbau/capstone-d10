from flask import Blueprint
from app.controllers.user_controller import get_all_users, add_user, get_user_by_id, update_user, delete_user

# Create a Blueprint for user routes
user_routes = Blueprint('user_routes', __name__)

# Get all users
user_routes.route('/', methods=['GET'])(get_all_users)

# Add user
user_routes.route('/register', methods=['POST'])(add_user)

# Get specific user by ID
user_routes.route('/<string:user_id>', methods=['GET'])(get_user_by_id)

# Update user by ID
user_routes.route('/<string:user_id>', methods=['PUT'])(update_user)

# Delete user by ID
user_routes.route('/<string:user_id>', methods=['DELETE'])(delete_user)

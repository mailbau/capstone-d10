from flask import Blueprint
from app.controllers.auth_controller import login_user

# Create a Blueprint for auth routes
auth_routes = Blueprint('auth_routes', __name__)

# Login user
auth_routes.route('/login', methods=['POST'])(login_user)


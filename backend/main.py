from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Firebase setup
cred = credentials.Certificate(os.getenv('FIREBASE_ADMIN_KEY'))
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
})

# Check Firebase connection
try:
    db.reference('/').get()
    print("Connected to Firebase")
except Exception as e:
    print("Error connecting to Firebase:", e)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Import Blueprints
from app.routers.user_routes import user_routes
from app.routers.tps_routes import tps_routes
from app.routers.path_routes import path_routes
from app.routers.sensor_routes import sensor_routes
from app.routers.auth_routes import auth_routes
from app.routers.tps_status_routes import tps_status_routes
from app.routers.route_routes import route_routes

# Register Blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(tps_routes, url_prefix='/tps')
app.register_blueprint(path_routes, url_prefix='/path')
app.register_blueprint(sensor_routes, url_prefix='/sensor')
app.register_blueprint(tps_status_routes, url_prefix='/tpsstatus')
app.register_blueprint(route_routes, url_prefix='/route')

# Define port from environment variables or use default
PORT = int(os.getenv('PORT', 8080))

if __name__ == '__main__':
    print("Available endpoints:")
    with app.test_request_context():
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        print("\n".join(routes))
    
    # Start the server
    app.run(host='0.0.0.0', port=PORT, debug=True)

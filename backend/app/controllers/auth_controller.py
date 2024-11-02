from flask import request, jsonify
import jwt
import bcrypt
import os
from firebase_admin import db

# Ensure Firebase and JWT secret configurations are initialized in your Flask app

def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        # Query the Firebase Realtime Database for the user by email
        user_ref = db.reference('/users')
        snapshot = user_ref.order_by_child('user_email').equal_to(email).get()

        if not snapshot:
            return jsonify({"message": "Invalid email or password"}), 401

        # Get user data from the snapshot
        user_id, user_data = list(snapshot.items())[0]

        # Compare the entered password with the hashed password in the database
        is_password_valid = bcrypt.checkpw(password.encode('utf-8'), user_data['user_password'].encode('utf-8'))
        if not is_password_valid:
            return jsonify({"message": "Invalid email or password"}), 401

        # Generate JWT token if password is valid
        token = jwt.encode(
            {"userId": user_id, "email": email},
            os.getenv("JWT_SECRET"),
            algorithm="HS256"
        )
        return jsonify({"token": token})
    except Exception as e:
        print("Error logging in user", e)
        return jsonify({"message": "An error occurred during login", "error": str(e)}), 500
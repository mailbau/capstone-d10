from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import db
import bcrypt
import os
import json

# Ensure Firebase is initialized (use your initialization code)
app = Flask(__name__)

# Get the Firebase database reference
database = db.reference('/users')

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users_snapshot = database.get()
        users = users_snapshot if users_snapshot else {}  # Return empty object if no users
        return jsonify(users), 200
    except Exception as e:
        print('Error getting all users:', e)
        return jsonify({'error': str(e)}), 500

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        if not user_id:
            return jsonify({'error': 'Invalid user ID'}), 400

        user_snapshot = database.child(user_id).get()
        if not user_snapshot:
            return jsonify({'message': 'User not found'}), 404

        return jsonify(user_snapshot), 200
    except Exception as e:
        print('Error getting user by ID:', e)
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_email = data.get('user_email')
        user_password = data.get('user_password')

        # Check if user already exists
        existing_user_snapshot = database.order_by_child('user_email').equal_to(user_email).get()
        if existing_user_snapshot:
            return jsonify({'message': 'User already exists'}), 409

        # Hash the password
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user object
        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'user_email': user_email,
            'user_password': hashed_password.decode('utf-8')
        }

        # Save the user to Firebase
        new_user_ref = database.push(new_user)
        return jsonify({'message': 'User registered successfully', 'user': {**new_user, 'id': new_user_ref.key}}), 201
    except Exception as e:
        print('Error registering user:', e)
        return jsonify({'error': str(e)}), 500

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        if not user_id:
            return jsonify({'error': 'Invalid user ID'}), 400

        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_email = data.get('user_email')
        user_password = data.get('user_password')

        # Check if user exists
        user_snapshot = database.child(user_id).get()
        if not user_snapshot:
            return jsonify({'message': 'User not found'}), 404

        # Prepare the updated user data
        updated_user = {}

        if first_name: updated_user['first_name'] = first_name
        if last_name: updated_user['last_name'] = last_name
        if user_email: updated_user['user_email'] = user_email
        if user_password:
            updated_user['user_password'] = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Update user data only with fields that are defined
        database.child(user_id).update(updated_user)
        return jsonify({'message': 'User updated successfully', 'updatedUser': updated_user}), 200
    except Exception as e:
        print('Error updating user:', e)
        return jsonify({'error': str(e)}), 500

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if not user_id:
            return jsonify({'error': 'Invalid user ID'}), 400

        # Check if user exists
        user_snapshot = database.child(user_id).get()
        if not user_snapshot:
            return jsonify({'message': 'User not found'}), 404

        database.child(user_id).delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        print('Error deleting user:', e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

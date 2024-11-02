from flask import Flask
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Parse the Firebase admin key from the environment variable
service_account_info = json.loads(os.getenv("FIREBASE_ADMIN_KEY"))

# Check if Firebase is already initialized to prevent reinitialization errors
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
    })

# Expose the database reference for other modules to use
database = db

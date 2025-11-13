"""
Authentication routes for admin login
"""

from flask import Blueprint, request, jsonify
from utils.auth import generate_token, verify_admin, create_admin_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    Admin login endpoint
    POST /api/auth/login
    Body: { "username": "admin", "password": "password" }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Verify credentials
        if verify_admin(username, password):
            token = generate_token(username)
            return jsonify({
                "message": "Login successful",
                "token": token
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({"error": "Failed to login"}), 500


@auth_bp.route('/auth/setup', methods=['POST'])
def setup_admin():
    """
    One-time admin setup (should be disabled in production)
    POST /api/auth/setup
    Body: { "username": "admin", "password": "password", "setup_key": "your-setup-key" }
    """
    try:
        data = request.get_json()

        # Check setup key (add SETUP_KEY to your .env)
        import os
        if data.get('setup_key') != os.getenv('SETUP_KEY'):
            return jsonify({"error": "Invalid setup key"}), 403

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400

        create_admin_user(username, password)

        return jsonify({"message": "Admin user created successfully"}), 201

    except Exception as e:
        print(f"Error in setup_admin: {e}")
        return jsonify({"error": "Failed to create admin user"}), 500
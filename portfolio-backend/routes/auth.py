"""
Authentication routes for admin access
"""

from flask import Blueprint, request, jsonify
from utils.auth import (
    verify_admin,
    generate_token,
    admin_required,
    create_admin_user
)
from utils.validators import LoginSchema, validate_request
from config.config import Config

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    Admin login endpoint
    POST /api/auth/login
    Body: {
        "username": "admin",
        "password": "password"
    }
    Returns: {
        "token": "jwt-token",
        "username": "admin"
    }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Verify credentials
        if verify_admin(username, password):
            # Generate JWT token
            token = generate_token(username)
            if token:
                return jsonify({
                    "message": "Login successful",
                    "token": token,
                    "username": username
                }), 200
            else:
                return jsonify({"error": "Failed to generate token"}), 500
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({"error": "Login failed"}), 500


@auth_bp.route('/auth/setup', methods=['POST'])
def setup_admin():
    """
    Create first admin user (protected by setup key)
    POST /api/auth/setup
    Body: {
        "username": "admin",
        "password": "securepassword",
        "setup_key": "your-setup-key"
    }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        setup_key = data.get('setup_key', '')

        # Validate setup key
        if setup_key != Config.SETUP_KEY:
            return jsonify({"error": "Invalid setup key"}), 403

        # Validate input
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400

        # Create admin user
        success = create_admin_user(username, password)
        if success:
            return jsonify({
                "message": "Admin user created successfully",
                "username": username
            }), 201
        else:
            return jsonify({"error": "Failed to create admin user or user already exists"}), 400

    except Exception as e:
        print(f"Error in setup_admin: {e}")
        return jsonify({"error": "Admin setup failed"}), 500


@auth_bp.route('/auth/verify', methods=['GET'])
@admin_required
def verify_token(username):
    """
    Verify if token is valid
    GET /api/auth/verify
    Headers: Authorization: Bearer <token>
    """
    return jsonify({
        "valid": True,
        "username": username
    }), 200


@auth_bp.route('/auth/profile', methods=['GET'])
@admin_required
def get_profile(username):
    """
    Get admin profile
    GET /api/auth/profile
    Headers: Authorization: Bearer <token>
    """
    try:
        from utils.database import admin_collection

        admin_user = admin_collection.find_one({'username': username})
        if not admin_user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "username": admin_user['username'],
            "created_at": admin_user['created_at'].isoformat(),
            "is_active": admin_user.get('is_active', True)
        }), 200

    except Exception as e:
        print(f"Error in get_profile: {e}")
        return jsonify({"error": "Failed to fetch profile"}), 500
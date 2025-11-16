"""
Authentication utilities for admin access
"""

import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from utils.database_optimized import admin_collection
import bcrypt

# Get secret key from config
def get_secret_key():
    from config.config import Config
    return Config.SECRET_KEY

def generate_token(username, expires_in=86400):
    """
    Generate JWT token for admin user
    Args:
        username (str): Admin username
        expires_in (int): Token expiration time in seconds (default: 24 hours)
    Returns:
        str: JWT token
    """
    try:
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, get_secret_key(), algorithm='HS256')
        return token
    except Exception as e:
        print(f"Error generating token: {e}")
        return None

def verify_token(token):
    """
    Verify JWT token
    Args:
        token (str): JWT token to verify
    Returns:
        dict: Decoded token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None

def hash_password(password):
    """
    Hash password using bcrypt
    Args:
        password (str): Plain text password
    Returns:
        str: Hashed password
    """
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except Exception as e:
        print(f"Error hashing password: {e}")
        return None

def verify_password(password, hashed):
    """
    Verify password against hash
    Args:
        password (str): Plain text password
        hashed (str): Hashed password
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

def verify_admin(username, password):
    """
    Verify admin credentials
    Args:
        username (str): Admin username
        password (str): Admin password
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    try:
        if not admin_collection:
            print("Admin collection not available")
            return False

        admin_user = admin_collection.find_one({'username': username})
        if not admin_user:
            return False

        return verify_password(password, admin_user['password_hash'])
    except Exception as e:
        print(f"Error verifying admin: {e}")
        return False

def create_admin_user(username, password):
    """
    Create a new admin user
    Args:
        username (str): Admin username
        password (str): Admin password
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not admin_collection:
            print("Admin collection not available")
            return False

        # Check if user already exists
        if admin_collection.find_one({'username': username}):
            print(f"Admin user '{username}' already exists")
            return False

        # Hash password
        hashed = hash_password(password)
        if not hashed:
            print("Failed to hash password")
            return False

        # Create admin document
        admin_doc = {
            'username': username,
            'password_hash': hashed,
            'created_at': datetime.utcnow(),
            'is_active': True
        }

        # Insert into database
        result = admin_collection.insert_one(admin_doc)
        return result.inserted_id is not None
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False

def admin_required(f):
    """
    Decorator to require admin authentication
    Usage: @admin_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Get token from Authorization header
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return jsonify({"error": "Missing or invalid token"}), 401

            token = auth_header.replace('Bearer ', '', 1)

            # Verify token
            payload = verify_token(token)
            if not payload:
                return jsonify({"error": "Invalid or expired token"}), 401

            # Pass username to the decorated function
            return f(payload.get('username'), *args, **kwargs)
        except Exception as e:
            print(f"Error in admin_required decorator: {e}")
            return jsonify({"error": "Authentication failed"}), 401

    return decorated_function
"""
Enhanced Flask application with security, logging, and performance improvements
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.config import Config
from utils.logger import setup_logging, RequestLogger
from utils.database_optimized import db_manager
import logging

# Import routes
from routes.contact import contact_bp
from routes.projects import project_bp
from routes.skills import skill_bp
from routes.analytics import analytics_bp
from routes.auth import auth_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Setup logging
logger = setup_logging(app)
request_logger = RequestLogger(app)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per hour", "50 per minute"],
    storage_uri="memory://"  # Use Redis in production: "redis://localhost:6379"
)

# Configure CORS with security headers
CORS(app, resources={
    r"/api/*": {
        "origins": [Config.FRONTEND_URL],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True,
        "max_age": 3600
    }
})


# Request/Response middleware
@app.before_request
def before_request():
    """Log incoming requests and add security headers"""
    request_logger.log_request()

    # Add request ID for tracking
    import uuid
    request.request_id = str(uuid.uuid4())

    # Log request details
    logger.info(f"Request ID: {request.request_id} - {request.method} {request.path}")


@app.after_request
def after_request(response):
    """Add security headers and log response"""
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    # Log response
    request_logger.log_response(response)

    return response


# Health check endpoint
@app.route('/health', methods=['GET'])
@limiter.exempt
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db_status = "healthy" if db_manager.client else "unhealthy"

        return jsonify({
            "status": "healthy",
            "database": db_status,
            "message": "Portfolio API is running",
            "version": "1.0.0"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503


# Root endpoint
@app.route('/', methods=['GET'])
@limiter.limit("10 per minute")
def root():
    """API information endpoint"""
    return jsonify({
        "message": "Portfolio API",
        "version": "1.0.0",
        "documentation": "/api/docs",
        "health": "/health",
        "endpoints": {
            "auth": "/api/auth",
            "contact": "/api/contact",
            "projects": "/api/projects",
            "skills": "/api/skills",
            "analytics": "/api/analytics"
        }
    }), 200


# Register blueprints with enhanced error handling
try:
    # Authentication routes
    app.register_blueprint(auth_bp, url_prefix='/api')
    logger.info("Auth routes registered")


    # Contact routes with mail dependency
    @app.route('/api/contact', methods=['POST'])
    @limiter.limit("5 per hour")  # Strict limit for contact form
    def handle_contact():
        from routes.contact import submit_contact
        from utils.validators import validate_request, ContactSchema
        from utils.validators import sanitize_input

        # Validate and sanitize input
        try:
            from marshmallow import ValidationError
            schema = ContactSchema()
            data = request.get_json()
            validated_data = schema.load(data)

            # Additional sanitization
            validated_data['name'] = sanitize_input(validated_data['name'])
            validated_data['message'] = sanitize_input(validated_data['message'])

            request.validated_data = validated_data
            return submit_contact(mail)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400


    @app.route('/api/contacts', methods=['GET'])
    def handle_get_contacts():
        from routes.contact import get_contacts
        from utils.auth import admin_required

        @admin_required
        def get_contacts_admin(user_id):
            return get_contacts()

        return get_contacts_admin()


    @app.route('/api/contacts/<contact_id>/read', methods=['PATCH'])
    def handle_mark_read(contact_id):
        from routes.contact import mark_contact_read
        from utils.auth import admin_required

        @admin_required
        def mark_read_admin(user_id):
            return mark_contact_read(contact_id)

        return mark_read_admin()


    # Other blueprints
    app.register_blueprint(project_bp, url_prefix='/api')
    app.register_blueprint(skill_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')

    logger.info("All routes registered successfully")

except Exception as e:
    logger.error(f"Failed to register routes: {e}")
    raise


# Error handlers with logging
@app.errorhandler(400)
def bad_request(error):
    logger.warning(f"Bad request: {error}")
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(401)
def unauthorized(error):
    logger.warning(f"Unauthorized access attempt: {error}")
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    logger.warning(f"Forbidden access: {error}")
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    logger.info(f"Endpoint not found: {request.path}")
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(429)
def rate_limit_exceeded(error):
    logger.warning(f"Rate limit exceeded for {get_remote_address()}")
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "request_id": getattr(request, 'request_id', 'unknown')
    }), 500


# Cleanup on app shutdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    """Clean up database connections"""
    if exception:
        logger.error(f"App context teardown with exception: {exception}")


# Create admin setup CLI command
@app.cli.command('create-admin')
def create_admin_command():
    """Create an admin user from command line"""
    import getpass
    from utils.auth import create_admin_user

    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords don't match!")
        return

    if len(password) < 8:
        print("Password must be at least 8 characters!")
        return

    try:
        create_admin_user(username, password)
        print(f"Admin user '{username}' created successfully!")
    except Exception as e:
        print(f"Failed to create admin: {e}")


# Create database indexes CLI command
@app.cli.command('init-db')
def init_database():
    """Initialize database with indexes"""
    try:
        db_manager.create_indexes()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize database: {e}")


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 Starting Enhanced Portfolio Backend API")
    print("=" * 50)
    print(f"Environment: {Config.FLASK_ENV}")
    print(f"Frontend URL: {Config.FRONTEND_URL}")
    print(f"Logging: Enabled")
    print(f"Rate Limiting: Enabled")
    print(f"Security Headers: Enabled")
    print("=" * 50 + "\n")

    # Development server
    if Config.FLASK_ENV == 'development':
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    else:
        # Production: Use Gunicorn instead
        print("Use Gunicorn for production deployment:")
        print("gunicorn --bind 0.0.0.0:5000 --workers 4 app:app")
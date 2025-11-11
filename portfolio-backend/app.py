from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from config.config import Config
from routes.contact import contact_bp
from routes.projects import project_bp
from routes.skills import skill_bp
from routes.analytics import analytics_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Mail
mail = Mail(app)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": [Config.FRONTEND_URL],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type"]
    }
})


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Portfolio API is running"
    }), 200


# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "Portfolio API",
        "version": "1.0.0",
        "endpoints": {
            "contact": "/api/contact",
            "projects": "/api/projects",
            "skills": "/api/skills",
            "analytics": "/api/analytics"
        }
    }), 200


# Register blueprints with API prefix
# Note: contact_bp needs special handling for mail dependency
@app.route('/api/contact', methods=['POST'])
def handle_contact():
    from routes.contact import submit_contact
    return submit_contact(mail)


@app.route('/api/contacts', methods=['GET'])
def handle_get_contacts():
    from routes.contact import get_contacts
    return get_contacts()


@app.route('/api/contacts/<contact_id>/read', methods=['PATCH'])
def handle_mark_read(contact_id):
    from routes.contact import mark_contact_read
    return mark_contact_read(contact_id)


app.register_blueprint(project_bp, url_prefix='/api')
app.register_blueprint(skill_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 Starting Portfolio Backend API")
    print("=" * 50)
    print(f"Environment: {Config.FLASK_ENV}")
    print(f"Frontend URL: {Config.FRONTEND_URL}")
    print("=" * 50 + "\n")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(Config.FLASK_ENV == 'development')
    )
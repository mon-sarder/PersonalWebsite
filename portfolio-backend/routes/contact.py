from flask import Blueprint, request, jsonify
from models.models import ContactModel
from utils.database import contacts_collection
from utils.email import send_contact_notification, send_confirmation_email

contact_bp = Blueprint('contact', __name__)


@contact_bp.route('/contact', methods=['POST'])
def submit_contact(mail):
    """
    Handle contact form submission
    POST /api/contact
    Body: { "name": "John", "email": "john@example.com", "message": "Hello!" }
    """
    try:
        data = request.get_json()

        # Validate required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400

        # Basic email validation
        if '@' not in email:
            return jsonify({"error": "Invalid email address"}), 400

        # Create contact document
        contact_doc = ContactModel.create(name, email, message)

        # Save to database
        result = contacts_collection.insert_one(contact_doc)

        # Send email notifications
        notification_sent = send_contact_notification(mail, name, email, message)
        confirmation_sent = send_confirmation_email(mail, email, name)

        return jsonify({
            "message": "Contact form submitted successfully",
            "id": str(result.inserted_id),
            "email_sent": notification_sent
        }), 201

    except Exception as e:
        print(f"Error in submit_contact: {e}")
        return jsonify({"error": "Failed to submit contact form"}), 500


@contact_bp.route('/contacts', methods=['GET'])
def get_contacts():
    """
    Get all contact submissions (for admin dashboard)
    GET /api/contacts
    """
    try:
        contacts = list(contacts_collection.find().sort("created_at", -1))
        return jsonify({
            "contacts": [ContactModel.serialize(c) for c in contacts]
        }), 200
    except Exception as e:
        print(f"Error in get_contacts: {e}")
        return jsonify({"error": "Failed to fetch contacts"}), 500


@contact_bp.route('/contacts/<contact_id>/read', methods=['PATCH'])
def mark_contact_read(contact_id):
    """
    Mark a contact as read
    PATCH /api/contacts/<id>/read
    """
    try:
        from bson import ObjectId
        result = contacts_collection.update_one(
            {"_id": ObjectId(contact_id)},
            {"$set": {"read": True}}
        )

        if result.modified_count:
            return jsonify({"message": "Contact marked as read"}), 200
        else:
            return jsonify({"error": "Contact not found"}), 404

    except Exception as e:
        print(f"Error in mark_contact_read: {e}")
        return jsonify({"error": "Failed to update contact"}), 500
"""
Request validation schemas using marshmallow
"""

from marshmallow import Schema, fields, validate, ValidationError
import re

# Custom validators
def validate_email(email):
    """Custom email validator"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email address")
    return True

class ContactSchema(Schema):
    """Validation schema for contact form"""
    name = fields.Str(required=True, validate=[
        validate.Length(min=2, max=100),
        validate.Regexp(r'^[a-zA-Z\s]+$', error='Name must contain only letters and spaces')
    ])
    email = fields.Email(required=True, validate=validate_email)
    message = fields.Str(required=True, validate=[
        validate.Length(min=10, max=1000)
    ])

class ProjectSchema(Schema):
    """Validation schema for projects"""
    title = fields.Str(required=True, validate=[
        validate.Length(min=3, max=100)
    ])
    description = fields.Str(required=True, validate=[
        validate.Length(min=10, max=500)
    ])
    tech_stack = fields.List(fields.Str(), required=True, validate=[
        validate.Length(min=1, max=10)
    ])
    github_link = fields.Url(required=False, allow_none=True)
    live_link = fields.Url(required=False, allow_none=True)
    image_url = fields.Url(required=False, allow_none=True)
    order = fields.Int(required=False, validate=[
        validate.Range(min=0, max=999)
    ])

class SkillSchema(Schema):
    """Validation schema for skills"""
    name = fields.Str(required=True, validate=[
        validate.Length(min=1, max=50)
    ])
    category = fields.Str(required=True, validate=[
        validate.Length(min=1, max=50)
    ])
    proficiency = fields.Str(required=True, validate=[
        validate.OneOf(["Beginner", "Intermediate", "Advanced", "Expert"])
    ])

class LoginSchema(Schema):
    """Validation schema for login"""
    username = fields.Str(required=True, validate=[
        validate.Length(min=3, max=50)
    ])
    password = fields.Str(required=True, validate=[
        validate.Length(min=8, max=100)
    ])

def validate_request(schema_class):
    """Decorator to validate request data"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            from flask import request, jsonify
            schema = schema_class()
            try:
                data = request.get_json()
                validated_data = schema.load(data)
                request.validated_data = validated_data
                return f(*args, **kwargs)
            except ValidationError as err:
                return jsonify({"errors": err.messages}), 400
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    import html
    if text:
        # Remove HTML tags and escape special characters
        text = re.sub(r'<[^>]*>', '', str(text))
        text = html.escape(text)
    return text
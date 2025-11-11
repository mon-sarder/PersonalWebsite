from flask import Blueprint, request, jsonify
from bson import ObjectId
from models.models import ProjectModel
from utils.database import projects_collection

project_bp = Blueprint('project', __name__)


@project_bp.route('/projects', methods=['GET'])
def get_projects():
    """
    Get all projects
    GET /api/projects
    """
    try:
        projects = list(projects_collection.find().sort("order", 1))
        return jsonify({
            "projects": [ProjectModel.serialize(p) for p in projects]
        }), 200
    except Exception as e:
        print(f"Error in get_projects: {e}")
        return jsonify({"error": "Failed to fetch projects"}), 500


@project_bp.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    """
    Get a single project by ID
    GET /api/projects/<id>
    """
    try:
        project = projects_collection.find_one({"_id": ObjectId(project_id)})

        if not project:
            return jsonify({"error": "Project not found"}), 404

        return jsonify(ProjectModel.serialize(project)), 200
    except Exception as e:
        print(f"Error in get_project: {e}")
        return jsonify({"error": "Failed to fetch project"}), 500


@project_bp.route('/projects', methods=['POST'])
def create_project():
    """
    Create a new project
    POST /api/projects
    Body: {
        "title": "My Project",
        "description": "Description",
        "tech_stack": ["React", "Python", "MongoDB"],
        "github_link": "https://github.com/...",
        "live_link": "https://...",
        "image_url": "https://..."
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        tech_stack = data.get('tech_stack', [])

        if not title or not description:
            return jsonify({"error": "Title and description are required"}), 400

        # Create project document
        project_doc = ProjectModel.create(
            title=title,
            description=description,
            tech_stack=tech_stack,
            github_link=data.get('github_link'),
            live_link=data.get('live_link'),
            image_url=data.get('image_url')
        )

        # Save to database
        result = projects_collection.insert_one(project_doc)

        return jsonify({
            "message": "Project created successfully",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:
        print(f"Error in create_project: {e}")
        return jsonify({"error": "Failed to create project"}), 500


@project_bp.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """
    Update an existing project
    PUT /api/projects/<id>
    """
    try:
        data = request.get_json()

        # Build update document (only include fields that are provided)
        update_fields = {}
        if 'title' in data:
            update_fields['title'] = data['title']
        if 'description' in data:
            update_fields['description'] = data['description']
        if 'tech_stack' in data:
            update_fields['tech_stack'] = data['tech_stack']
        if 'github_link' in data:
            update_fields['github_link'] = data['github_link']
        if 'live_link' in data:
            update_fields['live_link'] = data['live_link']
        if 'image_url' in data:
            update_fields['image_url'] = data['image_url']
        if 'order' in data:
            update_fields['order'] = data['order']

        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400

        result = projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": update_fields}
        )

        if result.matched_count:
            return jsonify({"message": "Project updated successfully"}), 200
        else:
            return jsonify({"error": "Project not found"}), 404

    except Exception as e:
        print(f"Error in update_project: {e}")
        return jsonify({"error": "Failed to update project"}), 500


@project_bp.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """
    Delete a project
    DELETE /api/projects/<id>
    """
    try:
        result = projects_collection.delete_one({"_id": ObjectId(project_id)})

        if result.deleted_count:
            return jsonify({"message": "Project deleted successfully"}), 200
        else:
            return jsonify({"error": "Project not found"}), 404

    except Exception as e:
        print(f"Error in delete_project: {e}")
        return jsonify({"error": "Failed to delete project"}), 500
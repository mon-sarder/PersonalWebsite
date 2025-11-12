from flask import Blueprint, request, jsonify
from bson import ObjectId
from models.models import SkillModel
from utils.database import skills_collection

skill_bp = Blueprint('skill', __name__)


@skill_bp.route('/skills', methods=['GET'])
def get_skills():
    """
    Get all skills, optionally grouped by category
    GET /api/skills?grouped=true
    """
    try:
        grouped = request.args.get('grouped', 'false').lower() == 'true'

        skills = list(skills_collection.find())
        serialized_skills = [SkillModel.serialize(s) for s in skills]

        if grouped:
            # Group skills by category
            grouped_skills = {}
            for skill in serialized_skills:
                category = skill['category']
                if category not in grouped_skills:
                    grouped_skills[category] = []
                grouped_skills[category].append(skill)

            return jsonify({"skills": grouped_skills}), 200
        else:
            return jsonify({"skills": serialized_skills}), 200

    except Exception as e:
        print(f"Error in get_skills: {e}")
        return jsonify({"error": "Failed to fetch skills"}), 500


@skill_bp.route('/skills/<skill_id>', methods=['GET'])
def get_skill(skill_id):
    """
    Get a single skill by ID
    GET /api/skills/<id>
    """
    try:
        skill = skills_collection.find_one({"_id": ObjectId(skill_id)})

        if not skill:
            return jsonify({"error": "Skill not found"}), 404

        return jsonify(SkillModel.serialize(skill)), 200
    except Exception as e:
        print(f"Error in get_skill: {e}")
        return jsonify({"error": "Failed to fetch skill"}), 500


@skill_bp.route('/skills', methods=['POST'])
def create_skill():
    """
    Create a new skill
    POST /api/skills
    Body: {
        "name": "React",
        "category": "Frontend",
        "proficiency": "Advanced"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        name = data.get('name', '').strip()
        category = data.get('category', '').strip()
        proficiency = data.get('proficiency', '').strip()

        if not name or not category or not proficiency:
            return jsonify({"error": "Name, category, and proficiency are required"}), 400

        # Validate proficiency level
        valid_proficiencies = ["Beginner", "Intermediate", "Advanced", "Expert"]
        if proficiency not in valid_proficiencies:
            return jsonify({
                "error": f"Proficiency must be one of: {', '.join(valid_proficiencies)}"
            }), 400

        # Create skill document
        skill_doc = SkillModel.create(name, category, proficiency)

        # Save to database
        result = skills_collection.insert_one(skill_doc)

        return jsonify({
            "message": "Skill created successfully",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:
        print(f"Error in create_skill: {e}")
        return jsonify({"error": "Failed to create skill"}), 500


@skill_bp.route('/skills/<skill_id>', methods=['PUT'])
def update_skill(skill_id):
    """
    Update an existing skill
    PUT /api/skills/<id>
    """
    try:
        data = request.get_json()

        # Build update document
        update_fields = {}
        if 'name' in data:
            update_fields['name'] = data['name']
        if 'category' in data:
            update_fields['category'] = data['category']
        if 'proficiency' in data:
            proficiency = data['proficiency']
            valid_proficiencies = ["Beginner", "Intermediate", "Advanced", "Expert"]
            if proficiency not in valid_proficiencies:
                return jsonify({
                    "error": f"Proficiency must be one of: {', '.join(valid_proficiencies)}"
                }), 400
            update_fields['proficiency'] = proficiency

        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400

        result = skills_collection.update_one(
            {"_id": ObjectId(skill_id)},
            {"$set": update_fields}
        )

        if result.matched_count:
            return jsonify({"message": "Skill updated successfully"}), 200
        else:
            return jsonify({"error": "Skill not found"}), 404

    except Exception as e:
        print(f"Error in update_skill: {e}")
        return jsonify({"error": "Failed to update skill"}), 500


@skill_bp.route('/skills/<skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    """
    Delete a skill
    DELETE /api/skills/<id>
    """
    try:
        result = skills_collection.delete_one({"_id": ObjectId(skill_id)})

        if result.deleted_count:
            return jsonify({"message": "Skill deleted successfully"}), 200
        else:
            return jsonify({"error": "Skill not found"}), 404

    except Exception as e:
        print(f"Error in delete_skill: {e}")
        return jsonify({"error": "Failed to delete skill"}), 500


@skill_bp.route('/skills/batch', methods=['POST'])
def create_skills_batch():
    """
    Create multiple skills at once
    POST /api/skills/batch
    Body: {
        "skills": [
            {"name": "React", "category": "Frontend", "proficiency": "Advanced"},
            {"name": "Python", "category": "Backend", "proficiency": "Expert"}
        ]
    }
    """
    try:
        data = request.get_json()
        skills_data = data.get('skills', [])

        if not skills_data:
            return jsonify({"error": "No skills provided"}), 400

        # Create skill documents
        skill_docs = []
        for skill in skills_data:
            skill_doc = SkillModel.create(
                skill.get('name'),
                skill.get('category'),
                skill.get('proficiency')
            )
            skill_docs.append(skill_doc)

        # Insert all at once
        result = skills_collection.insert_many(skill_docs)

        return jsonify({
            "message": f"Successfully created {len(result.inserted_ids)} skills",
            "count": len(result.inserted_ids)
        }), 201

    except Exception as e:
        print(f"Error in create_skills_batch: {e}")
        return jsonify({"error": "Failed to create skills"}), 500
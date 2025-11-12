# models/models.py
from datetime import datetime
from bson import ObjectId


class ContactModel:
    @staticmethod
    def create(name, email, message):
        return {
            "name": name,
            "email": email,
            "message": message,
            "read": False,
            "created_at": datetime.utcnow()
        }

    @staticmethod
    def serialize(contact):
        return {
            "id": str(contact["_id"]),
            "name": contact["name"],
            "email": contact["email"],
            "message": contact["message"],
            "read": contact.get("read", False),
            "created_at": contact["created_at"].isoformat()
        }


class ProjectModel:
    @staticmethod
    def create(title, description, tech_stack, github_link=None, live_link=None, image_url=None):
        return {
            "title": title,
            "description": description,
            "tech_stack": tech_stack,
            "github_link": github_link,
            "live_link": live_link,
            "image_url": image_url,
            "created_at": datetime.utcnow(),
            "order": 999
        }

    @staticmethod
    def serialize(project):
        return {
            "id": str(project["_id"]),
            "title": project["title"],
            "description": project["description"],
            "tech_stack": project["tech_stack"],
            "github_link": project.get("github_link"),
            "live_link": project.get("live_link"),
            "image_url": project.get("image_url"),
            "order": project.get("order", 999)
        }


class SkillModel:
    @staticmethod
    def create(name, category, proficiency):
        return {
            "name": name,
            "category": category,
            "proficiency": proficiency,
            "created_at": datetime.utcnow()
        }

    @staticmethod
    def serialize(skill):
        return {
            "id": str(skill["_id"]),
            "name": skill["name"],
            "category": skill["category"],
            "proficiency": skill["proficiency"]
        }


class AnalyticsModel:
    @staticmethod
    def create_page_view(page, referrer=None, user_agent=None):
        return {
            "type": "page_view",
            "page": page,
            "referrer": referrer,
            "user_agent": user_agent,
            "timestamp": datetime.utcnow()
        }

    @staticmethod
    def create_project_click(project_id, project_title):
        return {
            "type": "project_click",
            "project_id": project_id,
            "project_title": project_title,
            "timestamp": datetime.utcnow()
        }

    @staticmethod
    def serialize(event):
        return {
            "id": str(event["_id"]),
            "type": event["type"],
            "timestamp": event["timestamp"].isoformat(),
            **{k: v for k, v in event.items() if k not in ["_id", "type", "timestamp"]}
        }
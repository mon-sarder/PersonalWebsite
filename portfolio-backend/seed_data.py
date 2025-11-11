"""
Seed script to populate the database with sample data for testing
Run this after setting up your MongoDB connection
"""

from utils.database import projects_collection, skills_collection
from models.models import ProjectModel, SkillModel


def seed_projects():
    """Add sample projects"""
    print("Seeding projects...")

    sample_projects = [
        {
            "title": "E-commerce Website",
            "description": "Full-stack e-commerce platform with user authentication, product catalog, shopping cart, and payment integration.",
            "tech_stack": ["React", "Node.js", "MongoDB", "Stripe"],
            "github_link": "https://github.com/yourusername/ecommerce",
            "live_link": "https://myecommerce.com",
            "image_url": None,
            "order": 1
        },
        {
            "title": "Weather Dashboard",
            "description": "Real-time weather application using OpenWeather API with location search and 5-day forecasts.",
            "tech_stack": ["JavaScript", "HTML/CSS", "OpenWeather API"],
            "github_link": "https://github.com/yourusername/weather-app",
            "live_link": "https://myweather.com",
            "image_url": None,
            "order": 2
        },
        {
            "title": "Task Management System",
            "description": "Collaborative task management tool with drag-and-drop functionality and team collaboration features.",
            "tech_stack": ["React", "Python", "Flask", "PostgreSQL"],
            "github_link": "https://github.com/yourusername/task-manager",
            "live_link": None,
            "image_url": None,
            "order": 3
        }
    ]

    for project_data in sample_projects:
        project_doc = ProjectModel.create(
            title=project_data["title"],
            description=project_data["description"],
            tech_stack=project_data["tech_stack"],
            github_link=project_data.get("github_link"),
            live_link=project_data.get("live_link"),
            image_url=project_data.get("image_url")
        )
        project_doc["order"] = project_data["order"]
        projects_collection.insert_one(project_doc)

    print(f"✓ Added {len(sample_projects)} sample projects")


def seed_skills():
    """Add sample skills"""
    print("Seeding skills...")

    sample_skills = [
        # Frontend
        {"name": "React", "category": "Frontend", "proficiency": "Advanced"},
        {"name": "JavaScript", "category": "Frontend", "proficiency": "Advanced"},
        {"name": "HTML/CSS", "category": "Frontend", "proficiency": "Expert"},
        {"name": "TypeScript", "category": "Frontend", "proficiency": "Intermediate"},
        {"name": "Tailwind CSS", "category": "Frontend", "proficiency": "Advanced"},

        # Backend
        {"name": "Python", "category": "Backend", "proficiency": "Advanced"},
        {"name": "Flask", "category": "Backend", "proficiency": "Advanced"},
        {"name": "Node.js", "category": "Backend", "proficiency": "Intermediate"},
        {"name": "Java", "category": "Backend", "proficiency": "Intermediate"},
        {"name": "REST APIs", "category": "Backend", "proficiency": "Advanced"},

        # Database
        {"name": "MongoDB", "category": "Database", "proficiency": "Advanced"},
        {"name": "PostgreSQL", "category": "Database", "proficiency": "Intermediate"},
        {"name": "MySQL", "category": "Database", "proficiency": "Intermediate"},

        # Tools & Others
        {"name": "Git", "category": "Tools", "proficiency": "Advanced"},
        {"name": "Docker", "category": "Tools", "proficiency": "Intermediate"},
        {"name": "Linux", "category": "Tools", "proficiency": "Intermediate"},
        {"name": "AWS", "category": "Cloud", "proficiency": "Beginner"},
    ]

    skill_docs = []
    for skill_data in sample_skills:
        skill_doc = SkillModel.create(
            name=skill_data["name"],
            category=skill_data["category"],
            proficiency=skill_data["proficiency"]
        )
        skill_docs.append(skill_doc)

    skills_collection.insert_many(skill_docs)
    print(f"✓ Added {len(sample_skills)} sample skills")


def clear_collections():
    """Clear all collections (use with caution!)"""
    print("Clearing all collections...")
    projects_collection.delete_many({})
    skills_collection.delete_many({})
    print("✓ All collections cleared")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Database Seeding Script")
    print("=" * 50 + "\n")

    response = input("This will add sample data to your database. Continue? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        # Optional: clear existing data first
        clear_response = input("Clear existing data first? (yes/no): ")
        if clear_response.lower() in ['yes', 'y']:
            clear_collections()

        seed_projects()
        seed_skills()

        print("\n" + "=" * 50)
        print("✓ Database seeding completed!")
        print("=" * 50 + "\n")
    else:
        print("Seeding cancelled.")
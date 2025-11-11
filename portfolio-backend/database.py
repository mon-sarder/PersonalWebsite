from pymongo import MongoClient
from config.config import Config

def get_database():
    """
    Create and return MongoDB database connection
    """
    try:
        client = MongoClient(Config.MONGODB_URI)
        # Test the connection
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB!")
        return client['portfolio']
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        return None

# Initialize database connection
db = get_database()

# Collections
contacts_collection = db['contacts'] if db else None
projects_collection = db['projects'] if db else None
skills_collection = db['skills'] if db else None
analytics_collection = db['analytics'] if db else None
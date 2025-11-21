"""
Database optimization utilities
"""

from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from config.config import Config
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Enhanced database manager with connection pooling and indexes"""

    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        """Create MongoDB connection with connection pooling"""
        try:
            # Connection with pooling parameters
            self.client = MongoClient(
                Config.MONGODB_URI,
                maxPoolSize=50,
                minPoolSize=10,
                maxIdleTimeMS=30000,
                waitQueueTimeoutMS=5000,
                serverSelectionTimeoutMS=5000,
                retryWrites=True,
                w='majority'
            )

            # Test connection
            self.client.admin.command('ping')
            self.db = self.client['portfolio']

            logger.info("✓ Successfully connected to MongoDB with connection pooling")

            # Create indexes
            self.create_indexes()

            return self.db

        except Exception as e:
            logger.error(f"✗ Error connecting to MongoDB: {e}")
            return None

    def create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Projects indexes
            self.db.projects.create_index([('order', ASCENDING)])
            self.db.projects.create_index([('created_at', DESCENDING)])
            self.db.projects.create_index([('title', TEXT), ('description', TEXT)])

            # Skills indexes
            self.db.skills.create_index([('category', ASCENDING)])
            self.db.skills.create_index([('proficiency', ASCENDING)])
            self.db.skills.create_index([('name', ASCENDING)], unique=True)

            # Contacts indexes
            self.db.contacts.create_index([('created_at', DESCENDING)])
            self.db.contacts.create_index([('read', ASCENDING)])
            self.db.contacts.create_index([('email', ASCENDING)])

            # Analytics indexes
            self.db.analytics.create_index([('timestamp', DESCENDING)])
            self.db.analytics.create_index([('type', ASCENDING)])
            self.db.analytics.create_index([
                ('type', ASCENDING),
                ('timestamp', DESCENDING)
            ])

            # Admin indexes
            self.db.admins.create_index([('username', ASCENDING)], unique=True)

            logger.info("✓ Database indexes created successfully")

        except Exception as e:
            logger.error(f"Error creating indexes: {e}")

    def get_collection(self, name):
        """Get a collection with error handling"""
        if self.db is None:
            self.connect()
        return self.db[name] if self.db is not None else None
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("Database connection closed")


# Create singleton instance
db_manager = DatabaseManager()
db = db_manager.connect()

# Export collections
contacts_collection = db_manager.get_collection('contacts')
projects_collection = db_manager.get_collection('projects')
skills_collection = db_manager.get_collection('skills')
analytics_collection = db_manager.get_collection('analytics')
admin_collection = db_manager.get_collection('admins')

# Cache implementation
from functools import lru_cache, wraps
from datetime import datetime, timedelta
import hashlib
import json


class CacheManager:
    """Simple in-memory cache (use Redis in production)"""

    def __init__(self):
        self.cache = {}
        self.ttl = {}

    def get(self, key):
        """Get cached value if not expired"""
        if key in self.cache:
            if datetime.utcnow() < self.ttl.get(key, datetime.utcnow()):
                return self.cache[key]
            else:
                del self.cache[key]
                del self.ttl[key]
        return None

    def set(self, key, value, ttl_seconds=300):
        """Set cache value with TTL"""
        self.cache[key] = value
        self.ttl[key] = datetime.utcnow() + timedelta(seconds=ttl_seconds)

    def delete(self, key):
        """Delete cache entry"""
        if key in self.cache:
            del self.cache[key]
            del self.ttl[key]

    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.ttl.clear()


cache_manager = CacheManager()


def cached(ttl_seconds=300):
    """Decorator for caching function results"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hashlib.md5(json.dumps([args, kwargs], sort_keys=True).encode()).hexdigest()}"

            # Check cache
            result = cache_manager.get(cache_key)
            if result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return result

            # Call function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl_seconds)
            logger.debug(f"Cache miss for {func.__name__}, cached for {ttl_seconds}s")

            return result

        return wrapper

    return decorator
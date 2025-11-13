"""
Database utilities - imports from optimized version for backward compatibility
"""

from utils.database_optimized import (
    db_manager,
    db,
    contacts_collection,
    projects_collection,
    skills_collection,
    analytics_collection,
    admin_collection,
    cache_manager,
    cached
)

__all__ = [
    'db_manager',
    'db',
    'contacts_collection',
    'projects_collection',
    'skills_collection',
    'analytics_collection',
    'admin_collection',
    'cache_manager',
    'cached'
]
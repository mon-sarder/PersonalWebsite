// MongoDB initialization script
// This runs when the MongoDB container first starts

db = db.getSiblingDB('portfolio');

// Create collections
db.createCollection('contacts');
db.createCollection('projects');
db.createCollection('skills');
db.createCollection('analytics');
db.createCollection('admins');

// Create indexes
db.projects.createIndex({ "order": 1 });
db.projects.createIndex({ "created_at": -1 });
db.projects.createIndex({ "title": "text", "description": "text" });

db.skills.createIndex({ "category": 1 });
db.skills.createIndex({ "proficiency": 1 });
db.skills.createIndex({ "name": 1 }, { unique: true });

db.contacts.createIndex({ "created_at": -1 });
db.contacts.createIndex({ "read": 1 });
db.contacts.createIndex({ "email": 1 });

db.analytics.createIndex({ "timestamp": -1 });
db.analytics.createIndex({ "type": 1 });
db.analytics.createIndex({ "type": 1, "timestamp": -1 });

db.admins.createIndex({ "username": 1 }, { unique: true });

print('✓ Portfolio database initialized successfully');
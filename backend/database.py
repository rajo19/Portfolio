from pymongo import MongoClient
from gridfs import GridFS
from config import Config

# MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client.portfolio
fs = GridFS(db)

# Collections
projects_collection = db.projects
users_collection = db.users
blog_collection = db.blog
contact_collection = db.contact
chat_sessions_collection = db.chat_sessions

def get_database():
    """Get database instance"""
    return db

def get_gridfs():
    """Get GridFS instance"""
    return fs

def get_collections():
    """Get all collections"""
    return {
        'projects': projects_collection,
        'users': users_collection,
        'blog': blog_collection,
        'contact': contact_collection,
        'chat_sessions': chat_sessions_collection
    }

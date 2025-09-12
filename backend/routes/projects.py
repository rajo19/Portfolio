from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId
from datetime import datetime
from database import projects_collection

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('', methods=['GET'])
def get_projects():
    projects = list(projects_collection.find())
    for project in projects:
        project['_id'] = str(project['_id'])
    return jsonify(projects)

@projects_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    data['updated_at'] = datetime.utcnow()
    
    result = projects_collection.insert_one(data)
    return jsonify({'message': 'Project created', 'id': str(result.inserted_id)}), 201

@projects_bp.route('/<project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    data = request.get_json()
    data['updated_at'] = datetime.utcnow()
    
    result = projects_collection.update_one(
        {'_id': ObjectId(project_id)},
        {'$set': data}
    )
    
    if result.modified_count:
        return jsonify({'message': 'Project updated'})
    return jsonify({'message': 'Project not found'}), 404

@projects_bp.route('/<project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    result = projects_collection.delete_one({'_id': ObjectId(project_id)})
    
    if result.deleted_count:
        return jsonify({'message': 'Project deleted'})
    return jsonify({'message': 'Project not found'}), 404

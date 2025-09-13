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
    try:
        # Validate project_id format
        if not ObjectId.is_valid(project_id):
            return jsonify({'error': 'Invalid project ID format'}), 400
            
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Check if project exists
        project = projects_collection.find_one({'_id': ObjectId(project_id)})
        if not project:
            return jsonify({'error': 'Project not found'}), 404
            
        # Prepare update data
        update_data = {
            'title': data.get('title', project.get('title')),
            'company': data.get('company', project.get('company')),
            'description': data.get('description', project.get('description')),
            'technologies': data.get('technologies', project.get('technologies', [])),
            'highlights': data.get('highlights', project.get('highlights', [])),
            'start_date': data.get('start_date', project.get('start_date')),
            'end_date': data.get('end_date', project.get('end_date')),
            'updated_at': datetime.utcnow()
        }
        
        # Validate required fields
        if not update_data['title']:
            return jsonify({'error': 'Title is required'}), 400
        if not update_data['company']:
            return jsonify({'error': 'Company is required'}), 400
        if not update_data['description']:
            return jsonify({'error': 'Description is required'}), 400
            
        # Update project
        result = projects_collection.update_one(
            {'_id': ObjectId(project_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Project not found'}), 404
            
        # Get updated project
        updated_project = projects_collection.find_one({'_id': ObjectId(project_id)})
        updated_project['_id'] = str(updated_project['_id'])
        
        return jsonify({
            'message': 'Project updated successfully',
            'project': updated_project
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/<project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    result = projects_collection.delete_one({'_id': ObjectId(project_id)})
    
    if result.deleted_count:
        return jsonify({'message': 'Project deleted'})
    return jsonify({'message': 'Project not found'}), 404

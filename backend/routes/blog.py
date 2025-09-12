from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId
from datetime import datetime
from database import blog_collection

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('', methods=['GET'])
def get_blog_posts():
    posts = list(blog_collection.find().sort('created_at', -1))
    for post in posts:
        post['_id'] = str(post['_id'])
    return jsonify(posts)

@blog_bp.route('', methods=['POST'])
@jwt_required()
def create_blog_post():
    data = request.get_json()
    data['author'] = 'Rajorshi Tah'
    data['created_at'] = datetime.utcnow()
    data['updated_at'] = datetime.utcnow()
    
    result = blog_collection.insert_one(data)
    return jsonify({'message': 'Blog post created', 'id': str(result.inserted_id)}), 201

@blog_bp.route('/<post_id>', methods=['PUT'])
@jwt_required()
def update_blog_post(post_id):
    data = request.get_json()
    data['updated_at'] = datetime.utcnow()
    
    result = blog_collection.update_one(
        {'_id': ObjectId(post_id)},
        {'$set': data}
    )
    
    if result.modified_count:
        return jsonify({'message': 'Blog post updated'})
    return jsonify({'message': 'Blog post not found'}), 404

@blog_bp.route('/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_blog_post(post_id):
    result = blog_collection.delete_one({'_id': ObjectId(post_id)})
    
    if result.deleted_count:
        return jsonify({'message': 'Blog post deleted'})
    return jsonify({'message': 'Blog post not found'}), 404

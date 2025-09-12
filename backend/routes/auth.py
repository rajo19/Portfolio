from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from database import users_collection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = users_collection.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token, 'user': {'username': username, 'email': user['email']}})
    
    return jsonify({'message': 'Invalid credentials'}), 401

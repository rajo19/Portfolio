from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from database import get_gridfs
import io

cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_cv():
    fs = get_gridfs()
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400
    
    # Delete existing CV files
    for grid_file in fs.find({'filename': {'$regex': '^cv_'}}):
        fs.delete(grid_file._id)
    
    # Save new CV
    filename = secure_filename(f"cv_{file.filename}")
    file_id = fs.put(file, filename=filename, content_type=file.content_type)
    
    return jsonify({'message': 'CV uploaded successfully', 'file_id': str(file_id)})

@cv_bp.route('/download', methods=['GET'])
def download_cv():
    fs = get_gridfs()
    
    cv_file = fs.find_one({'filename': {'$regex': '^cv_'}})
    if not cv_file:
        return jsonify({'message': 'CV not found'}), 404
    
    return send_file(
        io.BytesIO(cv_file.read()),
        as_attachment=True,
        download_name=cv_file.filename.replace('cv_', ''),
        mimetype=cv_file.content_type
    )

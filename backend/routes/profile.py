from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

profile_bp = Blueprint('profile', __name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    """Ensure upload folder exists"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@profile_bp.route('', methods=['GET'])
def get_profile():
    profile = {
        'name': 'Rajorshi Tah',
        'email': 'rajorshitah9@gmail.com',
        'phone': '(+81)8048172852 | (+91)9474806123',
        'location': 'Tokyo, Japan 136-0073',
        'linkedin': 'https://www.linkedin.com/in/rajorshi-tah',
        'bio': 'Software Developer at Accenture with expertise in backend development, AI/ML, and full-stack development. Experienced in building scalable systems handling thousands of requests daily.',
        'education': [
            {
                'degree': 'Masters in Mechanical Engineering',
                'institution': 'Indian Institute of Technology Kharagpur',
                'gpa': '8.63',
                'duration': 'Jul 2020 - May 2021'
            },
            {
                'degree': 'Bachelors in Mechanical Engineering',
                'institution': 'Indian Institute of Technology Kharagpur',
                'gpa': '8.63',
                'duration': 'Jul 2016 - May 2021'
            },
            {
                'degree': 'Bachelors in Computer Science and Engineering (Minor)',
                'institution': 'Indian Institute of Technology Kharagpur',
                'gpa': '8.35',
                'duration': 'Jul 2016 - May 2021'
            }
        ],
        'skills': {
            'programming': ['Python', 'C++', 'Node.js', 'React.js', 'SQL'],
            'databases': ['PostgreSQL', 'MongoDB'],
            'cloud': ['AWS', 'Azure', 'Docker', 'Git'],
            'ai_ml': ['TensorFlow', 'Keras', 'LlamaIndex', 'Transformers'],
            'specialties': ['Backend Development', 'NLP', 'Machine Learning', 'Computer Vision']
        },
        'certifications': [
            'AWS Certified Machine Learning Specialist',
            'AWS Certified Solution Architect-Associate',
            'Kaggle Expert'
        ],
        'achievements': [
            'Achieved AIR 2907(99.8 percentile) in JEE Advanced 2016',
            'Secured State Rank 49(99.98 percentile) in WBJEE 2016',
            'Secured AIR 861 (98.6 percentile) in KVPY 2015-16',
            'Secretary of Sports at B.R. Ambedkar Hall managing 1500 students'
        ],
        'profile_picture': '/api/profile/picture'  # Default or current profile picture URL
    }
    return jsonify(profile)

@profile_bp.route('/picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    """Upload profile picture (admin only)"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'message': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        # Check file size
        if len(file.read()) > MAX_FILE_SIZE:
            return jsonify({'message': 'File too large. Maximum size is 5MB'}), 400
        
        # Reset file pointer after reading
        file.seek(0)
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({'message': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400
        
        # Ensure upload directory exists
        ensure_upload_folder()
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"profile_{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Return success response with file URL
        file_url = f"/api/profile/picture/{unique_filename}"
        
        return jsonify({
            'message': 'Profile picture uploaded successfully',
            'filename': unique_filename,
            'url': file_url,
            'uploaded_at': datetime.utcnow().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Upload failed: {str(e)}'}), 500

@profile_bp.route('/profile_pic', methods=['GET'])
def get_profile_pic():
    """Get the latest profile picture"""
    try:
        # Ensure upload folder exists
        ensure_upload_folder()
        
        # Get all files in upload directory
        files = [f for f in os.listdir(UPLOAD_FOLDER) 
                if os.path.isfile(os.path.join(UPLOAD_FOLDER, f)) and f.startswith('profile_')]
        
        if not files:
            return jsonify({'message': 'No profile pictures found'}), 404
            
        # Sort files by modification time (newest first)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
        latest_file = files[0]
        
        # Serve the latest file
        return send_from_directory(UPLOAD_FOLDER, latest_file)
        
    except Exception as e:
        return jsonify({'message': f'Error getting profile picture: {str(e)}'}), 500
        
@profile_bp.route('/picture/<filename>', methods=['GET'])
def get_profile_picture(filename):
    """Serve specific profile picture file (legacy endpoint)"""
    try:
        # Security check - ensure filename is safe
        safe_filename = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({'message': 'Profile picture not found'}), 404
        
        # Serve the file
        return send_from_directory(UPLOAD_FOLDER, safe_filename)
        
    except Exception as e:
        return jsonify({'message': f'Error serving file: {str(e)}'}), 500

@profile_bp.route('/picture', methods=['DELETE'])
@jwt_required()
def delete_profile_picture():
    """Delete current profile picture (admin only)"""
    try:
        filename = request.json.get('filename')
        
        if not filename:
            return jsonify({'message': 'Filename required'}), 400
        
        # Security check
        safe_filename = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        # Check if file exists and delete
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': 'Profile picture deleted successfully'})
        else:
            return jsonify({'message': 'Profile picture not found'}), 404
            
    except Exception as e:
        return jsonify({'message': f'Delete failed: {str(e)}'}), 500

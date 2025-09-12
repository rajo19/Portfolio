from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config
from models import init_database

# Import route blueprints
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.cv import cv_bp
from routes.ai import ai_bp
from routes.contact import contact_bp
from routes.blog import blog_bp
from routes.profile import profile_bp

app = Flask(__name__)

# Load configuration
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_DEFAULT_SENDER

# Initialize extensions
CORS(app)
jwt = JWTManager(app)
mail = Mail()
mail.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(projects_bp, url_prefix='/api/projects')
app.register_blueprint(cv_bp, url_prefix='/api/cv')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(contact_bp, url_prefix='/api/contact')
app.register_blueprint(blog_bp, url_prefix='/api/blog')
app.register_blueprint(profile_bp, url_prefix='/api/profile')

if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=8000)

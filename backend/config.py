import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'your-secret-key-here')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Mail configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    
    # Database configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/portfolio')
    
    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

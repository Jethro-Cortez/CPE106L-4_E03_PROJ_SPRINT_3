import os

class Config:
    """Configuration class for Flask application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_123')
    ADMIN_SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY', 'admin123')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///library.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
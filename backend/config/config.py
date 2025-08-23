import os

class Config:
    """Application configuration"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///easyx.db'

    # backend/config/config.py
    MAX_DAILY_HOURS = 12.0
    HOUR_TOLERANCE = 0.01

    # API configuration
    API_VERSION = 'v1'



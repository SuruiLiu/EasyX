import os

# Timesheet validation configuration
MAX_DAILY_HOURS_DEFAULT = 12.0
HOUR_TOLERANCE = 0.01

class Config:
    """Application configuration"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    
    # Database configuration

    # DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///easyx.db'
    # new database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://easyx:easyxpass@postgres:5432/easyxdb"
    )
    
    # API configuration
    API_VERSION = 'v1'
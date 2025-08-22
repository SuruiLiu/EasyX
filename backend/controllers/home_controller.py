from flask import Blueprint
from services.home_service import HomeService

home_bp = Blueprint('home', __name__)
home_service = HomeService()

@home_bp.route('/', methods=['GET'])
def get_welcome():
    """Get welcome message"""
    return home_service.get_welcome_message()

@home_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return home_service.health_check()

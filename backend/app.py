from flask import Flask
from flask_cors import CORS
from config.config import Config
from controllers.home_controller import home_bp
from controllers.pdf_extraction_controller import pdf_extraction_bp
from backend.controllers.timesheet_controller import bp_timesheet

# init database
from services.db_init import init_db_and_seed

def create_app():
    """Create Flask application"""
    # for test
    print(">>> create_app CALLED <<<", flush=True)

    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend-backend communication
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(pdf_extraction_bp)
    app.register_blueprint(bp_timesheet)
   

    # Use the native SQLAlchemy, without relying on the app context. Just call it directly.
    init_db_and_seed()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)

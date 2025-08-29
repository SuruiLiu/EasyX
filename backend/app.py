from flask import Flask
from flask_cors import CORS
from config.config import Config
from controllers.home_controller import home_bp
from controllers.timesheet_controller import bp_timesheet
from controllers.pdf_extraction_controller import pdf_extraction_bp
from controllers.timesheet_query_controller import bp_timesheet_query 

def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend-backend communication
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(bp_timesheet)
    app.register_blueprint(pdf_extraction_bp)
    app.register_blueprint(bp_timesheet_query)    # GET /timesheet/<tid>
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)

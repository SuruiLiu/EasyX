class HomeService:
    """Home page related services"""
    
    def get_welcome_message(self):
        """Get welcome message"""
        return "Welcome EasyX"
    
    def health_check(self):
        """Health check service"""
        return {
            "status": "healthy",
            "message": "EasyX backend is running"
        }

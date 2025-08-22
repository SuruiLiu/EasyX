# EasyX - Payroll Automation System

A comprehensive payroll automation system that extracts data from PDF timesheets, validates against expected data, and integrates with Xero for seamless payroll processing.

## 🎯 Sprint 1 Goals
- **Database to hold "expected data"**: Collaborate to determine necessary data structure and storage requirements
- **Mapping data from PDF to Xero**: Develop a robust method to map and store extracted data in Xero-compatible format
- **Extracting data from PDF**: Implement an intelligent system to extract and store timesheet data from PDF documents
- **Comparing extracted data to expected data**: Create a validation mechanism to ensure data accuracy and flag discrepancies

## 🏗️ Technology Stack

### Frontend
- **React 18**: Modern JavaScript library for building user interfaces
- **JavaScript ES6+**: Latest JavaScript features for enhanced development
- **HTML5/CSS3**: Standard web technologies for structure and styling
- **npm**: Package manager for JavaScript dependencies

### Backend
- **Python 3.x**: Primary programming language for backend services
- **Flask 2.3.3**: Lightweight web framework for API development
- **Flask-CORS**: Cross-Origin Resource Sharing support for frontend-backend communication
- **Virtual Environment**: Isolated Python environment for dependency management

## 📁 Project Structure

```
EasyX/
├── frontend/                    # React Frontend Application
│   ├── public/
│   │   └── index.html          # HTML template
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Header.js       # Application header component
│   │   │   └── Footer.js       # Application footer component
│   │   ├── pages/              # Page-level components
│   │   │   └── Home.js         # Main dashboard page
│   │   ├── App.js              # Root application component
│   │   └── index.js            # Application entry point
│   └── package.json            # Frontend dependencies and scripts
├── backend/                     # Flask Backend API
│   ├── controllers/            # Request handling layer
│   │   └── home_controller.py  # Home route controller
│   ├── services/               # Business logic layer
│   │   └── home_service.py     # Home-related services
│   ├── models/                 # Data model definitions
│   │   ├── __init__.py
│   │   └── base_model.py       # Base model class
│   ├── config/                 # Configuration management
│   │   └── config.py           # Application configuration
│   ├── app.py                  # Flask application entry point
│   ├── requirements.txt        # Python dependencies
│   └── venv/                   # Python virtual environment (auto-generated)
├── .github/                    # GitHub automation
│   ├── workflows/              # GitHub Actions workflows
│   └── ISSUE_TEMPLATE/         # Issue and PR templates
├── start.sh                    # One-click startup script
└── README.md                   # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.x installed
- Node.js and npm installed
- Git for version control

### Installation & Running
1. **Clone the repository**:
   ```bash
   git clone https://github.com/SuruiLiu/EasyX.git
   cd EasyX
   ```

2. **Start the system** (one command starts both frontend and backend):
   ```bash
   ./start.sh
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Health Check: http://localhost:5000/health

## 📋 User Scenarios
Refer to the detailed user scenarios in [Issue #34](https://github.com/SuruiLiu/EasyX/issues/34) for insights into how the system is used in real-world payroll processing situations.

## 📊 PBI Progress
Track the progress of Product Backlog Items (PBIs) in the [project board](https://github.com/users/SuruiLiu/projects/2).

## 🤝 Contributing
To contribute to this project, please follow these steps:

1. **Create a new branch** for your feature or bugfix
2. **Commit your changes** with clear, descriptive messages
3. **Push your branch** to your fork
4. **Open a pull request** to the main repository and request a review
5. **Ensure your code** passes all tests and adheres to the project's coding standards

### Development Guidelines
- Follow the established project structure
- Write clear, self-documenting code
- Include appropriate error handling
- Test your changes thoroughly before submitting

We welcome contributions and appreciate your efforts to improve the project!

## 📄 License
This project is part of academic coursework and follows university guidelines for collaborative development.

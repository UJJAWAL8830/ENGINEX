from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config # Import the configuration class from your root directory

# Initialize the database globally so it can be accessed by models
db = SQLAlchemy()

def create_app():
    app = Flask(_name_)
    
    # Apply centralized configurations [cite: 7, 26]
    app.config.from_object(Config)

    # Initialize the app with the database [cite: 40]
    db.init_app(app)

    # 1. Import Blueprints to maintain modular service delivery [cite: 21, 26]
    from .auth import auth
    from .agri.routes import agri
    from .health_care.routes import health_care
    from .security.routes import security

    # 2. Register Blueprints with appropriate URL prefixes [cite: 26, 27]
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(agri, url_prefix='/agri')
    app.register_blueprint(health_care, url_prefix='/health-care')
    app.register_blueprint(security, url_prefix='/security')

    # 3. Import ALL models here so SQLAlchemy detects them for table creation [cite: 44]
    from .models import Citizens, Govt, ServiceProviders, Scheme
    from .health_care.models import Hospital, Doctor
    from .agri.models import AgriCenter

    with app.app_context():
        # Automatically creates tables in PostgreSQL if they don't exist [cite: 40, 47]
        db.create_all()

    # 4. Setup Login Manager for secure session handling [cite: 8]
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # Multi-table check to support diverse user types: Citizens, Govt, and Providers [cite: 41, 48, 49]
        user = Citizens.query.get(int(id))
        if not user:
            user = Govt.query.get(int(id))
        if not user:
            user = ServiceProviders.query.get(int(id))
        return user

    return app
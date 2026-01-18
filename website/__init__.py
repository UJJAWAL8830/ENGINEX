from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # 1. Import Blueprints
    from .agri import agri
    from .health_care import health_care
    from .security import security
    from .auth import auth
    from .routes import routes

    # 2. Register Blueprints with specific prefixes
    # Citizen-specific dashboard and services
    app.register_blueprint(routes, url_prefix='/') 
    
    # Authentication routes (login, signup, logout)
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Departmental portals
    app.register_blueprint(agri, url_prefix='/agri')

    app.register_blueprint(health_care, url_prefix='/health_care')

    app.register_blueprint(security, url_prefix='/security')

    # 3. Model Registration for db.create_all()
    from .models import Citizens, Govt, ServiceProviders, Scheme
    from .health_care.models import Hospital, Doctor
    from .agri.models import AgriCenter, AgriComplaint # Added your new complaint table

    with app.app_context():
        db.create_all()

    # 4. Setup Login Manager for secure session handling
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # Multi-table check to support diverse user types: Citizens, Govt, and Providers
        user = Citizens.query.get(int(id))
        if not user:
            user = Govt.query.get(int(id))
        if not user:
            user = ServiceProviders.query.get(int(id))
        return user

    return app
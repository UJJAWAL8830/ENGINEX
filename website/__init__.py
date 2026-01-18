from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config 
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from .agri import agri
    from .health_care import health_care
    from .security import security
    from .auth import auth
    from .routes import routes

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(agri, url_prefix='/agri')
    app.register_blueprint(health_care, url_prefix='/health-care')
    app.register_blueprint(security, url_prefix='/security')


    from .models import Citizens, Govt, ServiceProviders, Scheme
    from .health_care.models import Hospital, Doctor
    from .agri.models import AgriCenter

    with app.app_context():

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
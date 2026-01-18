from flask import Blueprint

# Define the Blueprint named 'users'
users_bp = Blueprint('users', __name__, template_folder='templates')

# Import the routes so the app knows about them
from . import routes
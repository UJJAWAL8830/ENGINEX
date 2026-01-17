from flask import Blueprint

# 1. Create the Blueprint object
# 'users' is the name of the blueprint
# __name__ locates the folder
# template_folder tells Flask where to look for HTML files inside this folder
users_bp = Blueprint('users', __name__, template_folder='templates')

# 2. Import routes at the BOTTOM
# This looks weird, but it is necessary. 
# The routes need the 'users_bp' object created above, so we must import them AFTER creating it.
from . import routes
from flask import Blueprint

# 1. Create the Blueprint named 'health_care'
health_care = Blueprint('health_care', __name__)

# 2. Import the routes (Must be at the bottom to avoid errors)
from . import routes
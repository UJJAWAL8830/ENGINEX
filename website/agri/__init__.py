from flask import Blueprint

# Define the blueprint here
agri = Blueprint('agri', __name__)

# Import routes at the bottom to prevent circular import
from . import routes
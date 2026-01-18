from flask import Blueprint

health_care= Blueprint('health_care', __name__)

from .import routes
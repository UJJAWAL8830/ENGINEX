from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import current_user
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    # Public landing page: If already logged in, move to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    return render_template("index.html", user=current_user)

@routes.route('/home')
def home():
    # Manual Authentication Check
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    # Role-Based Redirection Gatekeeper
    role = session.get('role')
    if role != 'citizen':
        sector = session.get('sector')
        if sector == 'Health':
            return redirect(url_for('health_care.health_dashboard'))
        elif sector == 'Agriculture':
            return redirect(url_for('agri.agri_dashboard'))
        elif sector == 'Security':
            return redirect(url_for('security.security_dashboard'))
        return redirect(url_for('routes.index'))

    # Context for JanSetu 2026 platform
    now = datetime.now().strftime("%A, %d %b %Y")
    return render_template("home.html", 
                           user=current_user, 
                           current_time_formatted=now)

@routes.route('/services')
def services():
    # Manual Authentication Check
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    # Service directory orchestrator for verified citizens
    if session.get('role') != 'citizen':
        return redirect(url_for('routes.home'))
    return render_template("services.html")

@routes.route('/notices')
def notices():
    # Manual Authentication Check
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    # Transparent communication for authenticated stakeholders
    return render_template("news.html", user=current_user)
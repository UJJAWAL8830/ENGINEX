from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Citizens, Govt, ServiceProviders
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        state = request.form.get('state')
        city = request.form.get('city')

        user = Citizens.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            new_citizen = Citizens(
                email=email,
                full_name=full_name,
                password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
                state=state,
                city=city
            )
            db.session.add(new_citizen)
            db.session.commit()
            flash('Account created! You can now log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template("login.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 1. Sequential check to find the user and determine the role
        user = Citizens.query.filter_by(email=email).first()
        role = 'citizen'

        if not user:
            user = ServiceProviders.query.filter_by(email=email).first()
            role = 'provider'

        if not user:
            user = Govt.query.filter_by(email=email).first()
            role = 'government'

        # 2. Authentication and Role-Based Redirection
        if user and check_password_hash(user.password_hash, password):
            # Using flask-login for session management
            login_user(user, remember=True)
            session['role'] = role
            
            if role == 'citizen':
                return redirect(url_for('routes.home'))
            
            elif role == 'provider':
                # Replace with your actual service provider dashboard route
                return redirect(url_for('routes.admin_provider_dashboard'))
            
            elif role == 'government':
                session['sector'] = user.sector # Store Health/Agri/Security
                
                # Nested logic for Sector-Based routing
                if user.sector == 'Health':
                    return redirect(url_for('health_care.health_dashboard'))
                elif user.sector == 'Agriculture':
                    return redirect(url_for('agri.agri_dashboard'))
                elif user.sector == 'Security':
                    return redirect(url_for('security.security_dashboard'))
                else:
                    return redirect(url_for('routes.index'))
        else:
            flash('Login failed. Please check your email and password.', category='error')
            
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))
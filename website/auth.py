import redis
from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from .models import Citizens
from werkzeug.security import generate_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Collect data from the form
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        state = request.form.get('state')
        city = request.form.get('city')

        # Check if citizen already exists
        user = Citizens.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            # Create new citizen entry
            new_citizen = Citizens(
                email=email,
                full_name=full_name,
                password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
                state=state,
                city=city,
            )
            db.session.add(new_citizen)
            db.session.commit()
            flash('Account created! You can now log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Sequential check across tables
        user = Citizens.query.filter_by(email=email).first()
        role = 'citizen'

        # if not user:
        #     user = GovEmployees.query.filter_by(email=email).first()
        #     role = 'government'

        # if not user:
        #     user = ServiceProviders.query.filter_by(email=email).first()
        #     role = 'provider'

        # if user and check_password_hash(user.password_hash, password):
            # session['user_id'] = user.id
            # session['role'] = role
            # if role == 'government':
                # session['sector'] = user.sector # Store Health/Agri/Security [cite: 35]
            
            # return redirect(url_for('main.home'))
            
    return render_template("login.html")
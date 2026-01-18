# # from flask import Flask, redirect, url_for
# # from users import users_bp  # Import your blueprint

# # app = Flask(__name__)

# # # Register the blueprint (routes start with /citizen)
# # app.register_blueprint(users_bp, url_prefix='/citizen')

# # # --- THE FIX IS HERE ---
# # @app.route('/')
# # def index():
# #     # Automatically redirect localhost:5000 -> localhost:5000/citizen/home
# #     return redirect(url_for('users.home'))

# # if __name__ == '__main__':
# #     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, session, url_for
# from users import users_bp  # <--- IMPORT YOUR BLUEPRINT

# app = Flask(__name__)
# app.secret_key = 'ingenium_secret_key'

# # --- 1. REGISTER THE BLUEPRINT ---
# # This connects the "users" folder to the app.
# # All citizen routes will start with /citizen (e.g., /citizen/home)
# app.register_blueprint(users_bp, url_prefix='/citizen')

# # --- 2. UNIVERSAL LANDING PAGE ---
# @app.route('/')
# def universal_home():
#     return render_template('index.html')

# # --- 3. LOGIN ROUTE (The Gatekeeper) ---
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Retrieve form data
#         email = request.form.get('email')
#         password = request.form.get('password')
#         role = request.form.get('role') 

#         # --- SIMULATED AUTHENTICATION ---
#         session['user'] = email
#         session['role'] = role
        
#         # --- THE REDIRECT LOGIC ---
#         if role == 'citizen':
#             # Redirect to the Blueprint Route: 'users.home'
#             # Flask looks inside users/routes.py for the 'home' function
#             return redirect(url_for('users.home'))
            
#         elif role == 'admin':
#             return redirect(url_for('admin_dashboard'))
            
#         elif role == 'provider':
#             return redirect(url_for('kanban_board'))

#     return render_template('login.html')

# # --- 4. PLACEHOLDER ROUTES (For Admin/Provider) ---
# @app.route('/admin')
# def admin_dashboard():
#     return "<h1>Admin Dashboard (Coming Soon)</h1>"

# @app.route('/provider')
# def kanban_board():
#     return "<h1>Service Provider Kanban (Coming Soon)</h1>"

# # --- 5. LOGOUT ---
# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('universal_home'))

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
import redis
from flask import Flask, render_template, request, redirect, session, url_for
from users import users_bp
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# 1. IMPORT YOUR DATABASE MODELS
# We add 'Hospital' here so we can use it in the Admin Dashboard
from users.models import db, Citizen, GovEmployee, ServiceProvider, Hospital , AgriMarket

app = Flask(__name__)
app.secret_key = 'ingenium_secret_key'

app.config['SESSION_TYPE'] = 'redis'  # Use Redis
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'jansetu:'

# --- DATABASE CONFIGURATION ---
# Update this with your actual PostgreSQL password/DB name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingenium'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_REDIS'] = redis.from_url("redis://127.0.0.1:6379")

# Initialize DB and Session

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://127.0.0.1:6379", # <--- Connects to your running Redis
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window" # Standard counting method
)

# Initialize DB with this app
db.init_app(app)
Session(app)

# Register the Blueprint (Your Citizen Routes)
app.register_blueprint(users_bp, url_prefix='/citizen')

# ==========================================
# 1. PUBLIC ROUTES & LOGIN
# ==========================================

@app.route('/')
def universal_home():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('universal_home'))

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 1. CHECK CITIZENS
        user = Citizen.query.filter_by(email=email).first()
        if user and user.password_hash == password:
            session['user_id'] = user.id
            session['role'] = 'citizen'
            return redirect(url_for('users.home'))

        # 2. CHECK GOV EMPLOYEES (ADMIN)
        user = GovEmployee.query.filter_by(email=email).first()
        if user and user.password_hash == password:
            session['user_id'] = user.id
            session['role'] = 'admin'
            session['sector'] = user.sector 
            
            # Intelligent Redirect: If Health Admin, go to Health Dashboard
            if user.sector == 'Health':
                return redirect(url_for('admin_health_dashboard'))
            elif user.sector == 'Agriculture':  # <--- NEW LOGIC
                return redirect(url_for('admin_agri_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))

        # 3. CHECK SERVICE PROVIDERS
        user = ServiceProvider.query.filter_by(email=email).first()
        if user and user.password_hash == password:
            session['user_id'] = user.id
            session['role'] = 'provider'
            return redirect(url_for('kanban_board'))

        return "Account not found or Incorrect Password."

    return render_template('login.html')

# ==========================================
# 2. ADMIN HEALTH DASHBOARD (The New Features)
# ==========================================

@app.route('/admin/health')
def admin_health_dashboard():
    # Security: Ensure only Admins can access
    if session.get('role') != 'admin': return redirect(url_for('login'))
    
    # A. Fetch Dynamic Data (From Database)
    hospitals = Hospital.query.all()
    
    # B. Static Stats (For Visual Appeal)
    stats = {
        "patients": 12450,
        "ambulances": 45,
        "stock": "82%"
    }
    
    # Make sure this template exists at templates/admin/health_dashboard.html
    return render_template('admin/health_dashboard.html', hospitals=hospitals, stats=stats)

@app.route('/admin/health/add', methods=['POST'])
def add_health_center():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    
    # Get form data
    name = request.form.get('name')
    address = request.form.get('address')
    type = request.form.get('type')
    beds = request.form.get('beds')
    contact = request.form.get('contact')
    
    # Save to DB
    new_hospital = Hospital(name=name, address=address, type=type, beds=int(beds or 0), contact=contact)
    db.session.add(new_hospital)
    db.session.commit()
    
    return redirect(url_for('admin_health_dashboard'))

@app.route('/admin/health/delete/<int:id>')
def delete_health_center(id):
    if session.get('role') != 'admin': return redirect(url_for('login'))
    
    hospital = Hospital.query.get(id)
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
    return redirect(url_for('admin_health_dashboard'))

# ==========================================
# 3. OTHER DASHBOARDS (Placeholders)
# ==========================================

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return f"<h1>Government Dashboard: {session.get('sector')} Sector (General View)</h1>"

@app.route('/provider')
def kanban_board():
    if session.get('role') != 'provider': return redirect(url_for('login'))
    return "<h1>Service Provider Kanban Board</h1>"

@app.route('/admin/agriculture')
def admin_agri_dashboard():
    # Security Check
    if session.get('role') != 'admin': return redirect(url_for('login'))
    
    # 1. Fetch Dynamic Data (Live Market Prices)
    market_data = AgriMarket.query.all()
    
    # 2. Static Stats (For Visual Appeal)
    stats = {
        "active_farmers": "5,600",
        "soil_cards_issued": "120",
        "rainfall_alert": "Normal"
    }
    
    return render_template('admin/agri_dashboard.html', market_data=market_data, stats=stats)

# --- ACTION: ADD CROP PRICE ---
@app.route('/admin/agriculture/add-price', methods=['POST'])
def add_agri_price():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    
    # Get Form Data
    crop_name = request.form.get('crop_name')
    market_name = request.form.get('market_name')
    price = request.form.get('price')
    status = request.form.get('status')
    
    # Save to Database
    new_entry = AgriMarket(
        crop_name=crop_name, 
        market_name=market_name, 
        price=price, 
        status=status,
        updated_date="Today" # You can use datetime.now() if you want
    )
    
    db.session.add(new_entry)
    db.session.commit()
    
    return redirect(url_for('admin_agri_dashboard'))

# --- ACTION: DELETE ENTRY ---
@app.route('/admin/agriculture/delete/<int:id>')
def delete_agri_price(id):
    if session.get('role') != 'admin': return redirect(url_for('login'))
    
    entry = AgriMarket.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('admin_agri_dashboard'))


@app.route('/seed-citizens')
def seed_citizens():
    # 1. Create Table if missing
    with app.app_context():
        db.create_all()

        # 2. Define Mock Users
        test_users = [
            {"email": "student@test.com", "pass": "123", "name": "Rahul Student"},
            {"email": "farmer@test.com", "pass": "123", "name": "Ramesh Kisan"},
            {"email": "citizen@test.com", "pass": "123", "name": "Amit Citizen"}
        ]

        # 3. Loop and Insert
        added_count = 0
        for u in test_users:
            # Check if email exists to prevent crash
            existing = Citizen.query.filter_by(email=u['email']).first()
            if not existing:
                new_user = Citizen(
                    email=u['email'],
                    password_hash=u['pass'], # Storing as '123' for simplicity
                    full_name=u['name'],
                    
                )
                db.session.add(new_user)
                added_count += 1
        
        db.session.commit()
        
        return f"✅ Success! {added_count} new citizens added.<br>Login with <b>student@test.com</b> and password <b>123</b>"
    
# ==========================================
# 🛑 CUSTOM ERROR HANDLER (The New Part)
# ==========================================
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html'), 429
    


# --- TEMPORARY ROUTE TO CREATE AGRI ADMIN ---
@app.route('/create-agri-admin')
def create_agri_admin():
    # Check if exists
    existing = GovEmployee.query.filter_by(email="admin@agri.gov.in").first()
    if existing: return "Agri Admin already exists!"

    # Create User
    agri_admin = GovEmployee(
        full_name="Dr. M. Swaminathan",
        email="admin@agri.gov.in",     # <--- LOGIN ID
        password_hash="admin123",
        department="Ministry of Agriculture",
        sector="Agriculture",          # <--- THIS TRIGGERS THE DASHBOARD
        role="admin"
    )
    
    db.session.add(agri_admin)
    db.session.commit()
    return "✅ Agri Admin Created! Login with: <b>admin@agri.gov.in</b> / <b>admin123</b>"

if __name__ == '__main__':
    # Ensure tables exist
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=5000)
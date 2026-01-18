from flask import Flask, render_template, request, redirect, session, url_for
from users import users_bp
# 1. IMPORT YOUR DATABASE MODELS
# (Make sure these import paths match your actual project structure)
from users.models import db, Citizen, GovEmployee, ServiceProvider 

app = Flask(__name__)
app.secret_key = 'ingenium_secret_key'

# Database Configuration (Update with your actual DB details)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/ingenium'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB with this app
db.init_app(app)

app.register_blueprint(users_bp, url_prefix='/citizen')

# --- UNIVERSAL LANDING PAGE ---
@app.route('/')
def universal_home():
    return render_template('index.html')

# --- INTELLIGENT LOGIN ROUTE (Auto-Detects Role) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # WE REMOVED THE 'ROLE' INPUT. 
        # NOW WE SEARCH THE TABLES ONE BY ONE.

        # 1. CHECK CITIZENS TABLE
        user = Citizen.query.filter_by(email=email).first()
        if user:
            # Found in Citizen Table! Validate Password.
            if user.password_hash == password: # In real app, use check_password_hash()
                session['user_id'] = user.id
                session['role'] = 'citizen'
                return redirect(url_for('users.home'))
            else:
                return "Incorrect Password for Citizen account"

        # 2. CHECK GOV EMPLOYEES TABLE (If not found in Citizens)
        user = GovEmployee.query.filter_by(email=email).first()
        if user:
            if user.password_hash == password:
                session['user_id'] = user.id
                session['role'] = 'admin'
                session['sector'] = user.sector # Save sector (Health/Agri) to session
                return redirect(url_for('admin_dashboard'))
            else:
                return "Incorrect Password for Government account"

        # 3. CHECK SERVICE PROVIDERS TABLE (If not found in Gov)
        user = ServiceProvider.query.filter_by(email=email).first()
        if user:
            if user.password_hash == password:
                session['user_id'] = user.id
                session['role'] = 'provider'
                return redirect(url_for('kanban_board'))
            else:
                return "Incorrect Password for Service Provider account"

        # 4. IF EMAIL NOT FOUND IN ANY TABLE
        return "Account not found. Please Sign Up if you are a Citizen."

    return render_template('login.html')

# --- PLACEHOLDER DASHBOARDS ---
@app.route('/admin')
def admin_dashboard():
    # Security check
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return f"<h1>Government Dashboard: {session.get('sector')} Sector</h1>"

@app.route('/provider')
def kanban_board():
    if session.get('role') != 'provider': return redirect(url_for('login'))
    return "<h1>Service Provider Kanban Board</h1>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('universal_home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
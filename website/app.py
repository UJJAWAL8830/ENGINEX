from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'ingenium_secret_key'  # Required for session management

# --- 1. UNIVERSAL LANDING PAGE ---
@app.route('/')
def universal_home():
    return render_template('index.html')

# --- 2. LOGIN ROUTE (Connectivity Logic) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve data from the login form
        role = request.form.get('role')
        email = request.form.get('email')
        password = request.form.get('password')
        department = request.form.get('department') # Only relevant for admins
        
        # --- SIMPLE AUTH LOGIC (Hackathon Mode) ---
        # Storing user info in session to simulate a logged-in state
        
        session['user'] = email
        session['role'] = role
        
        # ==> CONNECTIVITY CHECK: Redirect based on Role <==
        
        if role == 'citizen':
            # If the user is a Citizen -> Redirect to Citizen Home Page
            return redirect(url_for('citizen_home'))
            
        elif role == 'admin':
            # If the user is an Admin -> Redirect to Admin Dashboard (Future step)
            session['department'] = department
            return redirect(url_for('admin_dashboard'))
            
        elif role == 'developer':
            # If the user is a Developer -> Redirect to Developer Portal (Future step)
            return redirect(url_for('developer_portal'))
            
    return render_template('login.html')

# --- 3. CITIZEN ROUTES (Connected to citizen/home.html) ---
@app.route('/citizen/home')
def citizen_home():
    # Security Check: If user is not logged in or not a citizen, redirect to login
    if session.get('role') != 'citizen':
        return redirect(url_for('login'))
        
    # This renders the specific 'citizen/home.html' template we built
    return render_template('citizen/home.html')

@app.route('/citizen/services')
def citizen_services():
    # Security Check
    if session.get('role') != 'citizen':
        return redirect(url_for('login'))
    return render_template('citizen/services.html')

@app.route('/citizen/news')
def citizen_news():
    # Security Check
    if session.get('role') != 'citizen':
        return redirect(url_for('login'))
    return render_template('citizen/news.html')

# --- ADD THESE NEW ROUTES UNDER THE CITIZEN SECTION ---

@app.route('/citizen/services/health')
def service_health():
    if session.get('role') != 'citizen': return redirect(url_for('login'))
    return render_template('citizen/services/health.html')

@app.route('/citizen/services/agriculture')
def service_agriculture():
    if session.get('role') != 'citizen': return redirect(url_for('login'))
    return render_template('citizen/services/agriculture.html')

@app.route('/citizen/services/security')
def service_security():
    if session.get('role') != 'citizen': return redirect(url_for('login'))
    return render_template('citizen/services/security.html')


# --- 4. PLACEHOLDERS FOR OTHER ROLES ---
@app.route('/admin/dashboard')
def admin_dashboard():
    dept = session.get('department', 'General')
    # Route to specific admin dashboard based on department
    if dept.lower() == 'agriculture':
        return render_template('admin/agriculture_admin.html')
    elif dept.lower() == 'health':
        return render_template('admin/health_admin.html')
    elif dept.lower() == 'security':
        return render_template('admin/security_admin.html')
    else:
        return f"<h1>Welcome {dept} Admin (Dashboard Coming Soon)</h1>"


# Direct routes for admin pages (optional, for direct access)
@app.route('/admin/agriculture')
def admin_agriculture():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin/agriculture_admin.html')

@app.route('/admin/health')
def admin_health():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin/health_admin.html')

@app.route('/admin/security')
def admin_security():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin/security_admin.html')

@app.route('/developer/portal')
def developer_portal():
    return "<h1>Developer Portal (Coming Soon)</h1>"

# --- 5. LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('universal_home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
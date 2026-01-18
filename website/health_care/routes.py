from flask import render_template, request, redirect, url_for, session
from . import users_bp
from .models import db, Hospital  # Ensure users/models.py has the Hospital class

# ==========================================
# 1. CITIZEN VIEW (The Output)
# ==========================================
@users_bp.route('/services/health')
def health():
    # Fetch all hospitals to show to the citizen
    hospitals = Hospital.query.all()
    return render_template('users/services/health.html', hospitals=hospitals)

# ==========================================
# 2. ADMIN DASHBOARD (The Input)
# ==========================================
@users_bp.route('/admin/health')
def admin_health_dashboard():
    # Security: Ensure only Admins can access
    # (Uncomment this line once your login is fully working)
    # if session.get('role') != 'admin': return redirect(url_for('login'))
    
    # 1. Fetch Dynamic Data (Real Database Data)
    hospitals = Hospital.query.all()
    
    # 2. Static Data (For the "Cool" Graphs)
    stats = {
        "total_patients": 12450,
        "active_ambulances": 45,
        "medicine_stock": "82%"
    }
    
    return render_template('admin/health_dashboard.html', hospitals=hospitals, stats=stats)

# ==========================================
# 3. ADMIN ACTIONS (Add & Delete)
# ==========================================
@users_bp.route('/admin/health/add-center', methods=['POST'])
def add_health_center():
    # 1. Get data from the form
    name = request.form.get('name')
    address = request.form.get('address')
    hospital_type = request.form.get('type') # Changed variable name from 'type' to avoid Python conflict
    beds = request.form.get('beds')
    contact = request.form.get('contact')
    
    # 2. Save to Database (with safety check for beds)
    new_hospital = Hospital(
        name=name, 
        address=address, 
        type=hospital_type, 
        beds=int(beds) if beds else 0, # Fix: Prevents crash if beds is empty
        contact=contact
    )
    
    db.session.add(new_hospital)
    db.session.commit()
    
    return redirect(url_for('users.admin_health_dashboard'))

@users_bp.route('/admin/health/delete/<int:id>')
def delete_health_center(id):
    hospital = Hospital.query.get(id)
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
    return redirect(url_for('users.admin_health_dashboard'))
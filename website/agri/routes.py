from flask import render_template, redirect, url_for, flash ,Blueprint, request
from flask_login import login_required, current_user
from .models import AgriCenter
from ..models import Citizens,Complaint,db
from . import agri


@agri.route('/agri_dashboard')
@login_required
def agri_dashboard():
    # Role Verification: Only citizens can access agricultural support services [cite: 49]
    if not isinstance(current_user, Citizens):
        flash("Access Denied: This dashboard is for Citizens/Farmers.", category="error")
        return redirect(url_for('auth.login'))

    # ORM query: Get centers located in the user's city
    # This fulfills the goal of providing "farmer support" at a local scale [cite: 21, 26]
    user_city = current_user.city
    centers = AgriCenter.query.filter_by(city=user_city).all()
    
    return render_template("agri/agri_dashboard.html", 
                           centers=centers, 
                           city=user_city)

@agri.route('/file-grievance', methods=['GET', 'POST'])
@login_required
def file_grievance():
    if not isinstance(current_user, Citizens):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_complaint = Complaint(
            title=request.form.get('title'),
            description=request.form.get('description'),
            category='Agriculture',
            city=current_user.city,
            citizen_id=current_user.id
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash("Agricultural grievance submitted.", category="success")
        return redirect(url_for('agri.agri_dashboard'))

    return render_template("agri/report.html")
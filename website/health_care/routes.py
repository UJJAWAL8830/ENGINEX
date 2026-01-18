from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from werkzeug.security import generate_password_hash
from .. import db
from flask_login import login_required, current_user
from .models import Hospital
from ..models import Citizens,Complaint 
from . import health_care
@health_care.route('/health_dashboard')
@login_required
def health_dashboard():
    
    if not isinstance(current_user, Citizens):
        flash("Access Denied: This portal is reserved for Citizens.", category="error")
        return redirect(url_for('auth.login'))

    
    user_city = current_user.city
    hospitals = Hospital.query.filter_by(city=user_city).all()
    
    return render_template("health_care/health_dashboard.html", 
                           hospitals=hospitals, 
                           city=user_city)


@health_care.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if not isinstance(current_user, Citizens):
        flash("Access Denied: This portal is reserved for Citizens.", category="error")
        return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        patient_name = request.form.get('patient_name')
        doctor_id = request.form.get('doctor_id')
        appointment_date = request.form.get('appointment_date')

        flash('Appointment booked successfully!', category='success')
        return redirect(url_for('health_care.health_dashboard'))

    return render_template("book_appointment.html")


@health_care.route('/report-issue', methods=['GET', 'POST'])
@login_required
def report_issue():
    # Only citizens can file complaints to ensure data protection [cite: 55]
    if not isinstance(current_user, Citizens):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_complaint = Complaint(
            title=request.form.get('title'),
            description=request.form.get('description'),
            category='Health Care',
            city=current_user.city,
            citizen_id=current_user.id
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash("Healthcare issue reported successfully.", category="success")
        return redirect(url_for('health_care.health_dashboard'))

    return render_template("health_care/report.html")

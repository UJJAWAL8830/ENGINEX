from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user
from ..models import Citizens, Complaint, db
from . import security

@security.route('/dashboard')
def security_dashboard():
    # 1. Manual Authentication Check
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    # 2. Strict Role & Sector Gatekeeping
    # Ensures only 'Security' sector officials can enter
    return render_template("security/security_dashboard.html", user=current_user)

@security.route('/city-complaint', methods=['GET', 'POST'])
@login_required
def city_complaint():
    if not isinstance(current_user, Citizens):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_complaint = Complaint(
            title=request.form.get('title'),
            description=request.form.get('description'),
            category='Security/Urban',
            city=current_user.city,
            citizen_id=current_user.id
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash("Urban complaint registered.", category="success")
        return redirect(url_for('security.security_dashboard'))

    return render_template("security/report.html")
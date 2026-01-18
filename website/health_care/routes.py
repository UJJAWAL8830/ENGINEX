from flask import (
     render_template, request,
    flash, redirect, url_for, session, jsonify
)
from flask_login import login_required, current_user
import PIL.Image
from . import health_care # Use the blueprint object defined in __init__.py
from .. import db
from .models import Hospital
from website.models import Citizens, Complaint
import google.genai as genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key="YOUR_ACTUAL_API_KEY")

@health_care.route('/health_dashboard')
@login_required
def health_dashboard():
    # Role-based protection for the National Digital Public Infrastructure
    if not isinstance(current_user, Citizens):
        flash("Access Denied: This portal is reserved for Citizens.", category="error")
        return redirect(url_for('auth.login'))

    user_city = current_user.city
    hospitals = Hospital.query.filter_by(city=user_city).all()
    
    return render_template("health_care/health_dashboard.html", 
                           hospitals=hospitals, 
                           city=user_city)

# FIX: Route path should be simple, not a file path
@health_care.route('/analyze', methods=['POST'])
@login_required
def analyze_health_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        img = PIL.Image.open(file)
        
        prompt = """
        Analyze this medical lab report image meticulously. 
        Extract the patient name and key test results.
        Provide the output strictly as a raw JSON object:
        {
            "patient_name": "Name",
            "summary": "1-sentence summary",
            "vital_results": [{"test_name": "name", "value": "val", "status": "Normal", "simple_explanation": "text"}],
            "doctor_note": "note"
        }
        Return ONLY JSON. No markdown.
        """

        # Gemini 2.0 Flash for low-latency national service delivery
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=[prompt, img]
        )
        
        clean_json = response.text.strip().replace("```json", "").replace("```", "")
        return jsonify({"analysis": clean_json})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
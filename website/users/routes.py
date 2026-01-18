import google.generativeai as genai
from flask_login import current_user
import PIL.Image
from flask import redirect, render_template, request, jsonify, session, url_for

from .models import Citizen, db, Hospital, AgriMarket
from . import users_bp

# 1. Configure API
genai.configure(api_key="AIzaSyDHi9ikTI4GhqZqAMI_WgOCCp-BcvLtUyk") # <--- PASTE KEY HERE

# --- CHATBOT MODEL (Strict "Government Official" Persona) ---
# This model is ONLY for the chat widget
chat_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""
    You are 'JanSetu Sahayak', a government service assistant. 
    Your goal is to help citizens navigate the portal.
    Keep answers short.
    """
)

# --- PAGE ROUTES ---
@users_bp.route('/home')
def home():
    # 1. Security Check: Is user logged in?
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 2. Fetch the logged-in user's details from the Database
    # We use the ID stored in the session to find them
    user = Citizen.query.get(session['user_id'])
    
    # 3. Pass this 'user' variable to the HTML
    return render_template('users/home.html', user=user)

@users_bp.route('/services')
def services():
    return render_template('users/services.html')

@users_bp.route('/services/health')
def health():
    return render_template('users/services/health.html')
@users_bp.route('/services/agriculture')
def agriculture():
    return render_template('users/services/agriculture.html')

@users_bp.route('/services/security')
def security():
    return render_template('users/services/security.html')

@users_bp.route('/news')
def news():
    return render_template('users/news.html')


# --- CHATBOT ROUTE ---
@users_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')
        history = session.get('chat_history', [])
        
        chat_session = chat_model.start_chat(history=history)
        response = chat_session.send_message(user_message)
        
        history.append({"role": "user", "parts": [user_message]})
        history.append({"role": "model", "parts": [response.text]})
        session['chat_history'] = history[-10:] 
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "Server Error."})


# --- HEALTH ANALYSIS ROUTE (THE FIX IS HERE) ---
import json # Import json at top

@users_bp.route('/services/health/analyze', methods=['POST'])
def analyze_health_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})
    
    file = request.files['file']
    
    try:
        img = PIL.Image.open(file)
        vision_model = genai.GenerativeModel('gemini-2.5-flash')
        
        # --- THE MAGIC PROMPT ---
        prompt = """
        Analyze this medical report image.
        Return the output strictly as a JSON object with this exact structure:
        {
            "patient_name": "Name found or 'Unknown'",
            "summary": "A 1-sentence simple summary of the report.",
            "vital_results": [
                {
                    "test_name": "e.g. Hemoglobin",
                    "value": "e.g. 12.5 g/dL",
                    "status": "Normal" or "High" or "Low",
                    "simple_explanation": "Simple explanation of what this means."
                }
            ],
            "doctor_note": "A polite, non-medical advice note for the patient."
        }
        Do not use Markdown formatting (no ```json). Just the raw JSON string.
        """
        
        response = vision_model.generate_content([prompt, img])
        
        # Clean the response just in case Gemini adds backticks
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        
        return jsonify({"analysis": clean_json})
        
    except Exception as e:
        return jsonify({"error": str(e)})

        # --- 1. THE PAGE ROUTE ---
@users_bp.route('/services/schemes')
def schemes():
    return render_template('users/services/schemes.html')

# --- 2. THE AI API ROUTE ---
@users_bp.route('/find-schemes', methods=['POST'])
def find_schemes():
    data = request.json
    
    profile = f"""
    Age: {data.get('age')}, Gender: {data.get('gender')}, 
    Occupation: {data.get('occupation')}, Annual Income: ₹{data.get('income')},
    State: {data.get('state')}, Category: {data.get('category')}
    """
    
    # --- UPDATED PROMPT ---
    prompt = f"""
    Act as an Indian Government Scheme Expert. 
    Analyze this citizen profile: {profile}
    
    Recommend the Top 3 Government Schemes they are eligible for.
    Return strictly as a JSON object with this structure:
    {{
        "schemes": [
            {{
                "name": "Scheme Name",
                "ministry": "Ministry Name",
                "benefits": "Key financial benefit",
                "approval_chance": "High" or "Medium",
                "documents_needed": ["Doc 1", "Doc 2"],
                
                "application_url": "ONLY the raw URL (e.g. https://pmkisan.gov.in). If you are not 100% sure of the URL, return 'SEARCH'." 
            }}
        ]
    }}
    Do not use Markdown. Just raw JSON.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return jsonify({"analysis": clean_json})
    except Exception as e:
        return jsonify({"error": str(e)})
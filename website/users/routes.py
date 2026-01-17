from flask import render_template
from . import users_bp

# --- HOME ROUTE ---
@users_bp.route('/home')
def home():
    faqs = [
        {
            "question": "How do I apply for the PM-Kisan Scheme?",
            "answer": "Navigate to the Services tab, select 'Agriculture', and click 'Apply Now'."
        },
        {
            "question": "Can I link my Aadhaar here?",
            "answer": "Yes. Go to your Profile settings to link your National ID securely."
        },
        {
            "question": "What if the website is down?",
            "answer": "Our system uses a distributed architecture, so it rarely goes down. Call 1800-HELPLINE for support."
        }
    ]
    return render_template('users/home.html', faqs=faqs)

# --- SERVICES ROUTE (The missing piece!) ---
@users_bp.route('/services')
def services():
    # You need to create services.html, or this will give a TemplateNotFound error next.
    # For now, let's just reuse home.html or a temporary string to prove the link works.
    return render_template('users/services.html') 

# --- NEWS ROUTE ---
@users_bp.route('/news')
def news():
    return render_template('users/news.html')
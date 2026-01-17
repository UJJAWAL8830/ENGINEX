from flask import render_template
from . import users_bp  # Import the blueprint we created above

@users_bp.route('/')
@users_bp.route('/home')
def home():
    # FAQ Data (Hardcoded for now, or fetch from DB later)
    faqs = [
        {"q": "How do I apply for a crop loan?", "a": "Go to the Services page and select Agriculture."},
        {"q": "Is my data secure?", "a": "Yes, we use government-grade encryption."},
        {"q": "How do I reset my password?", "a": "Contact the Help Desk at 1800-GOV-HELP."}
    ]
    return render_template('home.html', faqs=faqs)

@users_bp.route('/services')
def services():
    return render_template('services.html')

@users_bp.route('/news')
def news():
    return render_template('users/news.html')